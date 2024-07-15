# pip install pyyaml

import os
import shutil
import random
from pathlib import Path
import yaml
import tkinter as tk
from tkinter import filedialog

def select_directory(title):
    root = tk.Tk()
    root.withdraw()  # ウィンドウを隠す
    directory = filedialog.askdirectory(title=title)
    root.destroy()
    return directory

# ディレクトリを選択
source_dir = select_directory('移動元ディレクトリを選択してください')
dataset_dir = select_directory('移動先ディレクトリを選択してください')

# ディレクトリパスの設定
train_images_dir = os.path.join(dataset_dir, 'images', 'train')
val_images_dir = os.path.join(dataset_dir, 'images', 'val')
train_labels_dir = os.path.join(dataset_dir, 'labels', 'train')
val_labels_dir = os.path.join(dataset_dir, 'labels', 'val')

# 必要なディレクトリを作成
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# 画像とラベルファイルのリストを取得
image_files = [f for f in os.listdir(source_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
label_files = [f for f in os.listdir(source_dir) if f.endswith('.txt')]

# 画像ファイルと対応するラベルファイルのペアを作成
file_pairs = [(img, img.replace(img.split('.')[-1], 'txt')) for img in image_files]

# データセットをシャッフル
random.shuffle(file_pairs)

# トレーニングと検証の分割比率
train_ratio = 0.8
train_size = int(len(file_pairs) * train_ratio)

# トレーニングデータと検証データに分割
train_pairs = file_pairs[:train_size]
val_pairs = file_pairs[train_size:]

# ファイルを対応するディレクトリに移動
for img, lbl in train_pairs:
    shutil.move(os.path.join(source_dir, img), os.path.join(train_images_dir, img))
    shutil.move(os.path.join(source_dir, lbl), os.path.join(train_labels_dir, lbl))

for img, lbl in val_pairs:
    shutil.move(os.path.join(source_dir, img), os.path.join(val_images_dir, img))
    shutil.move(os.path.join(source_dir, lbl), os.path.join(val_labels_dir, lbl))

# データ設定ファイルの作成
data_yaml = {
    'train': os.path.abspath(train_images_dir),
    'val': os.path.abspath(val_images_dir),
    'nc': 2,  # クラスの数
    'names': ['hansode', 'nagasode']  # クラス名のリスト
}

with open('data.yaml', 'w') as yaml_file:
    yaml.dump(data_yaml, yaml_file, default_flow_style=False)

print("データセットの準備が完了しました。")
