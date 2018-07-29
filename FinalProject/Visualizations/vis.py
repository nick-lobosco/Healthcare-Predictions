from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import statistics

categories = ['County', 'State', 'Year', 'Procedure', 'Total number of discharges', 'Rate of Discharges per 100000 population', 'Mean length of stay days', 'Aggregate number of days in the hospital', 'Number of inpatient days per 100000 population', 'Mean cost per stay', 'Aggregate costs for all hospital stays', 'Costs for inpatient stays per capita']
files = ['AR13', 'AZ13', 'CA13', 'FL13', 'HI13', 'IA13', 'IL13', 'IN13','KY13', 'LA13', 'MA13', 'MD13','MI13','MN13','NC13','ND13', 'NJ13','NV13','OK13','OR13','PA13','SC13','TN13', 'TX13', 'UT13', 'WA13', 'WI13', 'WV13', 'WY13']
states = {}
name2code = {}

#get states to abbreviations mapping
stateFile = open('states.txt', 'r')
lines = stateFile.readlines()
for line in lines:
	line = line.split('\t')
	states[line[0]] = line[1].strip()
stateFile.close()

#get (name, state) to county code mapping
counties = open('counties.txt', 'r')
lines = counties.readlines()
for line in lines:
	splitLine = line.split()
	county = splitLine[1]
	for x in range(len(splitLine)-3):
		county += ' '+ splitLine[2+x]
	tup = (county, splitLine[len(splitLine) - 1])
	name2code[tup] = splitLine[0]
counties.close()

#create csv for each Procedure category
for x in range(4, len(categories)):
	totalDict = {}
	countDict = {}
	code2val = {}
	avgDict = {}
	vals = []
	for file in files:
		Procedures = open('../Procedures/'+file+'Procedures.csv').readlines()
		for line in Procedures:
			split = line.split(',')
			tup = (split[0], states[split[1].strip()])
			try:
				val = float(split[x])
			except:
				continue
			try:
				totalDict[tup] += val
			except:
				totalDict[tup] = val
			try:
				countDict[tup] += 1
			except:
				countDict[tup] = 1

	for key,val in totalDict.iteritems():
		try:
			newKey = name2code[key]
		except:
			continue
		code2val[newKey] = val/countDict[key]
		avgDict[key] = val/countDict[key]
		vals.append(val/countDict[key])

	mapping = open('./procedureMappings/' + categories[x] + '.csv', 'w+')
	print('"state_code","county_code","value"', file=mapping)
	for key, val in code2val.iteritems():
		print(key[0:2] + ',' + key[2:] + ',' + str(val), file=mapping)
	mapping.close()

"""
#create csv for each diagnoses category
for x in range(4, len(categories)):
	totalDict = {}
	countDict = {}
	code2val = {}
	avgDict = {}
	vals = []
	for file in files:
		Diagnoses = open('../Diagnoses/'+file+'Diagnoses.csv').readlines()
		for line in Diagnoses:
			split = line.split(',')
			tup = (split[0], states[split[1].strip()])
			try:
				val = float(split[x])
			except:
				continue
			try:
				totalDict[tup] += val
			except:
				totalDict[tup] = val
			try:
				countDict[tup] += 1
			except:
				countDict[tup] = 1

	for key,val in totalDict.iteritems():
		try:
			newKey = name2code[key]
		except:
			continue
		code2val[newKey] = val/countDict[key]
		avgDict[key] = val/countDict[key]
		vals.append(val/countDict[key])

	mapping = open('./diagnosesMappings/' + categories[x] + '.csv', 'w+')
	print('"state_code","county_code","value"', file=mapping)
	for key, val in code2val.iteritems():
		print(key[0:2] + ',' + key[2:] + ',' + str(val), file=mapping)
	mapping.close()
"""