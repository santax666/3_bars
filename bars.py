import json
import os
import argparse
from math import hypot


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def get_distance(start_point, end_point):
    return hypot((start_point[0]-end_point[0]), (start_point[1]-end_point[1]))


def get_data_for_analysis(json_data, coordinates):
    data_for_analysis = []
    for bar in json_data:
        bar_name = bar["Cells"]["Name"]
        bar_seats_count = bar["Cells"]['SeatsCount']
        distance_to_bar = get_distance(coordinates,
                                       bar["Cells"]["geoData"]["coordinates"])
        bar_info = (bar_name, bar_seats_count, distance_to_bar,)
        data_for_analysis.append(bar_info)
    return data_for_analysis


def find_extreme_values(data):
    biggest = max(data, key=lambda x: x[1])
    smallest = min(data, key=lambda x: x[1])
    nearest = min(data, key=lambda x: x[2])
    return biggest, smallest, nearest


def create_parser():
    parser = argparse.ArgumentParser(usage='%(prog)s [аргументы]',
                                     description="Определение самого большого,"
                                                 " маленького, близкого бара"
                                                 " с помощью %(prog)s")
    parser.add_argument("jsonfile", help="JSON-файл для обработки")
    parser.add_argument('--latitude', type=int, help="Ваша широта")
    parser.add_argument('--longitude', type=int, help="Ваша долгота")
    return parser


def get_your_coordinates(kind_param):
    coordinate = input("Пожалуйста, введите вашу {0}: ".format(kind_param))
    while not coordinate.isdecimal():
        coordinate = input("Неверный формат, повторите ввод: ")
    return int(coordinate)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    json_file = namespace.jsonfile
    latitude = namespace.latitude
    longitude = namespace.longitude

    json_data = load_data(json_file)
    if json_data is None:
        print("JSON-файл не обнаружен!")
    else:
        if latitude is None:
            latitude = get_your_coordinates('широту')
        if longitude is None:
            longitude = get_your_coordinates('долготу')
        coordinates = (latitude, longitude,)

        bars_data = get_data_for_analysis(json_data, coordinates)
        bars_info = find_extreme_values(bars_data)

        print("Самый большой бар:", bars_info[0][0])
        print("Самый маленький бар:", bars_info[1][0])
        print("Самый близкий бар:", bars_info[2][0])
