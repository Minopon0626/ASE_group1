# 必要なモジュールのインポート
import RPi.GPIO as GPIO
import time
import sys

# ポート番号の定義
Sw_GPIO_1 = 23
Sw_GPIO_2 = 21
LED_GPIO_1 = 24

same = 0 #同時押しの値

# GPIOの設定
GPIO.setmode(GPIO.BCM)
# GPIO23とGPIO21を入力モードに設定してプルダウン抵抗を有効にする
GPIO.setup(Sw_GPIO_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Sw_GPIO_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO24とGPIO25を出力モードに設定
GPIO.setup(LED_GPIO_1, GPIO.OUT)

# デバウンス処理のための時間（秒）
debounce_time = 0.02  # 20ミリ秒
# 点滅のための時間（秒）
blink_interval = 0.5  # 0.5秒

stabilize_time = 10

while True:
    try:
        same = 0
        # GPIO23とGPIO21の入力を読み取る
        switchStatus_1 = GPIO.input(Sw_GPIO_1)
        switchStatus_2 = GPIO.input(Sw_GPIO_2)
        
        if switchStatus_1 == 1 and switchStatus_2 == 1:
            time.sleep(debounce_time)
            if GPIO.input(Sw_GPIO_1) == 1 and GPIO.input(Sw_GPIO_2) == 1:
                same = 1
            # 両方のスイッチが押されている場合
                print("same time")
                while GPIO.input(Sw_GPIO_1) == 1 and GPIO.input(Sw_GPIO_2) == 1:
                    GPIO.output(LED_GPIO_1, GPIO.HIGH)  # LEDを点灯
                    time.sleep(blink_interval)  # 点灯時間
                    GPIO.output(LED_GPIO_1, GPIO.LOW)   # LEDを消灯
                    time.sleep(blink_interval)  # 消灯時間
                GPIO.output(LED_GPIO_1, GPIO.LOW)   # LEDを消灯

            # 同時押し解除後の安定化待機
            time.sleep(stabilize_time)
            
        elif switchStatus_1 == 1 and same == 0:
            # GPIO23のスイッチのみが押されている場合
            time.sleep(debounce_time)
            if GPIO.input(Sw_GPIO_1) == 1:
                print("samui")
                GPIO.output(LED_GPIO_1, GPIO.HIGH)  # LEDを点灯
                while GPIO.input(Sw_GPIO_1) == 1:
                    time.sleep(0.1)
                GPIO.output(LED_GPIO_1, GPIO.LOW)  # LEDを消灯
        
        elif switchStatus_2 == 1 and same == 0:
            # GPIO21のスイッチのみが押されている場合
            time.sleep(debounce_time)
            if GPIO.input(Sw_GPIO_2) == 1:
                print("atui")
                GPIO.output(LED_GPIO_1, GPIO.HIGH)  # LEDを点灯
                while GPIO.input(Sw_GPIO_2) == 1:
                    time.sleep(0.1)
                GPIO.output(LED_GPIO_1, GPIO.LOW)  # LEDを消灯
        
        time.sleep(0.1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
