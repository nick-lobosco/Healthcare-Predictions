from __future__ import print_function

files = ['AR13', 'AZ13', 'CA13', 'FL13', 'HI13', 'IA13', 'IL13', 'IN13','KY13', 'LA13', 'MA13', 'MD13','MI13','MN13','NC13','ND13', 'NJ13','NV13','OK13','OR13','PA13','SC13','TN13', 'TX13', 'UT13', 'WA13', 'WI13', 'WV13', 'WY13']
states = {}
name2code = {}
output = open('combined.csv', 'w+')


#get states to abbreviations mapping
stateFile = open('../Visualizations/states.txt', 'r')
lines = stateFile.readlines()
for line in lines:
	line = line.split('\t')
	states[line[0]] = line[1].strip()
stateFile.close()

#get (name, state) to county code mapping
counties = open('../Visualizations/counties.txt', 'r')
lines = counties.readlines()
for line in lines:
	splitLine = line.split()
	county = splitLine[1]
	for x in range(len(splitLine)-3):
		county += ' '+ splitLine[2+x]
	tup = (county, splitLine[len(splitLine) - 1])
	name2code[tup] = splitLine[0]
counties.close()

for file in files:
	lines = open(file + 'Procedures.csv').readlines()
	for line in lines:
		split = line.split(',')
		tup = (split[0], states[split[1].strip()])
		try:
			line = line.strip() + ',' + name2code[tup]
			print(line, file=output)
		except:
			pass

