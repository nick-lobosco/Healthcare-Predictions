from __future__ import print_function
import requests
import re
from bs4 import BeautifulSoup
import datetime


starttime = datetime.datetime.now()
#print(starttime)
Id='538C3F606586DF17'
"""
notStates = ['TX13', 'NJ13', 'MA13','FL13', 'AZ13']
states = []

r = requests.get('https://hcupnet-archive.ahrq.gov/HCUPnet.jsp?Id='+Id+'&Form=MAINSEL&JS=Y&Action=%3E%3ENext%3E%3E&_MAINSEL=County%20Level%20Statistics') #select county level stats
dbs = BeautifulSoup(r.text, 'html.parser').findAll('a', href=re.compile('DB='))
for db in dbs:
	dbString = str(db)
	if dbString[103:105] == '13' and dbString[101:105] not in notStates:
		states.append(dbString[101:105])

print(states)
"""
states = ['OK13', 'OR13', 'PA13', 'SC13', 'TN13', 'UT13', 'WA13', 'WV13', 'WI13', 'WY13']
count = 0
print(str(count) + ': ' + str(datetime.datetime.now()))

for state in states:
	r = requests.get('https://hcupnet-archive.ahrq.gov/HCUPnet.jsp?Id='+Id+'&Form=MAINSEL&JS=Y&Action=%3E%3ENext%3E%3E&_MAINSEL=County%20Level%20Statistics') #select county level stats
	db = BeautifulSoup(r.text, 'html.parser').find('a', href=re.compile('DB=' + state))
	f = open('./'+state+'Procedures.csv', 'w+')
	r = requests.get('https://hcupnet-archive.ahrq.gov/' + db.get('href'))
	r = requests.get('https://hcupnet-archive.ahrq.gov/HCUPnet.jsp?Id='+Id + '&Form=SelDXPR&JS=Y&Action=%3E%3ENext%3E%3E&_DXPR=PCCHPR1')
	opts = BeautifulSoup(r.text, 'html.parser').findAll('option', value=re.compile('\d+$'))
	for opt in opts:
		optText = opt.text
		i=0
		for c in optText:
			if(c.isalpha()):
				break
			else:
				i+=1
		optText = optText[i:]
		optText = optText.replace(',', '')
		o = opt.get('value')
		r = requests.post('https://hcupnet-archive.ahrq.gov/HCUPnet.jsp', { 'Form':'SelMAJDXPR', 'Id':Id,'JS':'Y','_PCCHPX1': o, '_SearchString': '', '_SearchMethod': 'Any', 'Go to the Next Screen.x': '21', 'Go to the Next Screen.y': '13'})
		r = requests.post('https://hcupnet-archive.ahrq.gov/HCUPnet.jsp', {'Form':'SelOUTC','Id':Id,'JS':'Y','_InOutcomes':'Yes','_Outcomes':'ADJ_IPS_RT','_Outcomes':'ADJ_IPD_RT','_Outcomes':'ADJ_CSTPERCAP', 'Go to the Next Screen.x': '55'
	,'Go to the Next Screen.y': '8'})
		r = requests.get('https://hcupnet-archive.ahrq.gov/HCUPnet.jsp?Id='+Id+'&Form=SelREGION&JS=Y&Action=%3E%3ENext%3E%3E&_REGION=No')
		counties = BeautifulSoup(r.text, 'html.parser').findAll('input', type='checkbox')
		x = 0
		for county in counties:
			if(x<2):
				x+=1
				continue
			r = requests.post('https://hcupnet-archive.ahrq.gov/HCUPnet.jsp', {'Form':'DispTab','Id':Id,'JS':'Y','_FIPSSTCO':county.get('value'),'Go to the Next Screen.x': '82', 'Go to the Next Screen.y': '17'})
			soup = BeautifulSoup(r.text, 'html.parser')
			x = soup.find('th', class_='tabtitle')
			location = re.search('(^.*?)\d', x.text).group(1)
			table = soup.find('table', summary=re.compile('CCS'))
			rows = table.findChildren(recursive=False)
			for row in rows:
				boole = False
				valid = False
				csvRow = location.encode('utf-8') + ', ' + str(2013) + ', ' + optText.encode('utf-8')
				entries = row.findChildren(recursive=False)
				for entry in entries:
					if(entry.text != 'Payer'): 
						e = entry.text.replace(',', '')
						try:
							float(e)
							valid = True
						except ValueError:
							pass
						csvRow += ', ' + e.encode('utf-8')
					if(entry.text in ('Medicare', 'Medicaid', 'Uninsured')):
							boole = True
				if(boole and valid):
					count += 1
					if(count%500 ==0):
						print(str(count) + ': ' + str(datetime.datetime.now()))
					print(csvRow, file=f)
	print(state + 'finished')
	f.close()

print(datetime.datetime.now())