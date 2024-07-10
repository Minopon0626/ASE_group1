import pyautogui
import time
import threading
import os

# スレッドの実行状態を管理する辞書
thread_status = {
    "Thread A": False,
    "Thread B": False,
    "Thread C": False
}

def thread_function(thread_name):
    print(f"スレッド {thread_name} が実行中です")
    if thread_name == "Thread A":
        pyautogui.rightClick()
        time.sleep(60)
    elif thread_name == "Thread B":
        pyautogui.press('space')
        time.sleep(120)
    elif thread_name == "Thread C":
        pyautogui.leftClick()
        time.sleep(180)
    print(f"スレッド {thread_name} の実行が完了しました")
    # スレッドの実行が終了したら、そのスレッドの実行状態をFalseに更新
    thread_status[thread_name] = False

def main():
    user_input = input("A, B, C, END のいずれかを入力してください: ")
    if user_input == "END":
        return
    # スレッドが既に実行中であれば、新たに起動しない
    if not thread_status[user_input]:
        # スレッドの実行状態をTrueに更新
        thread_status[user_input] = True
        # スレッドを作成して実行
        thread = threading.Thread(target=thread_function, args=(user_input,))
        thread.start()

    # 残り時間を表示する関数を別のスレッドで実行
    thread_print = threading.Thread(target=print_remaining_time)
    thread_print.start()

def clear_terminal():
    # ターミナルの画面をクリア
    os.system('cls' if os.name == 'nt' else 'clear')

def print_remaining_time():
    while True:
        clear_terminal()
        print("スレッド A が実行中です" if thread_status["Thread A"] else "スレッド A は実行中ではありません")
        print("スレッド B が実行中です" if thread_status["Thread B"] else "スレッド B は実行中ではありません")
        print("スレッド C が実行中です" if thread_status["Thread C"] else "スレッド C は実行中ではありません")
        time.sleep(1)

if __name__ == "__main__":
    main()
