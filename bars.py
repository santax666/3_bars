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
    return hypot(
        (longitude - bar_coordinates[0]), (latitude - bar_coordinates[1]))


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


def set_preset_options(bar_type):
    preset_options = {
        'big': (
            True, 1), 'small': (
            False, 1), 'near': (
                False, 2)}
    return preset_options[bar_type]


def get_bar(data, options):
    name_of_bar = []
    data.sort(key=lambda bar: bar[options[1]], reverse=options[0])
    for bar in data:
        if bar[options[1]] != data[0][options[1]]:
            break
        name_of_bar.append(bar[0])
    mark_of_bar = data[0][options[1]]
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
        sys.exit
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

        data_print = [['большой(ые)', 'big', ', посадочных мест:'],
                      ['маленький(ие)', 'small', ', посадочных мест:'],
                      ['ближайший(ие)', 'near', ', расстояние до бара(ов):']]
        for data in data_print:
            options = set_preset_options(data[1])
            print('Самый(ые)', data[0], 'бар(ы):',
                  get_bar(bars_data, options)[0], data[2],
                  get_bar(bars_data, options)[1])
