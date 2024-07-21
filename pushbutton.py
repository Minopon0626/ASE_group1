# 必要なモジュールのインポート
import RPi.GPIO as GPIO
import time
import sys

# ポート番号の定義
Sw_GPIO_1 = 23
Sw_GPIO_2 = 21

# GPIOの設定
GPIO.setmode(GPIO.BCM)
# GPIO23とGPIO21を入力モードに設定してプルダウン抵抗を有効にする
GPIO.setup(Sw_GPIO_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw_GPIO_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# デバウンス処理のための時間（秒）
debounce_time = 0.02  # 20ミリ秒

while True:
    try:
        # GPIO23の入力を読み取る
        switchStatus_1 = GPIO.input(Sw_GPIO_1)
        if switchStatus_1 == 1:
            # デバウンス処理
            time.sleep(debounce_time)
            # 再度スイッチの状態を確認
            if GPIO.input(Sw_GPIO_1) == 1:
                print("samui")
                # スイッチが離されるまで待機
                while GPIO.input(Sw_GPIO_1) == 1:
                    time.sleep(0.1)
        
        # GPIO21の入力を読み取る
        switchStatus_2 = GPIO.input(Sw_GPIO_2)
        if switchStatus_2 == 1:
            # デバウンス処理
            time.sleep(debounce_time)
            # 再度スイッチの状態を確認
            if GPIO.input(Sw_GPIO_2) == 1:
                print("atui")
                # スイッチが離されるまで待機
                while GPIO.input(Sw_GPIO_2) == 1:
                    time.sleep(0.1)
        
        time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
