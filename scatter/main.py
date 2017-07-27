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

    s1 = s2 = w1 = w2 = []

    #print(s_row[0] + " " + s_row[1] + " " + w_row[0] + " " + w_row[1])

    while s_row[0] != w_row[0]:
        w_row = next(weather)

        #print(s_row[0] + " " + s_row[1] + " " + w_row[0] + " " + w_row[1])

    infile.seek(0)
    for row in reader:
        w_row[3] = w_row[3].replace(' )', '')
        w_row[3] = w_row[3].replace(' ]', '')
        #print(w_row[0] + " " + w_row[1] + " " + w_row[3])
        if len(row) > 2 and w_row[3] != "///":
            if row[2] == '0' or row[2] == 'x' or row[2] == 'X':
                continue
            s1.append(0 if(row[2] == 'x' or row[2] == 'X') else int(row[2], 16))
            w1.append(float(w_row[3]))
            print(row[2] + " " + w_row[3])
        if len(row) > 3 and w_row[3] != "///":
            if row[3] == '0' or row[3] == 'x' or row[3] == 'X':
                continue
            s2.append(0 if(row[3] == 'x' or row[3] == 'X') else int(row[3], 16))
            w2.append(float(w_row[3]))
        try:
            w_row = next(weather)
        except:
            break
    infile.close()

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.scatter(s1, w1)
    ax1.set_title('first scatter plot')
    ax1.set_xlabel('sensor1')
    ax1.set_ylabel('weather')
    #fig1.show()

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(s2, w2)
    ax2.set_title('first scatter plot')
    ax2.set_xlabel('sensor2')
    ax2.set_ylabel('weather')
    #fig2.show()

    plt.savefig("test.png")

weatherfile.close()
