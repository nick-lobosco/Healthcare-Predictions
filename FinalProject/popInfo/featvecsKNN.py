from __future__ import print_function
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.nan)

output = open('abc', 'w+')
arraySize = 1116

#make county code to diagnoses mapping
#lines = open('combinedProcedures.csv', 'r').readlines()

lines = open('combinedDiagnoses.csv', 'r').readlines()
statedict = {}
for line in lines:
	split = line.split(',')
	state = split[13].strip()
	procedure = split[3].strip()
	try:
		value = int(split[5].strip())
	except:
		continue
	if state in statedict:
		proceduredict = statedict[state]
		if procedure in proceduredict:
			proceduredict[procedure] += value
		else:
			proceduredict[procedure] = value
	else:
		proceduredict = {}
		proceduredict[procedure] = value
		statedict[state] = proceduredict

sortedDict = {}
for state, proceduredict in statedict.iteritems():
	sortd = sorted(proceduredict.items(), key=itemgetter(1))
	sortd.reverse()
	procs = []
	rng = 5
	if len(sortd) < 5:
		rng = len(sortd)
	for x in range(rng):
		procs.append(sortd[x][0])
	sortedDict[state] = procs

#make feature vectors
countyDict = {}
file = open('countyPopInfo.csv', 'r')
lines = file.readlines()
for line in lines:
	split = line.split(',')
	fips = split[1].strip() + split[2].strip()
	if fips not in sortedDict:
		continue
	sex = int(split[5].strip()) - 1
	age = int(split[7].strip()) -1
	race = int(split[8].strip()) - 1
	pop = int(split[9].strip())
	index = 558*sex + 31*age + race
	if fips in countyDict:
		countyDict[fips][index] = pop
	else:
		countyDict[fips] = np.zeros(arraySize)



accuracies = []
for trainingSize in range(2,10):	
	#split vectors into training/test vectors
	count = 0
	training = {}
	test = {}
	for key, arr in countyDict.iteritems():
		if count%trainingSize == 0:
			test[key] = arr
		else:
			training[key] = arr
		count+=1

	acc = 0
	count = 0
	for testKey, testArr in test.iteritems():
		dist = []
		for trainingKey, trainingArr in training.iteritems():
			dist.append((trainingKey, np.linalg.norm(testArr-trainingArr)))
		s = sorted(dist,key=itemgetter(1)) 
		keys = s[0:5]
		top = {}
		for a in range(5):
			if(len(keys) <= a):
				break
			for b in range(5):
				if len(sortedDict[keys[a][0]]) <= b:
					break
				diag = sortedDict[keys[a][0]][b]
				try:
					top[diag] += 1
				except:
					top[diag] = 1 
		sortedTop = sorted(top.items(), key=itemgetter(1))
		sortedTop.reverse()
		top3 = sortedTop[0:3]
		for diagnosis in top3:
			if diagnosis[0] in sortedDict[testKey]:
				acc+=1
			count+=1

	accuracies.append((float(acc)/count))
print(accuracies)

l = []
for x in range(2,10):
	l.append(1-(1.0/x))
plt.plot(l, accuracies, 'ro')
plt.axis([.5, 1, .8, 1])
plt.xlabel('Amount of Data Used For Training')
plt.ylabel('Accuracy')
plt.show()
