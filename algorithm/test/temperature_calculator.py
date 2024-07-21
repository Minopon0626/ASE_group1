def validate_thresholds(cooling_threshold, heating_threshold):
    # 冷房または暖房の基準温度がNoneの場合、エラーメッセージを表示して例外を発生
    if cooling_threshold is None or heating_threshold is None:
        raise ValueError("エラー: 冷房または暖房の基準温度を計算できませんでした。データを確認してください。")
    # 冷房の基準温度が暖房の基準温度以下の場合、エラーメッセージを表示して例外を発生
    if cooling_threshold <= heating_threshold:
        raise ValueError("エラー: 冷房の基準温度は暖房の基準温度以上でなければなりません (cooling_threshold >= heating_threshold)")

def calculate_temperature(data, mode):
    sum_2 = 0  # 温度の合計（寒い）
    count_2 = 0  # データ点の数（寒い）
    sum_1 = 0  # 温度の合計（熱い）
    count_1 = 0  # データ点の数（熱い）

    # 各行のデータを処理
    for line in data:
        print(f"Processing line: {line}")  # デバッグメッセージ：処理する行を表示
        try:
            # データを温度と入力値に分割
            temperature, input_value = line.split(',')
            temperature = float(temperature)
            input_value = int(input_value)

            if mode == 'cooling':
                if input_value == 2:
                    sum_2 += temperature
                    count_2 += 1
                elif input_value == 1:
                    sum_1 += temperature
                    count_1 += 1
            elif mode == 'heating':
                if input_value == 1:
                    sum_1 += temperature
                    count_1 += 1
                elif input_value == 2:
                    sum_2 += temperature
                    count_2 += 1
        except ValueError:
            print(f"Invalid data format: {line}")  # データ形式が無効な場合のエラーメッセージ
            continue

    # データ点の数が0の場合、計算をスキップ
    if count_2 == 0 or count_1 == 0:
        if mode == 'cooling':
            print(f"Calculation failed for cooling: count_2={count_2}, count_1={count_1}")  # デバッグメッセージ：冷房の計算失敗
        elif mode == 'heating':
            print(f"Calculation failed for heating: count_2={count_2}, count_1={count_1}")  # デバッグメッセージ：暖房の計算失敗
        return None  # 計算できない場合はNoneを返す

    average_2 = sum_2 / count_2  # 寒いデータの平均温度を計算
    average_1 = sum_1 / count_1  # 熱いデータの平均温度を計算
    print(f"Averages for {mode}: average_2={average_2}, average_1={average_1}")  # デバッグメッセージ：平均温度を表示
    return (average_2 + average_1) / 2  # 平均値を返す

def adjust_temperature_for_people(cooling_threshold, heating_threshold, person_adjustment):
    adjusted_cooling = cooling_threshold - person_adjustment  # 人数補正後の冷房基準温度
    adjusted_heating = heating_threshold - person_adjustment  # 人数補正後の暖房基準温度
    return adjusted_cooling, adjusted_heating  # 補正後の基準温度を返す

def calculate_person_adjustment(long_sleeve_count, short_sleeve_count, long_sleeve_rate, short_sleeve_rate):
    person_adjustment = long_sleeve_count * long_sleeve_rate + short_sleeve_count * short_sleeve_rate  # 人数補正量を計算
    return person_adjustment  # 人数補正量を返す

def adjust_person_count(num_people, long_sleeve_count, short_sleeve_count):
    total_clothes = long_sleeve_count + short_sleeve_count  # 長袖と半袖の合計人数
    if num_people == total_clothes:
        return long_sleeve_count, short_sleeve_count  # 合計人数が一致する場合、そのまま返す
    elif num_people > total_clothes:
        difference = num_people - total_clothes  # 差分を計算
        adjusted_long_sleeve_count = long_sleeve_count + (difference * 0.5)  # 長袖人数を調整
        adjusted_short_sleeve_count = short_sleeve_count + (difference * 0.5)  # 半袖人数を調整
    else:
        difference = total_clothes - num_people  # 差分を計算
        adjusted_long_sleeve_count = max(0, long_sleeve_count - (difference * 0.5))  # 長袖人数を減少
        adjusted_short_sleeve_count = max(0, short_sleeve_count - (difference * 0.5))  # 半袖人数を減少

    return adjusted_long_sleeve_count, adjusted_short_sleeve_count  # 調整後の人数を返す
