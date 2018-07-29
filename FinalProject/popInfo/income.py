from __future__ import print_function
import csv

file = open('incomeData.csv', 'r')
reader = csv.reader(file, dialect='excel')
output = open('incomeOutput.csv', 'w+')

first = True
for row in reader:
	if first:
		print(row[0][3:] + row[1] + ',' + row[22].replace(',',''), file=output)
		first = False
	else:
		print(row[0] + row[1] + ',' + row[22].replace(',',''), file=output)


"""
first = True
for line in file.readlines():
	if first:
		split = line.strip()[3:].split(',')
		first = False
	else:
		split = line.strip().split(',')
	print(split[22])
	break
"""