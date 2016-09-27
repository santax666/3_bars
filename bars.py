import json
import os
import sys


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def get_distance(my_longitude, my_latitude, bar_longitude, bar_latitude):
    return ((my_longitude - bar_longitude)**2 + (my_latitude - bar_latitude)**2)**0.5


def get_bar(data, bar_type, my_longitude, my_latitude):
    if bar_type == 'big':
        sorted_bars = sorted(data, key=lambda bar: bar['Cells']['SeatsCount'], reverse=True)
        mark_of_bar = sorted_bars[0]['Cells']['SeatsCount']
    elif bar_type == 'small':
        sorted_bars = sorted(data, key=lambda bar: bar['Cells']['SeatsCount'])
        mark_of_bar = sorted_bars[0]['Cells']['SeatsCount']
    elif bar_type == 'near':
        sorted_bars = sorted(data, key=lambda bar: get_distance(my_longitude, my_latitude, bar["Cells"]["geoData"]["coordinates"][0], bar["Cells"]["geoData"]["coordinates"][1]))
        mark_of_bar = get_distance(my_longitude, my_latitude, sorted_bars[0]["Cells"]["geoData"]["coordinates"][0], sorted_bars[0]["Cells"]["geoData"]["coordinates"][1])
    else:
        return None

    number_of_seats = sorted_bars[0]['Cells']['SeatsCount']
    name_of_bar = []
    for bar in sorted_bars:
        if bar_type == 'near':
            if mark_of_bar != get_distance(my_longitude, my_latitude, bar["Cells"]["geoData"]["coordinates"][0], bar["Cells"]["geoData"]["coordinates"][1]):
                break
        else:
            if mark_of_bar != bar['Cells']['SeatsCount']:
                break
        name_of_bar.append(bar["Cells"]["Name"])
    return name_of_bar, mark_of_bar


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string.replace(',', '.'))
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("Скрипт находит самый большой, маленький и ближайший бары из JSON-файла.")
            print("Введите в терминале: python3.5 bars.py file.json")
        else:
            bars_json = load_data(sys.argv[1])
            if bars_json is None:
                print("JSON-файл не обнаружен!")
                sys.exit
            else:
                my_latitude = input("Пожалуйста, введите координаты широты вашего местоположения: ")
                while not is_digit(my_latitude):
                    my_latitude = input("Широта введена неверно, повторите ввод: ")
                my_latitude = float(my_latitude.replace(',', '.'))

                my_longitude = input("Пожалуйста, введите координаты долготы вашего местоположения: ")
                while not is_digit(my_longitude):
                    my_longitude = input("Долгота введена неверно, повторите ввод: ")
                my_longitude = float(my_longitude.replace(',', '.'))

                print('Самый(ые) большой(ые) бар(ы):', get_bar(bars_json, 'big',my_longitude, my_latitude)[0], ', число посадочных мест:', get_bar(bars_json, 'big',my_longitude, my_latitude)[1])
                print('Самый(ые) маленький(ие) бар(ы):', get_bar(bars_json, 'small',my_longitude, my_latitude)[0], ', число посадочных мест:', get_bar(bars_json, 'small',my_longitude, my_latitude)[1])
                print('Самый(ые) ближайший(ие) бар(ы):', get_bar(bars_json, 'near',my_longitude, my_latitude)[0], ', расстояние до бара(ов):', get_bar(bars_json, 'near',my_longitude, my_latitude)[1])
    else:
        print("Не задан JSON-файл для обработки!")
