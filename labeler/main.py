import sys
import matplotlib.pyplot as plt
import glob
import os
import pandas as pd
import numpy as np
from datetime import *
from datetime import datetime as dt
from statistics import mean


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
    #df['missing'] = [0 for i in range(len(df))]
    #df['missing'].where(
    #    (df.sensor1 != 'x') & (df.sensor1 != 'X') & (df.sensor1 != '') & (df.sensor3 != 'x') & (df.sensor3 != 'X') & (
    #    df.sensor3 != ''), 1)

    df['sensor1'] = df['sensor1'].replace(
        {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
         'D': 13, 'E': 14, 'F': 15, 'x': -1, 'X': -1, '': -1})
    df['sensor3'] = df['sensor3'].replace(
        {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12,
         'D': 13, 'E': 14, 'F': 15, 'x': -1, 'X': -1, '': -1})
    df.fillna({'sensor1': -1, 'sensor3': -1})
    date_np = np.array(df)[:, 0:2]
    data_np = np.array(df)[:, 2:4]
    #missing_np = np.array(df)[:, 4:5]
    #return [date_np, missing_np, data_np]
    return [date_np, data_np]


def draw_graph(path, date_list, data_list, turning_list, label_list):
    title = path[path.rfind('/') + 1:]
    title = title[path.rfind('\\') + 1:]
    title = title[:-4]
    try:
        os.mkdir(title)
    except FileExistsError:
        pass
    path = title + '/' + title

    week_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for now_time in range(1440, len(data_list), 1440):
        pre_date = date_list[now_time - 1440][0]
        # グラフ書き出し
        plt.cla()
        plt.figure(figsize=(20, 8))
        plt.tight_layout()
        week = datetime.strptime(pre_date, "%Y-%m-%d")
        # plt.suptitle(sys.argv[i][-11:-4] + " " + pre_date + " " + week_list[week.weekday()])
        plt.suptitle(title + " " + pre_date + " " + week_list[week.weekday()])

        plt.subplot(4, 1, 1)
        plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                   ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
        #plt.xticks(list(range(0,1441,120)), list([str(i) for i in range(0,25,2)]))
        # plt.bar(range(1440),data_list[now_time-1440: now_time,0])
        plt.plot(data_list[now_time - 1440: now_time, 0])
        plt.ylim(-1, 17)
        plt.title("living", loc='right')

        plt.subplot(4, 1, 2)
        plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                   ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
        # plt.bar(range(1440),data_list[now_time-1440:now_time,1])
        plt.plot(data_list[now_time - 1440:now_time, 1])
        plt.ylim(-1, 17)
        plt.title("entrance", loc='right')

        plt.subplot(4, 1, 3)
        plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                   ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
        plt.plot(turning_list[now_time - 1440:now_time])
        plt.ylim(-0.1, 1.1)
        plt.title("turning", loc='right')

        plt.subplot(4, 1, 4)
        plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                   ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
        plt.plot(label_list[now_time - 1440:now_time])
        plt.ylim(-1.1, 1.1)
        plt.title("label", loc='right')

        plt.savefig(path + "-" + pre_date + ".png", transparent=False)
        plt.close()
        print(title + "-" + pre_date + " outputted")


def write2csv(path, date_list, data_list, label_list):
    title = path[path.rfind('/') + 1:]
    title = title[path.rfind('\\') + 1:]
    title = title[:-4]
    outfile = open(title + "-result.csv", 'w')
    for i in range(len(date_list)):
        outfile.write(date_list[i][0] + ',' + date_list[i][1] + ',' + str(data_list[i][0]) + ',' + str(
            data_list[i][1]) + ',' + str(label_list[i]) + '\n')
    outfile.close()


def write2csv_for_fuji(path, date_list, missing_list, label_list):
    title = path[path.rfind('/') + 1:]
    title = title[path.rfind('\\') + 1:]
    title = title[:-4]
    outfile = open(title + "_absenceORpresenceORvisit_flgDaily.csv", 'w')
    for i in range(len(date_list)//1440):
        outfile.write(date_list[i*1440][0] + ',' + ('ok' if (missing_list[i] == 0) else 'ng'))
        for j in range(1440):
            outfile.write(',' + str(label_list[i*440+j]))
        outfile.write('\n')
    outfile.close()


def export2npy(path, data_list, label_list):
    title = path[path.rfind('/') + 1:]
    title = title[path.rfind('\\') + 1:]
    title = title[:-4]
    np.save(title + 'data.npy',data_list)
    np.save(title + 'label.npy', label_list)


def _main():
    if len(sys.argv) > 0 and sys.argv[1].find('csv') == -1:
        sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
        del sys.argv[1]

    for i in range(1, len(sys.argv)):
        in_filename = sys.argv[i]
        date_list, data_list = data_load(in_filename)
        turning_list = np.zeros(len(date_list))
        label_list = np.zeros(len(date_list))
        missing_list = np.zeros(len(date_list) // 1440)

        data_list[0][1] = 1

        for now_time in range(len(date_list)):
            if data_list[now_time][1] > 0:
                turning_list[now_time] = 1
            if data_list[now_time][0] < 0 or data_list[now_time][1] < 0:
                missing_list[now_time//1440] = 1

        for now_time in range(len(date_list)):
            if turning_list[now_time] > 0 and np.sum(turning_list[now_time: now_time + 30]) > 2:
                for j in reversed(range(now_time, now_time+30)):
                    if turning_list[j] > 0:
                        k = j
                        break
                for j in range(now_time+1, k):
                    turning_list[j] = 0

        for now_time in range(len(date_list)):
            if turning_list[now_time] == 1:
                start = now_time
                end = find_next_flag(turning_list, now_time+1)
                if mean(data_list[start:end, 0]) > 1 or (
                        end - start > 2 and + mean(data_list[start:end, 0]) + mean(data_list[start+1:end-1, 1]) > 1.5) or (
                        10 < end - start < 120 and max(data_list[start+5:end-5, 0] > 4)
                ):
                    for j in range(start, end):
                        label_list[j] = 1
                elif (end - start > 2 and mean(data_list[start+1:end-1, 0]) == 0 and label_list[now_time-2] != 1) or (
                        end - start > 1 and mean(data_list[start+1:end, 0]) == 0 and label_list[now_time-2] != 1) or (
                        end - start > 1 and mean(data_list[start:end-1, 0]) == 0 and label_list[now_time-2] != 1) or (
                        mean(data_list[start:end, 0]) == 0):
                    for j in range(start, end):
                        label_list[j] = -1
                now_time = end - 1

        draw_graph(sys.argv[i], date_list, data_list, turning_list, label_list)
        write2csv(sys.argv[i], date_list, data_list, label_list)
        #export2npy(sys.argv[i], data_list, missing_list)
        write2csv_for_fuji(sys.argv[i], date_list, missing_list, label_list


if __name__ == '__main__':
    _main()
