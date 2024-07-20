#必要なモジュールのインポート
#GPIOピン制御ライブラリ
import RPi.GPIO as GPIO
import time
import sys
 
#ポート番号の定義
Sw_GPIO = 23
#GPIOの設定
GPIO.setmode(GPIO.BCM)
#GPIO23を入力モードに設定してプルダウン抵抗を有効にする
GPIO.setup(Sw_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
while True:
    try:
        #GPIO23の入力を読み取る
        switchStatus = GPIO.input(Sw_GPIO)
        #スイッチが押下された時に”Hi!”と出力
        if switchStatus == 1:
            print(“Hi!”)
        time.sleep(0.1)
 
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()