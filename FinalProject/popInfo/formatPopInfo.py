from __future__ import print_function

lines = open('countyPopInfo.csv', 'r').readlines()
output = open('formattedPopInfo.csv', 'w+')
fipsdict = {}
for line in lines:
	split = line.split(',')
	fips = split[1]+split[2]
	age = split[7]
	pop = int(split[9].strip())
	if fips in fipsdict:
		#print(int(age)-1)
		fipsdict[fips][int(age)-1] += pop
	else:
		fipsdict[fips] = []
		for x in range(18):
			fipsdict[fips].append(0)
		fipsdict[fips][int(age)-1] = pop

for fips, arr in fipsdict.iteritems():
	l = str(arr[0])
	for x in range(1,18):
		l+=','+ str(arr[x])
	print(fips + ',' + l, file=output)



"""
ages = ['0', '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
for fips, agedict in fipsdict.iteritems():
	for age, pop in agedict.iteritems():
		print(fips + ',' + age + ',' + str(pop), file=output)
"""

"""
lines = open('countyPopInfo.csv', 'r').readlines()
output = open('formattedPopInfo.csv', 'w+')
fipsdict = {}
for line in lines:
	split = line.split(',')
	fips = split[1]+split[2]
	age = split[7]
	pop = int(split[9].strip())
	if fips in fipsdict:
		if age in fipsdict[fips]:
			fipsdict[fips][age] += pop
		else:
			fipsdict[fips][age] = pop
	else:
		fipsdict[fips] = {}
		fipsdict[fips][age] = pop

ages = ['0', '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
for fips, agedict in fipsdict.iteritems():
	for age, pop in agedict.iteritems():
		print(fips + ',' + age + ',' + str(pop), file=output)

"""
