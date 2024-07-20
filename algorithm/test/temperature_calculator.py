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

def adjust_temperature_for_people(cooling_threshold, heating_threshold, person_adjustment):
    adjusted_cooling = cooling_threshold - person_adjustment
    adjusted_heating = heating_threshold - person_adjustment
    return adjusted_cooling, adjusted_heating

def calculate_person_adjustment(long_sleeve_count, short_sleeve_count, long_sleeve_rate, short_sleeve_rate):
    person_adjustment = long_sleeve_count * long_sleeve_rate + short_sleeve_count * short_sleeve_rate
    return person_adjustment

def adjust_person_count(num_people, long_sleeve_count, short_sleeve_count):
    total_clothes = long_sleeve_count + short_sleeve_count
    if num_people == total_clothes:
        return long_sleeve_count, short_sleeve_count
    elif num_people > total_clothes:
        difference = num_people - total_clothes
        adjusted_long_sleeve_count = long_sleeve_count + (difference * 0.5)
        adjusted_short_sleeve_count = short_sleeve_count + (difference * 0.5)
    else:
        difference = total_clothes - num_people
        adjusted_long_sleeve_count = max(0, long_sleeve_count - (difference * 0.5))
        adjusted_short_sleeve_count = max(0, short_sleeve_count - (difference * 0.5))

    return adjusted_long_sleeve_count, adjusted_short_sleeve_count
