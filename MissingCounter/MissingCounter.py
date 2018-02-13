# coding: UTF-8
import numpy as np
import sys
import csv
import matplotlib.pyplot as plt
import glob


def id_to_user(id_str):
    if id_str == '07-0030':
        return 'A'
    if id_str == '10-0050':
        return 'B'
    if id_str == '12-0340':
        return 'C'
    if id_str == '18-0047':
        return 'D'
    if id_str == '18-0309':
        return 'E'
    if id_str == '18-0384':
        return 'F'
    if id_str == '19-0115':
        return 'G'
    if id_str == '20-0077':
        return 'H'
    if id_str == '25-0060':
        return 'I'
    if id_str == '44-0046':
        return 'J'
    if id_str == '48-0025':
        return 'K'
    return 'None user'


if len(sys.argv) > 0 and sys.argv[1].find('csv') == -1:
    sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
    del sys.argv[1]

for i in range(1, len(sys.argv)):
    infile = open(sys.argv[i], 'r')
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('/') + 1:]
    sys.argv[i] = sys.argv[i][sys.argv[i].rfind('\\') + 1:]

    reader = csv.reader(infile)
    pre_date = next(reader)[0]
    month_list = []
    s1_month_list = []
    s3_month_list = []
    count = 0
    s1_missing = 0
    s3_missing = 0
    infile.seek(0)

    for row in reader:
        date = row[0]
        # yyyy-mm が変わったとき
        if pre_date[:-3] != date[:-3]:
            if count == 0:
                s1_month_list.append(0)
                s3_month_list.append(0)
            else:
                s1_month_list.append((count-s1_missing)/count*100)
                s3_month_list.append((count-s3_missing)/count*100)
            month_list.append(pre_date[:-3])
            count = 0
            s1_missing = 0
            s3_missing = 0
            pre_date = date

        count += 1
        if len(row) < 3 or row[2] == 'x' or row[2] == 'X' or row[2] == '':
            s1_missing += 1
            if len(row) < 4 or row[3] == 'x' or row[3] == 'X' or row[3] == '':
                s3_missing += 1

    # グラフ書き出し
    plt.clf()
    plt.figure(figsize=(9,6))
    plt.bar(np.arange(len(s1_month_list))*2-0.4, s1_month_list, align='center', label='Liginv', color='grey')
    plt.bar(np.arange(len(s3_month_list))*2+0.4, s3_month_list, align='center', label='Enterway', color='black')
    plt.ylim(0, 100)
    plt.xlabel("month")
    plt.ylabel("acquisition rate [%]")
    plt.xticks(range(len(month_list)*2)[::(len(month_list)*2//12)], month_list[::(len(month_list)//12)], rotation=15)
    plt.legend(loc=2)
    plt.title('User ' + id_to_user(sys.argv[i][-11:-4]) + " data acquisition rate")
    plt.savefig('user-' + id_to_user(sys.argv[i][-11:-4]) + "data-acquisition-rate.png")
