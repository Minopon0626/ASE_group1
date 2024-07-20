def validate_thresholds(cooling_threshold, heating_threshold):
    if cooling_threshold is None or heating_threshold is None:
        raise ValueError("エラー: 冷房または暖房の基準温度を計算できませんでした。データを確認してください。")
    if cooling_threshold <= heating_threshold:
        raise ValueError("エラー: 冷房の基準温度は暖房の基準温度以上でなければなりません (cooling_threshold >= heating_threshold)")

def calculate_temperature(data, mode):
    sum_0_2 = 0
    count_0_2 = 0
    sum_1 = 0
    count_1 = 0

    for line in data:  # ヘッダー行も含めてすべての行を処理
        print(f"Processing line: {line}")  # デバッグメッセージ
        temperature, input_value = line.split(',')
        temperature = float(temperature)
        input_value = int(input_value)

        if mode == 'cooling':
            if input_value in [0, 2]:
                sum_0_2 += temperature
                count_0_2 += 1
            elif input_value == 1:
                sum_1 += temperature
                count_1 += 1
        elif mode == 'heating':
            if input_value in [0, 1]:
                sum_0_2 += temperature
                count_0_2 += 1
            elif input_value == 2:
                sum_1 += temperature
                count_1 += 1

    if count_0_2 == 0 or count_1 == 0:
        if mode == 'cooling':
            print(f"Calculation failed for cooling: count_0_2={count_0_2}, count_1={count_1}")  # デバッグメッセージ
        elif mode == 'heating':
            print(f"Calculation failed for heating: count_0_2={count_0_2}, count_1={count_1}")  # デバッグメッセージ
        return None  # 計算できない場合

    average_0_2 = sum_0_2 / count_0_2
    average_1 = sum_1 / count_1
    print(f"Averages for {mode}: average_0_2={average_0_2}, average_1={average_1}")  # デバッグメッセージ
    return (average_0_2 + average_1) / 2

def adjust_temperature_for_people(cooling_threshold, heating_threshold, num_people):
    adjusted_cooling = cooling_threshold - num_people
    adjusted_heating = heating_threshold - num_people
    return adjusted_cooling, adjusted_heating