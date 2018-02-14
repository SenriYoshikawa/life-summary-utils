import csv
import sys
import pandas as pd
import numpy as np


def data_load(data_file, call_file):
    df1 = pd.read_csv(data_file, header=None, names=['date', 'time', 'sensor1', 'sensor3', 'label'])
    df2 = pd.read_csv(call_file, header=1)
    data_np = np.array(df1)
    call_np = np.array(df2)
    return [data_np, call_np]


def _main():
    label = ['不在','在室','来客']
    if len(sys.argv) > 1 and sys.argv[1].find('csv') == -1:
        sys.argv.extend(glob.glob(sys.argv[1] + '*.csv'))
        del sys.argv[1]

    data_list, call_list = data_load(sys.argv[1], sys.argv[2])
    outfile = open(sys.argv[1][:-4] + "-check-result.csv", 'w')

    count = 0
    collect = 0
    for call_row in call_list[call_list[:,2] == '不在']:
        data_row = data_list[(data_list[:, 0] == call_row[0]) & (data_list[:, 1] == call_row[1])]
        outfile.write(call_row[0] + ',' + call_row[1] + ',不在,')
        #print(len(data_row))
        if len(data_row) == 1:
            data_row = data_row[0]
            outfile.write(data_row[0] + ',' + data_row[1] + ',' + str(int(data_row[2])) + ',' + str(int(data_row[3]))
                          + ',' + label[int(data_row[4])+1] + ',')
            count += 1
            if int(data_row[4]) == -1:
                outfile.write('1\n')
                collect += 1
            else:
                outfile.write('0\n')
        else:
            outfile.write('\n')

    print('accuracy = ' + str(collect / count))
    outfile.write('accuracy = ' + str(collect / count))
    outfile.close()

if __name__ == '__main__':
    _main()
