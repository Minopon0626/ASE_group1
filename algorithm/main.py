# 実行確認用コード
from temperature_calculator import get_temperature_based_on_people

def main():
    max_temperature = get_temperature_based_on_people()
    if max_temperature is not None:
        print(f"調整後の最大温度: {max_temperature:.1f}°C")

if __name__ == "__main__":
    main()
