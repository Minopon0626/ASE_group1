# 必要なモジュールのインポート
import RPi.GPIO as GPIO
import time
import sys

# ポート番号の定義
Sw_GPIO = 23
# GPIOの設定
GPIO.setmode(GPIO.BCM)
# GPIO23を入力モードに設定してプルダウン抵抗を有効にする
GPIO.setup(Sw_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# デバウンス処理のための時間（秒）
debounce_time = 0.02  # 20ミリ秒

while True:
    try:
        # GPIO23の入力を読み取る
        switchStatus = GPIO.input(Sw_GPIO)
        if switchStatus == 1:
            # デバウンス処理
            time.sleep(debounce_time)
            # 再度スイッチの状態を確認
            if GPIO.input(Sw_GPIO) == 1:
                print("Hi!")
                # スイッチが離されるまで待機
                while GPIO.input(Sw_GPIO) == 1:
                    time.sleep(0.1)
        time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
