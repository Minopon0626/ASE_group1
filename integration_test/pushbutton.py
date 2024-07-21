import RPi.GPIO as GPIO
import time
import sys
import os
import queue

# ポート番号の定義
Sw_GPIO_1 = 23
Sw_GPIO_2 = 21
LED_GPIO_1 = 24

same = 0  # 同時押しの値

# デバウンス処理のための時間（秒）
debounce_time = 0.02  # 20ミリ秒
# 点滅のための時間（秒）
blink_interval = 0.5  # 0.5秒
stabilize_time = 10

# デフォルトのパラメータ設定（適切な値に置き換えてください）
room_temperature = 22.0
cooling_threshold = 25.0
heating_threshold = 18.0
num_people = 3
directory_paths = {}  # ディレクトリパスはcreate_directories()関数で設定する

# 共有キューを作成
shared_queue = queue.Queue()

def setup_gpio():
    """GPIOの設定を行う関数"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Sw_GPIO_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(Sw_GPIO_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_GPIO_1, GPIO.OUT)

def handle_switches():
    global same
    global directory_paths

    # ディレクトリを作成し、パスを取得
    from algorithm.file_manager import create_directories
    directory_paths = create_directories()

    setup_gpio()
    
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
                    print("同時押し")
                    shared_queue.put(0)
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
                    print("寒い")
                    shared_queue.put(2)
                    GPIO.output(LED_GPIO_1, GPIO.HIGH)  # LEDを点灯
                    while GPIO.input(Sw_GPIO_1) == 1:
                        time.sleep(0.1)
                    GPIO.output(LED_GPIO_1, GPIO.LOW)  # LEDを消灯
            
            elif switchStatus_2 == 1 and same == 0:
                # GPIO21のスイッチのみが押されている場合
                time.sleep(debounce_time)
                if GPIO.input(Sw_GPIO_2) == 1:
                    print("暑い")
                    shared_queue.put(1)
                    GPIO.output(LED_GPIO_1, GPIO.HIGH)  # LEDを点灯
                    while GPIO.input(Sw_GPIO_2) == 1:
                        time.sleep(0.1)
                    GPIO.output(LED_GPIO_1, GPIO.LOW)  # LEDを消灯
            
            time.sleep(0.1)

            # capture_and_process_images からのメッセージをチェック
            if not shared_queue.empty():
                data_received = shared_queue.get()
                print(f"handle_switchesで受信したデータ: {data_received}")
                # ここで受信データに対して処理を行います

        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()
