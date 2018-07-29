from __future__ import print_function
import operator

lines = open('combined.csv', 'r').readlines()
output = open('outliersOutput.txt', 'w+')
statedict = {}
for line in lines:
	split = line.split(',')
	state = split[1].strip()
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
	sortd = sorted(proceduredict.items(), key=operator.itemgetter(1))
	sortd.reverse()
	procs = []
	#print(sortd[0][0])
	for x in range(1):
		procs.append(sortd[x][0])
	sortedDict[state] = procs

#print(sortedDict, file=output)
for state, procedures in sortedDict.iteritems():
	for procedure in procedures:
		count = 1
		for iterstate, iterprocs in sortedDict.iteritems():
			if(iterstate != state and procedure in iterprocs):
				count +=1
			if(count==4):
				break
		else:
			print(state + ': ' + procedure+'(' + str(count) + ')')

#find diagnoses/procedures present in all states
arr = []
for state, procedures in sortedDict.iteritems():
	for procedure in procedures:
		for iterstate, iterprocs in sortedDict.iteritems():
			if(procedure not in iterprocs):
				break
		else:
			if(procedure not in arr):
				arr.append(procedure)
print(arr)
"""
	print('Top 5 for ' + state + ':')
	for x in range(5):
		if(sortd[x][0] != 'Circumcision' and sortd[x][0] != 'Cesarean section' and sortd[x][0]!= 'Arthroplasty knee' and sortd[x][0]!= 'Percutaneous coronary angioplasty (PTCA)' and sortd[x][0]!='Hip replacement total and partial' and sortd[x][0] != 'Hip replacement total and partial' and sortd[x][0] != 'Cholecystectomy and common duct exploration'):
			print(sortd[x])
	print('\n')
	#print(sortd[0:5])
#print(statedict.values())
#print(statedict, file=output)
"""
