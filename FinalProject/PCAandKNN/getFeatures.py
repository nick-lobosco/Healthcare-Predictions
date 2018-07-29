# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 21:37:02 2018

@author: Charlotte
"""
'''
#for the medicare data!
[u'National Provider Identifier', 
u'Last Name/Organization Name of the Provider', 
u'First Name of the Provider',
 u'Middle Initial of the Provider', 
 u'Credentials of the Provider',
 u'Gender of the Provider',
 u'Entity Type of the Provider',
 u'Street Address 1 of the Provider',
 u'Street Address 2 of the Provider',
 u'City of the Provider',
 u'Zip Code of the Provider', 
 u'State Code of the Provider',
 u'Country Code of the Provider',
 u'Provider Type',
 u'Medicare Participation Indicator',
 u'Place of Service',
 u'HCPCS Code',
 u'HCPCS Description',
 u'HCPCS Drug Indicator',
 u'Number of Services', 
 u'Number of Medicare Beneficiaries',
 u'Number of Distinct Medicare Beneficiary/Per Day Services',
 u'Average Medicare Allowed Amount',
 u'Average Submitted Charge Amount',
 u'Average Medicare Payment Amount', 
 u'Average Medicare Standardized Amount']

#for the hcup data!!
['county','state','year','procedure','insurance','*total number of discharges','rate of discharges 100000',
'*mean length of stay','*aggregate number of days','number of inpatient days','*mean cost',
'*aggregate costs for all hospital stays','costs for inpatient stays per capita','countynumber']


def codeToDescription(infolist):
    cptcodes=[]
    codedict={}
    numberdict={}
    #create dictionary of descriptions with value as list of codes
    #take each list of codes, and create another dictionary 
    for i in infolist:
        desc=i[3]
        cptcodes.append(desc)
    cptcodes=set(cptcodes)
    for i in cptcodes:
        codedict[i]=[]
    for i in infolist:
        desc=i[3]
        cpt=i[2]
        alist=codedict[desc]
        alist.append(cpt)
        alist=list(set(alist))
        codedict[desc]=alist
    codetocodemap={}
    #dictionary of each code to its final code
    for key,value in codedict.iteritems():
        chosencode=value[0]
        for i in value:
            codetocodemap[i]=chosencode
    allcodes=[]
    for i in infolist:
        i[2]=codetocodemap[i[2]]
        allcodes.append(i[2])
    allcodes=list(set(allcodes))
    descdict={}
    for i in allcodes:
        descdict[i]=[]
    for i in infolist:
        desc=i[3]
        cpt=i[2]
        desclist=descdict[cpt]
        desclist.append(desc)
        desclist2=list(set(desclist))

        descdict[cpt]=desclist2
    sorted_d=sorted(descdict.items(),key=operator.itemgetter(0))


'''

from pyspark import SparkContext, SparkConf
import pandas as pd
import operator
import numpy as np
#import plotly.plotly as py
'''
conf=SparkConf().setAppName('MedicareSpark')
sc=SparkContext(conf=conf)
data=sc.textFile("Medicare_PUF_CY2015.csv")
data2=sc.textFile("caliProcedures.csv")
split=data.map(lambda x: x.split(","))
'''
'''
#use to see how many inputs for each state. notice that because of off by one, the number of 
#states if way above the actual #! (lists 34696 unique values in state column)
juststates=split.map(lambda x: (x[11])).map(lambda c: (c,1)).reduceByKey(lambda a,b: a+b)
countofstates=juststates.count()
#print countofstates 34696
top50=juststates.takeOrdered(60,lambda(key,value):-1*value)

'''

#
'''
#to do: 
   #create seperate mapping of hcpcs code to description just for own personal use?
'''


    
zipfile='zip2countyName.csv'
zips=[]
ziptocountyname={}
ziptocountycode={}
with open(zipfile) as f:
    ziplines=f.readlines()
for i in ziplines:
    line=i.split(',')
    zips.append(line[0])
    ziptocountyname[line[0]]=line[1]
zips=set(zips)
zipfile='zip2countyCode.csv'
with open(zipfile) as f:
    ziplines=f.readlines()
for i in ziplines:
    i=i.strip('\n')
    line=i.split(',')
    zipcode=line[0]
    ziptocountycode[zipcode]=line[1]
    
def zipcodematch(x):
    #if zipcode matches an actual zip code, output 1, else output 0
    zipcode=x
   # print zipcode
    if(zipcode in zips):
       # print 'match'
        return (ziptocountycode[zipcode],ziptocountyname[zipcode])
    else:
        return 0,0
def basicInfo(): 
    medicarefile="Medicare_PUF_CY2015.csv"
    f=open(medicarefile)
    medicarelines=[]
    for i in range(10000):
        line=f.readline()
        medicarelines.append(line)
    f.close()
    eachrow=[]
    allcodes=set([])
    print medicarelines[:5]
    for row in medicarelines:
        row=row.split(',')
        zipcode=row[10]
        state=row[11]
        zipcode=zipcode[0:5]
        countycode,countyname=zipcodematch(zipcode)
        cptcode=row[16]
        description=row[17].lower()
        cost=row[24]
        if (countyname!=0):
            if(len(cptcode)==5):
                atuple=[countycode,countyname,state,cptcode,description,cost]
                allcodes.add(cptcode)
                eachrow.append(atuple)
    return eachrow, allcodes

def getcpttoccsdict(cptcodes,boundslist):
    cpttoccsdict={}
    for i in cptcodes:
        blank=True
        j=0
        while(blank):
           # print boundslist[j]
            if(i>=boundslist[j][0]):
                if(i<=boundslist[j][1]):
                    cpttoccsdict[i]=boundslist[j][2]
                    blank=False
                else:
                        j+=1
            else:
                j+=1
            if(j>=len(boundslist)):
                blank=False
    return cpttoccsdict
                
def cptToDescription():
    return 0


def cptToCSS(infolist,mapper):
    for i in infolist:
        ccs=0
        if i[2] in mapper:
            ccs=mapper[i[2]]
        i[2]=ccs
    return infolist
            
def combineProcedure(infolist,countyset):
    dictoftuples={}
    for i in countyset:
        dictoftuples[i]=np.zeros((245,),dtype=int)
    for i in infolist:
        county=i[0]
        array=dictoftuples[county]
        ccscode=i[2]
        array[ccscode]+=1
        dictoftuples[county]=array

    return dictoftuples
    
    
def ccsFileParser():
    filename="2018_ccs_services_procedures.csv"
    f=open(filename)
    lines=f.readlines()
    boundslist=[]
    codetoname={}
    for i in lines:
        #dont want to split the actual procedure name which could contain , or ;
        i=i.split(',')
        numberstring=i[0]
        actualcode=int(i[1])

        if actualcode not in codetoname:
            description=i[2]
            if len(i)>3:
                stringparts=i[2:]
                description=''.join(stringparts)
            description=description.strip('\n')
            description=description.strip('"')
            codetoname[actualcode]=description

        lowerbound=numberstring[1:6]
        upperbound=numberstring[7:12]
        listtuple=[lowerbound,upperbound,actualcode]
        boundslist.append(listtuple)

    return boundslist,codetoname
    
def countCounties(infolist):
    counties=[]
    for i in infolist:
        counties.append(i[0])
    counties=set(counties)
    return counties
def mapdescriptiontocodeCCS(description,ccsdict):
    description=description.split(',')
    description=description[0]
    for i in ccsdict:
        if ccsdict[i]==description:
            return i
    return 0
def ccsDescriptiontoCode(ccsdict):
    desctocode={}
    for k,v in ccsdict.items():
        desctocode[v]=k
    return desctocode
                  
                  
def getHCUPvector(hcuparray):
    insurancedicts={}
    insurancedicts["Medicare"]={}
    insurancedicts["Medicaid"]={}
    insurancedicts["Uninsured"]={}
    for x in hcuparray:
        county=x[1]
        insurance=x[0]
        if county not in insurancedicts[insurance]:
            #codearray=np.zeros((245,),dtype=int)
            #codearray[ccscode]+=1
            #insurancedicts[insurance][county]=codearray
            infolist=[]
            infolist.append(x[2:])

            insurancedicts[insurance][county]=infolist
        else:
            infolist=insurancedicts[insurance][county]
            infolist.append(x[2:])
            insurancedicts[insurance][county]=infolist
    return insurancedicts
def combinebycountyHCUP(insurancedicts,Procedure):
    insurancedicttocountydict={}

    for k in insurancedicts.items():
        j=k[0] #this is a key
        insurancedicttocountydict[j]={}
        #for the dictionaries 
        for county in insurancedicts[j].items():
            countylist=insurancedicts[j][county[0]] #get county key
            if(Procedure):
                arr=np.zeros((4,245),dtype=int)
                for procedurerow in countylist:
                    #if you want to go by averages instead change 3 to 2 and 5 to 4
                    procedurecode=procedurerow[0]
                    procedurecount=procedurerow[1]
                    procedureduration=procedurerow[3]
                    procedurecost=procedurerow[5]
                    arr[0][procedurecode]=procedurecount
                    arr[2][procedurecode]=procedureduration
                    arr[3][procedurecode]=procedurecost
                    arr[1][procedurecode]=procedurecount
            else:
                arr=np.zeros((206,))
                for diagnosesrow in countylist:
                    diagnosesindex=diagnosesrow[0]
                    diagnosescount=diagnosesrow[1]
                    try:
                        diagnosescount=float(diagnosescount)
                    except:
                        diagnosescount=0
                    arr[diagnosesindex]=diagnosescount
            insurancedicttocountydict[j][county[0]]=arr
    return insurancedicttocountydict
def combineToState(insdictcountdict):
    insdict={}
    for k in insdictcountdict.items():
        k=k[0]
        statedict={}
        for county in insdictcountdict[k].items():
            county=county[0]
            state=county[0:2]
            if state not in statedict:
                statedict[state]=insdictcountdict[k][county]
            else:
                arr=statedict[state]
                addarr=insdictcountdict[k][county]
         #       print np.shape(arr), np.shape(addarr)
                arr=np.add(arr,addarr)
                statedict[state]=arr
        insdict[k]=statedict
    return insdict
def addExtraHCUPFeaturesCounty(insdictcountdict,filename):
    f=open(filename)
    lines=f.readlines()
    countydict={}
    numadd=0
    for i in lines:
        i=i.strip()
        i=i.split(',')
        county=i[0]
        if len(county)==4:
            county='0'+county
        rest=i[1:]
        numadd=len(rest)
        newdata=np.asarray(i[1:],dtype=float)
        
        countydict[county]=newdata

    for k in insdictcountdict.items():
        k=k[0]
        
        for county in insdictcountdict[k].items():
            county=county[0]
            arr=insdictcountdict[k][county]
            numberofvecs=len(arr)
            try:
                newarr=countydict[county]
                updatearr=np.empty((numberofvecs,numadd+len(arr[0])))
                for m in range(numberofvecs):
                    updatearr[m]=np.append(arr[m],newarr)
                insdictcountdict[k][county]=updatearr
            except:
                insdictcountdict[k].pop(county)
    return insdictcountdict

def getFractionalElementsHCUP(insdictcountdict):
    for k in insdictcountdict.items():
        k=k[0]
        for county in insdictcountdict[k].items():
            county=county[0]
            arr=insdictcountdict[k][county]
            fillvec=np.zeros(len(arr[1],),dtype=float)
            totalcount=np.sum(arr[1])
            fillvec.fill(totalcount)
            arr=arr.astype(float)
            arr[1]=np.divide(arr[1],fillvec)
            totalduration=np.sum(arr[2])
            fillvec.fill(totalduration)
            arr[2]=np.divide(arr[2],fillvec)
            totalcost=np.sum(arr[3])
            fillvec.fill(totalcost)
            arr[3]=np.divide(arr[3],fillvec)
            insdictcountdict[k][county]=arr
    return insdictcountdict
def readHCUPfiles(filename,ccsdict):
    f=open(filename)
    lines=f.readlines()
    hcuplines=[]
    for i in lines:
        i=i.split(',')  
        countycode=i[13].strip('\n')
        insurance=i[4].strip()
        procedure=(i[3].strip())
        discharge=float(i[5].strip())
        LOS=float(i[7].strip())
        aggdays=float(i[8].strip())
        cost=float(i[10].strip())
        aggcost=float(i[11].strip())
        ccscode=ccsdict[procedure]
        onevec=[insurance,countycode,ccscode,discharge,LOS,aggdays,cost,aggcost]
        hcuplines.append(onevec)

    return hcuplines
def getHCUPDiaglines(filename):
    f=open(filename)
    lines=f.readlines()
    diagnoses=[]
    hcuplines=[]
    for i in lines:
        i=i.split(',')
        diag=i[3].strip()
        diagnoses.append(diag)
    diagnoses=list(set(diagnoses))
    diagnoses.sort()
    diagdict={}
    for i in range(len(diagnoses)):
        key=diagnoses[i]
        value=i
        diagdict[key]=value   
    for i in lines:
        i=i.split(',')  
        countycode=i[13].strip('\n')
        insurance=i[4].strip()
        diag=i[3].strip()
        #creates dictionary of description to code
        diagindex=diagdict[diag]
        count=i[5].strip()
        onevec=[insurance,countycode,diagindex,count]
        hcuplines.append(onevec)
    invdict={v: k for k,v in diagdict.iteritems()}
    return hcuplines, invdict
#read in by state and get feature vectors, how to evaluate cost? 
def getFeatures():       
    boundslist,ccscodetonamedict=ccsFileParser()
    ccsdesctocodedict=ccsDescriptiontoCode(ccscodetonamedict)
    hcuplines=readHCUPfiles("combined.csv",ccsdesctocodedict)
    insurancedicts=getHCUPvector(hcuplines)
    inscountdict=combinebycountyHCUP(insurancedicts,True)
    diaglines,diagdict=getHCUPDiaglines('combinedD.csv')
    diaginsurancedicts=getHCUPvector(diaglines)
    diagcountdict=combinebycountyHCUP(diaginsurancedicts,False)
    addedcountyvecs=addExtraHCUPFeaturesCounty(inscountdict,'incomeOutput.csv')
    addedcountyvecs2=addExtraHCUPFeaturesCounty(addedcountyvecs,'formattedPopInfo.csv')
    #addedcountyvecs2=inscountdict
    return addedcountyvecs2,diagcountdict,diagdict
    #statevecs=combineToState(inscountdict)
    #return statevecs
def PCAgetFeatures():
    return 0
#d=getFeatures()
#print statevecs
#hcupfractionvecs=getFractionalElementsHCUP(inscountdict)
#print hcupfractionvecs
#gives procedures as fractions of 
#allinfo,cptcodes=basicInfo()
#countyset=countCounties(allinfo)

'''
mapper=getcpttoccsdict(cptcodes,boundslist)
converted=cptToCSS(allinfo,mapper)
dictwithcount=combineProcedure(converted,countyset)
'''
#print insurancedicts

