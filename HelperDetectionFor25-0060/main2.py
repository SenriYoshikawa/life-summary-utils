import sys
import csv
import matplotlib.pyplot as plt
import glob
import os


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

    sensor1_list = []
    sensor3_list = []
    helper_list = [0 for j in range(1440)]
    helper_flag = 0
    helper_count = 0

    day_count = 0
    min_count = 0

    for row in reader:
        date = row[0]
        min_count = min_count + 1

        #print(date)
        if pre_date != date:  # yyyy-mm-dd が変わったとき
            day_count = day_count + 1
            #if day_count == 3:
            #    exit(0)

            date_hyphen = pre_date.replace('/', '-')

            # グラフ書き出し
            plt.clf()
            plt.suptitle(sys.argv[i][-11:-4] + " " + date_hyphen)

            plt.subplot(3, 1, 1)
            plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                       ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
            plt.plot(sensor1_list)
            plt.ylim(-1, 17)

            plt.subplot(3, 1, 2)
            plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                       ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
            plt.plot(sensor3_list)
            plt.ylim(-1, 17)

            plt.subplot(3, 1, 3)
            plt.xticks([0, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440],
                       ["0", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"])
            plt.plot(helper_list)
            plt.ylim(0, 1)

            plt.savefig(sys.argv[i][0:-4] + "-" + date_hyphen + ".png")
            print(sys.argv[i][-11:-4] + "-" + date_hyphen + " outputed")

            sensor1_list.clear()
            sensor3_list.clear()
            helper_list.clear()
            helper_list = [0 for j in range(1440)]
            pre_date = date
            min_count = 1

        if len(row) > 2 and row[2] != 'x' and row[2] != 'X':
            sensor1_list.append(int(row[2], 16))
            if len(row) > 3 and row[3] != 'x' and row[3] != 'X':
                sensor3_list.append(int(row[3], 16))
            else:
                sensor3_list.append(0)
        else:
            sensor1_list.append(0)
            sensor3_list.append(0)

        if helper_flag != 0:
            helper_count = helper_count + 1

        if helper_flag == 0 and sensor3_list[-1] != 0:
            helper_flag = 1
            helper_count = 0

        elif helper_flag == 1 and sensor1_list[-1] != 0:
            helper_flag = 2

        elif helper_flag == 2 and sensor3_list[-1] != 0:
            helper_flag = 0
            for j in range(helper_count):
                helper_list[min_count-j] = 1

        if helper_count > 120:
            helper_flag = 0
            helper_count = 0

        #print(str(row[1]) + " " + str(day_count) + " " + str(helper_count))