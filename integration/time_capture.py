from datetime import datetime

def get_current_timestamp():
    """
    現在の日時を取得し、フォーマットする関数
    :return: フォーマットされた現在の日時
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")  # 現在の日時を取得し、フォーマット