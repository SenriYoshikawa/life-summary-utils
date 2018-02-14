import sys
import csv
import matplotlib.pyplot as plt
import glob
import os
from datetime import *


def checkFoward(sensor_list, index, n):
    try:
        for j in range(n):
            if sensor_list[index + j] != 0:
                return True
        return False
    except IndexError:
        return False


def checkBack(sensor_list, index, n):
    try:
        for j in range(n):
            if sensor_list[index - j] != 0:
                return True
        return False
    except IndexError:
        return False


if len(sys.argv) > 0 and sys.argv[1].find('csv') == -1:
    sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
    del sys.argv[1]

for i in range(1, len(sys.argv)):
    infile = open(sys.argv[i], 'r', encoding='utf-8')
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('/') + 1:]
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('\\') + 1:]

    try:
        os.mkdir(sys.argv[i][:-4])
    except FileExistsError:
        pass

    sys.argv[i] = sys.argv[i][:-4] + '/' + sys.argv[i]
    reader = csv.reader(infile)

    pre_date = next(reader)
    infile.seek(0)
    pre_date = pre_date[0]

    sensor1_list = [0 for j in range(1440)]
    sensor3_list = [0 for j in range(1440)]
    helper_list = [0 for j in range(1440)]
    week_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    helper_flag = 0
    helper_count = 0
    min_count = -1
    count = 1

    for row in reader:
        date = row[0]
        min_count = min_count + 1

        #print(date)
        if pre_date != date:  # yyyy-mm-dd が変わったとき

            for min_count in range(1440):
                if helper_flag != 0:
                    helper_count = helper_count + 1

                if helper_flag == 0 and sensor3_list[min_count] != 0 and checkFoward(sensor1_list, min_count, 15):
                    helper_flag = 1
                    helper_count = 0

                elif helper_flag == 1 and sensor3_list[min_count] != 0 and helper_count > 50 and \
                        (checkFoward(sensor3_list, min_count+1, 30) is False):
                    #print("helper_count = " + str(helper_count))
                    for j in range(helper_count):
                        helper_list[min_count - j] = 1
                    helper_flag = 2
                    helper_count = 0

                elif helper_flag == 2:
                    helper_flag = 0
                    helper_count = 0

                if helper_count > 120:
                    helper_flag = 0
                    helper_count = 0

                #print(str(int(min_count / 60))+":"+str(min_count%60) + " " + str(sensor1_list[min_count]) + " " + str(sensor3_list[min_count]) + " " +
                #      str(helper_flag) + " " + str(helper_count) + " " + str(
                 #   checkBack(sensor1_list, min_count, 6)) + " " +
                  #    str(checkFoward(sensor1_list, min_count, 6)))

            #print(pre_date)
            count = count + 1
            date_hyphen = pre_date.replace('/', '-')

            # グラフ書き出し
            plt.clf()
            week = datetime.strptime(pre_date, "%Y-%m-%d")
            plt.suptitle(sys.argv[i][-11:-4] + " " + date_hyphen + " " + week_list[week.weekday()])
            plt.title("living")

            plt.subplot(3, 1, 1)
            plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                       ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
            plt.plot(sensor1_list)
            plt.ylim(-1, 17)
            plt.title("entrance")

            plt.subplot(3, 1, 2)
            plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                       ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
            plt.plot(sensor3_list)
            plt.ylim(-1, 17)

            plt.subplot(3, 1, 3)
            plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                       ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
            plt.plot(helper_list)
            plt.ylim(-0.1, 1.1)
            plt.title("helper")

            plt.savefig(sys.argv[i][0:-4] + "-" + date_hyphen + ".png")
            print(sys.argv[i][-11:-4] + "-" + date_hyphen + " outputed")
            #print(helper_list)

            min_count = 0
            helper_count = 0
            helper_flag = 0
            for j in range(1440):
                helper_list[j] = 0
            pre_date = date

            #if count > 3:
            #    exit(0)

        if len(row) > 2 and row[2] != 'x' and row[2] != 'X':
            sensor1_list[min_count] = int(row[2], 16)
            if len(row) > 3 and row[3] != 'x' and row[3] != 'X':
                sensor3_list[min_count] = (int(row[3], 16))
            else:
                sensor3_list[min_count] = 0
        else:
            sensor1_list[min_count] = 0
            sensor3_list[min_count] = 0
