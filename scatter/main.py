import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


weatherfile = open(sys.argv[1], 'r')

for i in range(2, len(sys.argv)):
    weather = csv.reader(weatherfile)
    infile = open(sys.argv[i], 'r')
    reader = csv.reader(infile)

    s_row = next(reader)
    w_row = next(weather)

    s1 = [[] for row in range(4)]
    s2 = [[] for row in range(4)]
    w1 = [[] for row in range(4)]
    w2 = [[] for row in range(4)]

    weatherfile.seek(0)
    while s_row[0] != w_row[0]:
        w_row = next(weather)

    infile.seek(0)
    s1_sum = [0]*4
    s2_sum = [0]*4
    for row in reader:
        w_row[3] = w_row[3].replace(' )', '')
        w_row[3] = w_row[3].replace(' ]', '')
        for j in range(4):
            if (j * 3) + 1 <= int(row[0][5:7]) <= (j * 3) + 3:
                s1_sum[j] += 0 if(row[2] == 'x' or row[2] == 'X') else int(row[2], 16)
                s2_sum[j] += 0 if(row[3] == 'x' or row[3] == 'X') else int(row[3], 16)

        if row[1][3:5] == '00':
            s1_sum = [0]*4
            s2_sum = [0]*4

        if row[1][3:5] == '59':
            for j in range(4):
                if s1_sum[j] > 0 and w_row[3] != '///':
                    s1[j].append(s1_sum[j])
                    w1[j].append(float(w_row[3]))

                if s2_sum[j] > 0 and w_row[3] != '///':
                    s2[j].append(s2_sum[j])
                    w2[j].append(float(w_row[3]))

            try:
                w_row = next(weather)
            except Exception as e:
                print('file out range. ', e)
                break

    infile.close()

    fig = plt.figure()
    colors = ['r', 'b', 'g', 'y']

    ax1 = fig.add_subplot(1, 2, 1)
    for j in range(4):
        ax1.scatter(s1[j], w1[j], alpha=0.2, s=0.5, color=colors[j])
    ax1.set_title('living sensor templature scatter')
    ax1.set_xlabel('sensor1')
    ax1.set_ylabel('templature[deg]')
    ax1.set_xlim(0,)
    ax1.set_ylim(-15, 40)

    ax2 = fig.add_subplot(1, 2, 2)
    for j in range(4):
        ax2.scatter(s2[j], w2[j], alpha=0.2, s=0.5, color=colors[j])
    ax2.set_title('entrance sensor templature scatter')
    ax2.set_xlabel('sensor2')
    ax2.set_ylabel('templature[deg]')
    ax2.set_xlim(0,)
    ax2.set_ylim(-15, 40)

    fig.tight_layout()
    plt.savefig(sys.argv[i][:-16] + ".png")

weatherfile.close()
