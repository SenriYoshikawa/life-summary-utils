import sys
import csv
import matplotlib.pyplot as plt


weatherfile = open(sys.argv[1], 'r')

for i in range(2, len(sys.argv)):
    weather = csv.reader(weatherfile)
    infile = open(sys.argv[i], 'r')
    reader = csv.reader(infile)

    s_row = next(reader)
    w_row = next(weather)

    s1a_vol = []
    s1a_cnt = []
    s2a_vol = []
    s2a_cnt = []
    s1e_vol = [[] for j in range(13)]
    s1e_cnt = [[] for j in range(13)]
    s2e_vol = [[] for j in range(13)]
    s2e_cnt = [[] for j in range(13)]
    w1e = [[] for j in range(13)]
    w2e = [[] for j in range(13)]

    w1 = []
    w2 = []

    weatherfile.seek(0)
    while s_row[0] != w_row[0]:
        w_row = next(weather)

    infile.seek(0)
    s1_vol = 0
    s1_cnt = 0
    s2_vol = 0
    s2_cnt = 0

    for row in reader:
        current_month = int(row[0][5:7])
        w_row[3] = w_row[3].replace(' )', '')
        w_row[3] = w_row[3].replace(' ]', '')

        if len(row) > 2:
            s1_vol += 0 if (row[2] == 'x' or row[2] == 'X') else int(row[2], 16)
            s1_cnt += 0 if (row[2] == 'x' or row[2] == 'X' or row[2] == '0') else 1
        if len(row) > 3:
            s2_vol += 0 if (row[3] == 'x' or row[3] == 'X') else int(row[3], 16)
            s2_cnt += 0 if (row[3] == 'x' or row[3] == 'X' or row[3] == '0') else 1

        if row[1][3:5] == '00':
            s1_vol = 0
            s2_vol = 0
            s1_cnt = 0
            s2_cnt = 0

        if row[1][3:5] == '59':
            if s1_vol > 0 and w_row[3] != '///':
                s1a_vol.append(s1_vol)
                s1a_cnt.append(s1_cnt)
                w1.append(float(w_row[3]))
                s1e_vol[current_month].append(s1_vol)
                s1e_cnt[current_month].append(s1_cnt)
                w1e[current_month].append(float(w_row[3]))


            if s2_vol > 0 and w_row[3] != '///':
                s2a_vol.append(s2_vol)
                s2a_cnt.append(s2_cnt)
                w2.append(float(w_row[3]))
                s2e_vol[current_month].append(s2_vol)
                s2e_cnt[current_month].append(s2_cnt)
                w2e[current_month].append(float(w_row[3]))

            try:
                w_row = next(weather)
            except Exception as e:
                print('file out range. ', e)
                break

    infile.close()

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.scatter(s1a_vol, w1, alpha=0.2, s=0.5)
    ax1.set_title('living')
    ax1.set_xlabel('sensor1 volume')
    ax1.set_ylabel('temperature[deg]')
    ax1.set_xlim(0,)
    ax1.set_ylim(-15, 40)

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.scatter(s2a_vol, w2, alpha=0.2, s=0.5)
    ax2.set_title('entrance')
    ax2.set_xlabel('sensor2 volume')
    ax2.set_ylabel('temperature[deg]')
    ax2.set_xlim(0,)
    ax2.set_ylim(-15, 40)

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.scatter(s1a_cnt, w1, alpha=0.2, s=0.5)
    ax3.set_title('living')
    ax3.set_xlabel('sensor1 count')
    ax3.set_ylabel('temperature[deg]')
    ax3.set_xlim(0,)
    ax3.set_ylim(-15, 40)

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.scatter(s2a_cnt, w2, alpha=0.2, s=0.5)
    ax4.set_title('entrance')
    ax4.set_xlabel('sensor2 count')
    ax4.set_ylabel('temperature[deg]')
    ax4.set_xlim(0,)
    ax4.set_ylim(-15, 40)

    fig.tight_layout()
    plt.savefig(sys.argv[i][0:-4] + "temprature_all_month.png")

    fig = plt.figure(figsize=(20, 12))
    for j in range(1, 13):
        ax1 = fig.add_subplot(6, 8, j * 4 - 3)
        ax1.scatter(s1e_vol[j], w1e[j], alpha=0.5, s=0.5)
        ax1.set_title("month" + str(j) + "living")
        ax1.set_xlabel('sensor1 volume')
        ax1.set_ylabel('temperature[deg]')
        ax1.set_xlim(0, )
        ax1.set_ylim(-15, 40)

        ax2 = fig.add_subplot(6, 8, j * 4 - 2)
        ax2.scatter(s1e_cnt[j], w1e[j], alpha=0.5, s=0.5)
        ax2.set_title("month" + str(j) + "living")
        ax2.set_xlabel('sensor1 count')
        ax2.set_ylabel('temperature[deg]')
        ax2.set_xlim(0, )
        ax2.set_ylim(-15, 40)

        ax3 = fig.add_subplot(6, 8, j * 4 - 1)
        ax3.scatter(s2e_vol[j], w2e[j], alpha=0.5, s=0.5)
        ax3.set_title("month" + str(j) + "entrance")
        ax3.set_xlabel('sensor2 volume')
        ax3.set_ylabel('temperature[deg]')
        ax3.set_xlim(0, )
        ax3.set_ylim(-15, 40)

        ax4 = fig.add_subplot(6, 8, j * 4)
        ax4.scatter(s2e_cnt[j], w2e[j], alpha=0.5, s=0.5)
        ax4.set_title("month" + str(j) + "entrance")
        ax4.set_xlabel('sensor2 count')
        ax4.set_ylabel('temperature[deg]')
        ax4.set_xlim(0, )
        ax4.set_ylim(-15, 40)

    fig.tight_layout()
    plt.savefig(sys.argv[i][0:-4] + "temprature _each_month.png")

weatherfile.close()