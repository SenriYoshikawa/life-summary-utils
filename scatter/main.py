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

    s1 = []
    s2 = []
    w1 = []
    w2 = []

    while s_row[0] != w_row[0]:
        w_row = next(weather)

        # print(s_row[0] + " " + s_row[1] + " " + w_row[0] + " " + w_row[1])

    infile.seek(0)
    s1_sum = 0
    s2_sum = 0
    for row in reader:
        w_row[3] = w_row[3].replace(' )', '')
        w_row[3] = w_row[3].replace(' ]', '')

        s1_sum += 0 if(row[2] == 'x' or row[2] == 'X') else int(row[2], 16)
        s2_sum += 0 if (row[3] == 'x' or row[3] == 'X') else int(row[3], 16)

        if row[1][3:5] == '00':
            s1_sum = 0
            s2_sum = 0

        if row[1][3:5] == '59':
            if s1_sum > 0 and w_row[3] != '///':
                s1.append(s1_sum)
                w1.append(float(w_row[3]))

            if s2_sum > 0 and w_row[3] != '///':
                s2.append(s2_sum)
                w2.append(float(w_row[3]))

            try:
                w_row = next(weather)
            except Exception as e:
                print('file out range. ', e)
                break

    infile.close()

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.scatter(s1, w1)
    ax1.set_title('first scatter plot')
    ax1.set_xlabel('sensor1')
    ax1.set_ylabel('weather')
    ax1.set_xlim(0,)
    ax1.set_ylim(-15, 40)
    # fig1.show()

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(s2, w2)
    ax2.set_title('first scatter plot')
    ax2.set_xlabel('sensor2')
    ax2.set_ylabel('weather')
    ax2.set_xlim(0,)
    ax2.set_ylim(-15, 40)
    # fig2.show()

    fig.tight_layout()
    plt.savefig("test.png")

weatherfile.close()
