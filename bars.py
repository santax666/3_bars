import json
import os
import argparse
from math import hypot


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def get_distance(longitude, latitude, bar_coordinates):
    return hypot((longitude-bar_coordinates[0]), (latitude-bar_coordinates[1]))


def get_parse_data(data, longitude, latitude):
    parse_data = []
    for bar in data:
        name = bar["Cells"]["Name"]
        seats = bar["Cells"]['SeatsCount']
        distance = get_distance(longitude, latitude,
                                bar["Cells"]["geoData"]["coordinates"])
        bar_info = (name, seats, distance,)
        parse_data.append(bar_info)
    return parse_data


def get_bar(data):
    big = max(data, key=lambda x: x[1])
    small = min(data, key=lambda x: x[1])
    near = min(data, key=lambda x: x[2])
    return big, small, near


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string.replace(',', '.'))
            return True
        except ValueError:
            return False


def createParser():
    parser = argparse.ArgumentParser(usage='%(prog)s [аргументы]',
                                     description="Определение самого большого,"
                                                 " маленького, близкого бара"
                                                 " с помощью %(prog)s")
    parser.add_argument("jsonfile", help="JSON-файл для обработки")
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    json_file = namespace.jsonfile

    jsonfile = load_data(json_file)
    if jsonfile is None:
        print("JSON-файл не обнаружен!")
    else:
        latitude = input("Пожалуйста, введите вашу широту: ")
        while not is_digit(latitude):
            latitude = input("Неверная широта, повторите ввод: ")
        latitude = float(latitude.replace(',', '.'))

        longitude = input("Пожалуйста, введите вашу долготу: ")
        while not is_digit(longitude):
            longitude = input("Неверная долгота, повторите ввод: ")
        longitude = float(longitude.replace(',', '.'))

        bars_data = get_parse_data(jsonfile, longitude, latitude)
        bars = get_bar(bars_data)
        print("Самый большой бар:", bars[0][0])
        print("Самый маленький бар:", bars[1][0])
        print("Самый близкий бар:", bars[2][0])
