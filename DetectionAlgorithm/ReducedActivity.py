import sys
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import numpy as np
import glob
import os

def make_sentence(a):
    if a < -50:
        return "急激に減少しています."
    elif a < 20:
        return "減少しています."
    elif a < 0:
        return "やや減少しています."
    elif a < 20:
        return "やや増加しています."
    elif a < 50:
        return "増加しています."
    else:
        return "急激に増加しています."


if len(sys.argv) > 0 and sys.argv[1].find('csv') == -1:
    sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
    del sys.argv[1]

for i in range(1, len(sys.argv)):
    infile = open(sys.argv[i], 'r')
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('/') + 1:]
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('\\') + 1:]

    try:
        os.mkdir(sys.argv[i][:-4])
    except FileExistsError:
        pass

    sys.argv[i] = sys.argv[i][:-4] + '/' + sys.argv[i]
    outfile_1 = open(sys.argv[i][:-4] + "-living.csv", 'w')
    outfile_3 = open(sys.argv[i][:-4] + "-entrance.csv", 'w')
    reader = csv.reader(infile)

    # 平均値計算変数
    sensor1_sum = 0
    sensor1_cnt = 0
    sensor3_sum = 0
    sensor3_cnt = 0
    # 月平均保存変数
    sensor1_result = [[] for j in range(13)]
    sensor3_result = [[] for j in range(13)]

    year_list = []
    pre_date = next(reader)[0]
    infile.seek(0)

    # 記録開始月までのセルは0埋めしておく
    for j in range(int(pre_date[5:7])):
        sensor1_result[j].append(0)
        sensor3_result[j].append(0)

    for row in reader:
        date = row[0]

        if pre_date[0:-3] != date[0:-3]:  # yyyy-mm が変わったとき
            month = int(pre_date[5:7])
            if pre_date[0:4] != date[0:4]:
                year_list.append(int(pre_date[0:4]))
            if sensor1_cnt == 0:
                sensor1_result[month].append(0)
            else:
                sensor1_result[month].append(float(sensor1_sum) / sensor1_cnt)
            if sensor3_cnt == 0:
                sensor3_result[month].append(0)
            else:
                sensor3_result[month].append(float(sensor3_sum) / sensor3_cnt)
            sensor1_sum = 0
            sensor1_cnt = 0
            sensor3_sum = 0
            sensor3_cnt = 0
            pre_date = date

            if len(sensor1_result[month]) > 2 or (len(sensor1_result[month]) > 1 and sensor1_result[month][0] != 0):
                ratio = -1
                if sensor1_result[month][-2] < 0.1:
                    ratio = 1000
                else:
                    ratio = (1 - float(sensor1_result[month][-1]) / sensor1_result[month][-2])*100
                print(pre_date[0:-3] + " 前年同月比" + str('{:+3d}'.format(round(ratio))) + "%です." + make_sentence(ratio))

        if len(row) > 2 and row[2] != 'x' and row[2] != 'X':
            sensor1_sum += int(row[2], 16)
            sensor1_cnt += 1
            if len(row) > 3 and row[3] != 'x' and row[3] != 'X':
                sensor3_sum += int(row[3], 16)
                sensor3_cnt += 1

    for j in range(1,13):
        for k in range(len(sensor1_result[1]) - len(sensor1_result[j])):
            sensor1_result[j].append(0)
            sensor3_result[j].append(0)

    # csv書き出し
    year_list.append(year_list[-1] + 1)
    outfile_1.write(',')
    for j in year_list:
        outfile_1.write(str(j) + ',')
    outfile_1.write('\n')
    for j in range(1,13):
        outfile_1.write('month ' + str(j) + ',')
        for k in range(len(sensor1_result[j])):
            outfile_1.write(str(sensor1_result[j][k]) + ',')
        outfile_1.write('\n')

    outfile_3.write(',')
    for j in year_list:
        outfile_3.write(str(j) + ',')
    outfile_3.write('\n')
    for j in range(1,13):
        outfile_3.write('month ' + str(j) + ',')
        for k in range(len(sensor3_result[j])):
            outfile_3.write(str(sensor3_result[j][k]) + ',')
        outfile_3.write('\n')

    # 3ヶ月ごとにまとめる
    for j in range(1,5):
        for k in range(len(sensor1_result[1])):
            temp = np.count_nonzero([sensor1_result[(j - 1) * 3 + 1][k], sensor1_result[(j - 1) * 3 + 2][k],
                                     sensor1_result[(j - 1) * 3 + 3][k]])
            temp = 1 if temp == 0 else temp
            sensor1_result[j][k] = (sensor1_result[(j - 1) * 3 + 1][k] + sensor1_result[(j - 1) * 3 + 2][k] +
                                    sensor1_result[(j - 1) * 3 + 3][k]) / temp
            sensor3_result[j][k] = (sensor3_result[(j - 1) * 3 + 1][k] + sensor3_result[(j - 1) * 3 + 2][k] +
                                    sensor3_result[(j - 1) * 3 + 3][k]) / temp

    slope_list1 = []
    slope_list3 = []

    # グラフ書き出し
    plt.clf()
    label_list = ["q1", "q2", "q3", "q4"]
    color_list1 = ["blue", "red", "green", "coral"]
    color_list2 = ["steelblue", "tomato", "yellowgreen", "orange"]
    for j in range(1,5):
        a = 1 if sensor1_result[j][0] == 0 else 0
        b = len(sensor1_result[j])-1 if sensor1_result[j][-1] == 0 else len(sensor1_result[j])
        x = range(a,b)
        plt.plot(x, sensor1_result[j][a:b], "-o", label=label_list[j-1], color = color_list1[j-1])
        plt.plot(x, np.poly1d(np.polyfit(x, sensor1_result[j][a:b], 1))(x), '--', color = color_list2[j-1])
        slope_list1.append(np.polyfit(x, sensor1_result[j][a:b], 1)[0])
    plt.legend()
    plt.xlabel("year")
    plt.xticks(range(len(year_list)), year_list)
    plt.title(sys.argv[i][-11:-4] + "living")
    plt.savefig(sys.argv[i][0:-4] + "living.png")

    plt.clf()
    for j in range(1,5):
        a = 1 if sensor3_result[j][0] == 0 else 0
        b = len(sensor3_result[j])-1 if sensor3_result[j][-1] == 0 else len(sensor3_result[j])
        x = range(a,b)
        plt.plot(x, sensor3_result[j][a:b], "-o", label=label_list[j-1], color = color_list1[j-1])
        plt.plot(x, np.poly1d(np.polyfit(x, sensor3_result[j][a:b], 1))(x), '--', color = color_list2[j-1])
        slope_list3.append(np.polyfit(x, sensor1_result[j][a:b], 1))
    plt.legend()
    plt.xlabel("year")
    plt.xticks(range(len(year_list)), year_list)
    plt.title(sys.argv[i][-11:-4] + "entrance")
    plt.savefig(sys.argv[i][0:-4] + "entrance.png")

    slope = float(sum(slope_list1))/len(slope_list1)
    print(sys.argv[i][-11:-4] + "の結果")
    if slope < 0:
        print("衰えが見られます")
    else:
        print("衰えは見られません")