# タクトスイッチのテストファイル

import RPi.GPIO as GPIO               # 必要なモジュールをインポートします

button_pin = 12                       # GPIO 12にボタンをつなぎます

def button_callback(channel):         # ボタンが押された時にやりたいことを
    print("Button was pushed!")       # この行から書いておきます

GPIO.setmode(GPIO.BCM)                # BCMモードでGPIOを使用します

# GPIO 12を入力モードにし、プルアップします
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ボタンが押されてGPIO 12がGNDになることを検出し、button_callbackを起動します
# bouncetimeはボタン押しの検出間隔です
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_callback, bouncetime=200)

# 画面に文字を表示し、待機に入ります
input("Press button to count, or Enter to quit\n")

# キーボードの何かのキーが押されると実行します
GPIO.cleanup()
print("Bye!")