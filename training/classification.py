# pip install pillow

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import os
import shutil

class AnnotationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("画像注釈ツール")
        
        # ウィンドウサイズを設定
        self.root.geometry("800x600")

        # フレームを作成してキャンバスとクラスIDの設定を分ける
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # キャンバスを作成し、クロスカーソルを設定
        self.canvas = tk.Canvas(self.top_frame, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image_path = None
        self.img = None
        self.rect = None
        self.start_x = None
        self.start_y = None

        # クラスIDのリストを作成（ここにクラス名を追加）
        self.classes = ["hansode", "nagasode"]
        self.class_id_var = tk.StringVar(value=self.classes)

        # クラスIDを選択するためのリストボックスを作成
        self.listbox = tk.Listbox(self.bottom_frame, listvariable=self.class_id_var, height=6)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)

        # マウスのイベントをバインド
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # メニューを作成
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.menu.add_command(label="画像ディレクトリを設定", command=self.set_image_directory)
        self.menu.add_command(label="次の画像を読み込む", command=self.load_next_image)
        self.menu.add_command(label="注釈を保存", command=self.save_annotation)

        self.image_directory = None
        self.annotated_directory = None
        self.image_list = []
        self.current_image_index = 0

    def set_image_directory(self):
        # 画像ディレクトリと記録済みディレクトリを選択
        self.image_directory = filedialog.askdirectory(title="画像ディレクトリを選択")
        self.annotated_directory = filedialog.askdirectory(title="記録済みディレクトリを選択")
        if self.image_directory and self.annotated_directory:
            self.image_list = [f for f in os.listdir(self.image_directory) if f.endswith(('.jpg', '.jpeg', '.png'))]
            self.current_image_index = 0
            self.load_next_image()

    def load_next_image(self):
        # 次の画像を読み込む
        if not self.image_list or self.current_image_index >= len(self.image_list):
            messagebox.showinfo("完了", "すべての画像に注釈が付けられました。")
            return
        
        image_filename = self.image_list[self.current_image_index]
        self.image_path = os.path.join(self.image_directory, image_filename)

        # 画像を開いてキャンバスに表示
        self.img = Image.open(self.image_path)
        self.display_image(self.img)

        self.current_image_index += 1

    def display_image(self, img):
        # 画像を表示する
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 画像のサイズをウィンドウに合わせて調整
        img.thumbnail((canvas_width, canvas_height))
        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_img, anchor=tk.NW)

    def on_button_press(self, event):
        # マウスボタンが押されたときの処理
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_move_press(self, event):
        # マウスがドラッグされたときの処理
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        # マウスボタンが離されたときの処理
        pass

    def save_annotation(self):
        # 注釈を保存する処理
        if not self.image_path or not self.rect:
            return

        # バウンディングボックスの座標を取得
        bbox = self.canvas.coords(self.rect)
        selected_class_index = self.listbox.curselection()

        if not selected_class_index:
            print("クラスIDを選択してください。")
            return

        class_id = selected_class_index[0]  # 選択されたクラスID
        class_name = self.classes[class_id]  # クラス名

        # ナンバリング用に同クラスの既存ファイル数をカウント
        existing_files = [f for f in os.listdir(self.annotated_directory) if f.startswith(f"{class_name}__")]
        numbering = len(existing_files) + 1

        img_name_no_ext = f"{class_name}__{numbering}"
        annotation_file = os.path.join(self.annotated_directory, f"{img_name_no_ext}.txt")
        annotated_image_path = os.path.join(self.annotated_directory, f"{img_name_no_ext}.jpg")

        # 画像の幅と高さを取得
        width, height = self.img.size
        center_x = ((bbox[0] + bbox[2]) / 2) / width
        center_y = ((bbox[1] + bbox[3]) / 2) / height
        bbox_width = (bbox[2] - bbox[0]) / width
        bbox_height = (bbox[3] - bbox[1]) / height

        # 注釈をテキストファイルに保存
        with open(annotation_file, "w") as f:
            f.write(f"{class_id} {center_x} {center_y} {bbox_width} {bbox_height}\n")

        # 画像を記録済みディレクトリに移動
        shutil.move(self.image_path, annotated_image_path)

        print(f"注釈が{annotation_file}に保存され、画像が{annotated_image_path}に移動されました")

        # 次の画像を読み込む
        self.load_next_image()

if __name__ == "__main__":
    root = tk.Tk()
    tool = AnnotationTool(root)
    root.mainloop()
