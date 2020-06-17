#!/usr/bin/env python3

from argparse import ArgumentParser
import csv
from datetime import datetime
import subprocess

parser = ArgumentParser()
parser.add_argument('path', help='CSV file with data')
parser.add_argument('--week', action='store_true', help='Only include data from the last 7 days')
parser.add_argument('--morning', action='store_true', help='Only include data from mornings')
args = parser.parse_args()

now = datetime.now()

with open('plot.dat', 'w') as fout:
    with open(args.path, newline='') as fin:
        r = csv.reader(fin)

        ready = False

        for l in r:
            # Skip initial non-data rows
            if not ready:
                if len(l) > 0 and l[0] == 'Date':
                    ready = True

                continue

            date = datetime.strptime(l[0] + " " + l[1], '%m/%d/%Y %I:%M %p')
            datefmt = datetime.strftime(date, '%Y-%m-%d %H:%M')
            weight = l[2]

            if args.morning and date.hour >= 10:
                continue

            if args.week and (now - date).days > 7:
                continue

            fout.write(datefmt + "\t" + weight + "\n")

with open('plot.gnu', 'w') as f:
    f.write('set xdata time\n')
    f.write('set timefmt "%Y-%m-%d %H:%M"\n')
    #f.write('set format x "%y-%m"\n')
    f.write('set format x "%d/%m"\n')

    f.write('set ylabel "Weight (kg)"\n')

    f.write('set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"\n')
    f.write('set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"\n')

    f.write('set term svg\n')
    f.write('set output "plot.svg"\n')

    f.write('plot "plot.dat" using 1:3 w lines lw 2 title "Data"\n')

subprocess.run(["gnuplot", "plot.gnu"], check=True)
subprocess.run(["open", "-a", "Google Chrome", "plot.svg"], check=True)
