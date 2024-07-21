import time
import RPi.GPIO as GPIO

# GPIOの初期設定
GPIO.setmode(GPIO.BCM)

# GPIO18を入力端子として設定
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        try:
            # スイッチ押下待ち、デバウンス時間を設定
            GPIO.wait_for_edge(18, GPIO.FALLING, bouncetime=200)
            # 画面出力
            print('スイッチON!')
            # チャタリング対策
            time.sleep(0.3)
        except RuntimeError as e:
            print(f"RuntimeError: {e}")
except KeyboardInterrupt:
    print("プログラムが中断されました")
finally:
    GPIO.cleanup()