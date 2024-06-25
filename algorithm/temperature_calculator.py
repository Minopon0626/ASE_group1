# 温度設定アルゴリズムのつもり
# 現在は最大温度を返す用にしてある

from datetime import datetime

def determine_season(date):
    """
    日付に基づいて季節を推測する関数
    :param date: 日付 (datetimeオブジェクト)
    :return: 推測された季節 ('summer' または 'winter')
    """
    month = date.month
    if 4 <= month <= 9:
        return 'summer'
    else:
        return 'winter'

def calculate_temperature(season, number_of_people):
    """
    温度を計算する関数
    :param season: 季節 ('summer' または 'winter')
    :param number_of_people: 人数
    :return: 調整後の最大温度 (float)
    """
    try:
        # ベース温度設定
        if season == 'summer':
            base_temp_min = 24
            base_temp_max = 26
        elif season == 'winter':
            base_temp_min = 20
            base_temp_max = 22
        else:
            raise ValueError("無効な季節です。「summer」または「winter」を指定してください。")

        # 温度調整
        adjustment = number_of_people * 0.5
        adjusted_temp_max = base_temp_max - adjustment

        # 最大温度を返す
        return adjusted_temp_max
    except Exception as e:
        print(f"エラー: {e}")

def get_season_and_temperature(number_of_people):
    """
    現在の日付を基に季節を推測し、人数に基づいて温度を計算する関数
    :param number_of_people: 人数
    :return: (season, max_temperature)
    """
    # 現在の日付を取得
    current_date = datetime.now()
    
    # 日付に基づいて季節を推測
    season = determine_season(current_date)
    
    # 温度計算
    max_temperature = calculate_temperature(season, number_of_people)
    
    return season, max_temperature

def get_temperature_based_on_people():
    """
    ユーザーから人数を入力させ、その人数に基づいて温度を計算する関数
    :return: 温度 (float)
    """
    try:
        number_of_people = int(input("人数を入力してください: "))
        season, max_temperature = get_season_and_temperature(number_of_people)
        if max_temperature is not None:
            print(f"現在の日付: {datetime.now().strftime('%Y-%m-%d')}")
            print(f"推測された季節: {season}")
            return max_temperature
    except ValueError:
        print("人数の入力が無効です。整数を入力してください。")
    except Exception as e:
        print(f"エラー: {e}")
