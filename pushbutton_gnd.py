#タクトスイッチが押下された時の処理

import time

#GPIOの初期設定
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#GPIO18を入力端子設定
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    #スイッチ押下待ち
    GPIO.wait_for_edge(18, GPIO.FALLING)

    #画面出力
    print('スイッチON!')

    #チャタリング対策
    time.sleep(0.3)