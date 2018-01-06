# coding: UTF-8
import sys
import csv
import matplotlib.pyplot as plt
import datetime
import numpy as np
import glob
import os
import jholiday


if len(sys.argv) > 0 and sys.argv[1].find('csv') == -1:
    sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
    del sys.argv[1]

for i in range(1, len(sys.argv)):
    infile = open(sys.argv[i], 'r')
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('/') + 1:]
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('\\') + 1:]

    outfile = open(sys.argv[i][:-4] + " strip activity result.csv", 'w')
    outfile_sumarry = open(sys.argv[i][:-4] + " strip activity sumarry.csv", 'w')
    reader = csv.reader(infile)
    pre_date = next(reader)[0]
    infile.seek(0)
    go_entrance_flag = 0
    go_entrance_count = 0
    strip_count = 0
    strip_list = []
    strip_count_list = []
    strip_stdev_list = []
    go_living_flag = 0
    go_living_count = 0
    active_days_count = 0
    month_list = []

    for row in reader:
        date = row[0]
        if row[1] == "08:00":
            for j in range(60 * 10):
                next(reader)

        if row[1] == "00:00":
            this_date = datetime.date(int(row[0][0:4]), int(row[0][5:7]), int(row[0][-2:]))
            # 土曜日から２日スキップ
            if this_date.weekday() == 5:
                for j in range(60 * 24 * 2):
                    try:
                        next(reader)
                    except StopIteration:
                        pass

            # 祝日はスキップ
            if jholiday.holiday_name(date=this_date) is not None:
                for j in range(60 * 24):
                    next(reader)

            # 年末年始はスキップ
            if row[0][-5:] == "12-30":
                for j in range(60 * 24 * 4):
                    try:
                        next(reader)
                    except StopIteration:
                        pass

            # お盆はスキップ
            if row[0][-5:] == "08-13":
                for j in range(60 * 24 * 4):
                    try:
                        next(reader)
                    except StopIteration:
                        pass

        # yyyy-mm-dd が変わったとき
        if pre_date != date:
            if len(strip_list) != 0:
                active_days_count += 1
            strip_count += len(strip_list)
            if len(strip_list) > 0:
                outfile_sumarry.write(pre_date + ',' + str(len(strip_list)) + '\n')

            for j in range(len(strip_list)):
                outfile.write(pre_date + ',' + strip_list[j] + '\n')
            strip_list.clear()

            # yyyy-mm が変わったとき
            if pre_date[:-3] != date[:-3]:
                if active_days_count != 0:
                    strip_count /= active_days_count
                    #print(pre_date[:-3] + " " + str(active_days_count) + " " + str(strip_count))
                    strip_count_list.append(strip_count)
                    strip_stdev_list.append(np.std(strip_count_list))
                    month_list.append(pre_date[:-3])
                strip_count = 0
                active_days_count = 0

            pre_date = date

        if len(row) > 2 and row[2] != 'x' and row[2] != 'X':
            sensor1 = int(row[2], 16)
            if len(row) > 3 and row[3] != 'x' and row[3] != 'X':
                sensor3 = int(row[3], 16)
            else:
                sensor3 = -1
        else:
            sensor1 = -1
            sensor3 = -1

        if go_entrance_flag != 0:
            go_entrance_count += 1
        if sensor1 > 0 and sensor3 > 0:
            if go_entrance_flag == 2:
                go_entrance_flag = 0
                go_entrance_count = 0
                strip_list.append(row[1] + ',go entrance')
            else:
                go_entrance_flag = 2
                go_entrance_count = 1
        elif sensor1 > 0:
            if go_entrance_flag == 2:
                go_entrance_flag = 0
                go_entrance_count = 0
                strip_list.append(row[1] + ',go entrance')
            else:
                go_entrance_flag = 1
                go_entrance_count = 1
        elif sensor3 > 0 and go_entrance_flag == 1:
            go_entrance_flag = 2
        if go_entrance_count > 10:
            go_entrance_count = 0
            go_entrance_flag = 0

        if go_living_flag != 0:
            go_living_count += 1
        if sensor3 > 0 and sensor1 > 0:
            if go_living_flag == 2:
                go_living_flag = 0
                go_living_count = 0
                strip_list.append(row[1] + ',go living')
            else:
                go_living_flag = 2
                go_living_count = 1
        elif sensor1 > 0:
            if go_living_flag == 2:
                go_living_flag = 0
                go_living_count = 0
                strip_list.append(row[1] + ',go living')
            else:
                go_living_flag = 1
                go_living_count = 1
        elif sensor3 > 0 and go_living_flag == 1:
            go_living_flag = 2
        if go_living_count > 10:
            go_living_count = 0
            go_living_flag = 0

    # グラフ書き出し
    plt.clf()
    plt.subplots_adjust(bottom=0.2)
    x = range(len(month_list))
    plt.plot(x, strip_count_list, "-o")
    plt.plot(x, np.poly1d(np.polyfit(x, strip_count_list, 1))(x), '--')
    plt.errorbar(x, strip_count_list, yerr=strip_stdev_list, fmt='o')
    plt.legend()
    plt.xlabel("month")
    plt.xticks(range(len(month_list))[::(len(month_list)//12)], month_list[::(len(month_list)//12)], rotation=45)
    plt.title(sys.argv[i][:-4] + " strip activity result")
    plt.savefig(sys.argv[i][:-4] + " strip activity result.png")

    slope = np.polyfit(x, strip_count_list, 1)[0]
    print(sys.argv[i][:-4] + "の結果")
    if slope < 0:
        print("帯状活動は減少しています")
    else:
        print("帯状衰えは見られません")
    print("slope = "  + str(slope))
