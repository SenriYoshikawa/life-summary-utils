import sys
import matplotlib.pyplot as plt
import glob
import os
import pandas as pd
import numpy as np
from datetime import *
from datetime import datetime as dt


def check_forward(sensor_list, index, n):
    try:
        for j in range(n):
            if sensor_list[index + j] > 0:
                return True
        return False
    except IndexError:
        return False


def check_back(sensor_list, index, n):
    try:
        for j in range(n):
            if sensor_list[index - j] > 0:
                return True
        return False
    except IndexError:
        return False


def find_next_flag(sensor_list, index):
    for j in range(index, len(sensor_list)):
        if sensor_list[j] > 0:
            return j
    return len(sensor_list) - 1


def data_load(in_filename):
    df = pd.read_csv(in_filename, header=None, names=['date', 'time', 'sensor1', 'sensor3'])
    df['sensor1'] = df['sensor1'].replace(
        {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
         'D': 13, 'E': 14, 'F': 15, 'x': -1, 'X': -1, '': -1})
    df['sensor3'] = df['sensor3'].replace(
        {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
         'D': 13, 'E': 14, 'F': 15, 'x': -1, 'X': -1, '': -1})
    df.fillna({'sensor1': -1, 'sensor3': -1})
    date_np = np.array(df)[:, 0:2]
    data_np = np.array(df)[:, 2:4]
    return [date_np, data_np]


def draw_graph(path, date_list, data_list, label_list):
    title = path[path.rfind('/') + 1:]
    title = path[path.rfind('\\') + 1:]
    title = title[:-4]
    try:
        os.mkdir(path[:-4])
    except FileExistsError:
        pass
    path = title + '/' + title

    week_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for now_time in range(1440, len(data_list), 1440):
        pre_date = date_list[now_time - 1440][0]
        # グラフ書き出し
        plt.cla()
        plt.figure(figsize=(20, 6))
        plt.tight_layout()
        week = datetime.strptime(pre_date, "%Y-%m-%d")
        # plt.suptitle(sys.argv[i][-11:-4] + " " + pre_date + " " + week_list[week.weekday()])
        plt.suptitle(title + " " + pre_date + " " + week_list[week.weekday()])

        plt.subplot(3, 1, 1)
        plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                   ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
        # plt.bar(range(1440),data_list[now_time-1440: now_time,0])
        plt.plot(data_list[now_time - 1440: now_time, 0])
        plt.ylim(-1, 17)
        plt.title("living", loc='right')

        plt.subplot(3, 1, 2)
        plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                   ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
        # plt.bar(range(1440),data_list[now_time-1440:now_time,1])
        plt.plot(data_list[now_time - 1440:now_time, 1])
        plt.ylim(-1, 17)
        plt.title("entrance", loc='right')

        plt.subplot(3, 1, 3)
        plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                   ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
        plt.plot(label_list[now_time - 1440:now_time])
        plt.ylim(-0.1, 1.1)
        plt.title("label", loc='right')

        plt.savefig(path + "-" + pre_date + ".png", transparent=False)
        plt.close()
        print(title + "-" + pre_date + " outputed")


def _main():
    if len(sys.argv) > 0 and sys.argv[1].find('csv') == -1:
        sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
        del sys.argv[1]

    for i in range(1, len(sys.argv)):
        in_filename = sys.argv[i]
        date_list, data_list = data_load(in_filename)
        label_list = np.zeros(len(date_list))



        pre_date = date_list[0][0]
        data_list[0][1] = 1

        for now_time in range(len(date_list)):
            now_date = date_list[now_time][0]

            if data_list[now_time][1] and (check_forward(data_list[:, 1], now_time+1, 10) is False or
                                           check_back(data_list[:, 1], now_time-1, 10) is False):
                label_list[now_time] = 1

        draw_graph(sys.argv[i], date_list, data_list, label_list)


if __name__ == '__main__':
    _main()
