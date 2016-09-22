import json
import math

def load_data(filepath):
    return json.load(open(filepath,'r'))

def get_biggest_bar(data):
    i = 0
    max_seats = 0
    sp_max = []

    while i < len(data):
        if data[i]["Cells"]["SeatsCount"] == data[max_seats]["Cells"]["SeatsCount"]:
            sp_max.append(data[i]["Cells"]["Name"])
        elif data[i]["Cells"]["SeatsCount"] > data[max_seats]["Cells"]["SeatsCount"]:
            max_seats = i; sp_max = []; sp_max.append(data[i]["Cells"]["Name"]) #нашли больший бар, очищаем список больших баров
        i = i + 1
    return sp_max

def get_smallest_bar(data):
    i = 0
    min_seats = 0
    sp_min = []

    while i < len(data):
        if data[i]["Cells"]["SeatsCount"] == data[min_seats]["Cells"]["SeatsCount"]:
            sp_min.append(data[i]["Cells"]["Name"])
        elif data[i]["Cells"]["SeatsCount"] < data[min_seats]["Cells"]["SeatsCount"]:
            min_seats = i; sp_min = []; sp_min.append(data[i]["Cells"]["Name"]) #нашли меньший бар, очищаем список малых баров
        i = i + 1
    return sp_min

def get_closest_bar(data, longitude, latitude):
    i = 0
    min_dlina = math.sqrt((float(data[0]["Cells"]["geoData"]["coordinates"][0])-longitude)**2+(float(data[0]["Cells"]["geoData"]["coordinates"][1])-latitude)**2)
    sp_dl = []

    while i < len(data):
        dlina = math.sqrt((float(data[i]["Cells"]["geoData"]["coordinates"][0])-longitude)**2+(float(data[i]["Cells"]["geoData"]["coordinates"][1])-latitude)**2)
        if min_dlina == dlina:
            sp_dl.append(data[i]["Cells"]["Name"])
        elif dlina < min_dlina:
            min_dlina = dlina; sp_dl = []; sp_dl.append(data[i]["Cells"]["Name"]) #нашли ближайший бар, очищаем список близких баров
        i = i + 1
    return sp_dl

# проверка введенного числа
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
# ввод GPS-координат
    print('Здравствуйте!')

    x_gps = input("Пожалуйста, введите координаты широты вашего местоположения: ")
    while not is_digit(x_gps):
        x_gps = input("Широта введена неверно, повторите ввод: ")
    x_gps = float(x_gps.replace(',', '.'))

    y_gps = input("Пожалуйста, введите координаты долготы вашего местоположения: ")
    while not is_digit(y_gps):
        y_gps = input("Долгота введена неверно, повторите ввод: ")
    y_gps = float(y_gps.replace(',', '.'))

# чтение json-файла
    data = load_data('Бары.json')

# вывод результатов
    if len(get_biggest_bar(data)) < 2:
        print('Самый большой бар - ',get_biggest_bar(data)[0])
    else:
        print('Самые большие бары - ',get_biggest_bar(data))

    if len(get_smallest_bar(data)) < 2:
        print('Самый маленький бар - ',get_smallest_bar(data)[0])
    else:
        print('Самые маленькие бары - ',get_smallest_bar(data))

    if len(get_closest_bar(data,x_gps,y_gps)) < 2:
        print('Самый ближайший бар - ',get_closest_bar(data,x_gps,y_gps)[0])
    else:
        print('Самые близкие бары - ',get_closest_bar(data,x_gps,y_gps))


