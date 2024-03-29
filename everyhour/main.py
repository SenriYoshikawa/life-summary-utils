import sys
import csv

for i in range(1, len(sys.argv)) :
    infile = open(sys.argv[i], 'r')
    outfile = open(sys.argv[i][0:-4] + "_h.csv", 'w')

    reader = csv.reader(infile)
    writer = csv.writer(outfile, lineterminator='\n')

    s1 = s2 = 0;
    date = "";

    for row in reader:
        if len(row) > 2:
            s1 += 0 if(row[2] == 'x' or row[2] == 'X') else int(row[2], 16)
        if len(row) > 3:
            s2 += 0 if(row[3] == 'x' or row[3] == 'X') else int(row[3], 16)

        if row[1][3:5] == "00":
            date = row[1]

        if row[1][3:5] == "59":
            writer.writerow([row[0], date, s1, s2])
            s1 = s2 = 0

    infile.close()
    outfile.close()
