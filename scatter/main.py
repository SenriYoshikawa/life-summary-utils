import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


weatherfile = open(sys.argv[1], 'r')

for i in range(2, len(sys.argv)) :
    weather = csv.reader(weatherfile)
    infile = open(sys.argv[i], 'r')
    reader = csv.reader(infile)

    s_row = next(reader)
    w_row = next(weather)

    weatherfile.seek(0)
    while s_row[0] != w_row[0]:
        w_row = next(weather)

    s1 = []
    s2 = []
    w1 = []
    w2 = []

    infile.seek(0)
    for row in reader:
        w_row[3] = w_row[3].replace(' )', '')
        w_row[3] = w_row[3].replace(' ]', '')
        if len(row) > 2 and w_row[3] != "///" and row[2] != 'x' and row[2] != 'X':
            s1.append(0 if (row[2] == 'x' or row[2] == 'X') else row[2])
            w1.append(float(w_row[3]))
        if len(row) > 3 and w_row[3] != "///" and row[3] != 'x' and row[3] != 'X':
            s2.append(0 if (row[3] == 'x' or row[3] == 'X') else row[3])
            w2.append(float(w_row[3]))

        try:
            w_row = next(weather)
        except Exception as e:
            print('file out range. ', e)
            break

    infile.close()

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.scatter(s1, w1, alpha=0.2, s=0.5)
    ax1.set_title('living sensor templature scatter')
    ax1.set_xlabel('sensor1')
    ax1.set_ylabel('templature[deg]')
    ax1.set_xlim(0,)
    ax1.set_ylim(-15, 40)
    # fig1.show()

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(s2, w2, alpha=0.2, s=0.5)
    ax2.set_title('entrance sensor templature scatter')
    ax2.set_xlabel('sensor2')
    ax2.set_ylabel('templature[deg]')
    ax2.set_xlim(0,)
    ax2.set_ylim(-15, 40)
    # fig2.show()

    fig.tight_layout()
    plt.savefig(sys.argv[i][0:-4] + ".png")

weatherfile.close()
