# -*- coding: utf-8 -*-
"""
Created on Mon May 07 23:15:52 2018

@author: Charlotte
"""

import getFeatures
import numpy as np
import sklearn.preprocessing as preprocessing
from sklearn.decomposition import PCA
from sklearn import neighbors
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def getVecList(countyvecs,vecnumber,paymenttype):
    vectors=countyvecs[paymenttype]
    keylist=vectors.keys()
    keylist.sort()
    veclist=[]
    namelist=[]
    i=vecnumber
    for key in keylist:
        
        all4vecs=vectors[key]
        if i>=0:
            countvec=all4vecs[i]
        else:
            countvec=all4vecs
        veclist.append(countvec)
        namelist.append(key)
    veclist=np.asarray(veclist)
    return veclist

def BasicPCAGraphs(vecnumber):
    countyvecs,diagvecs,diagdict=getFeatures.getFeatures()
    pca= PCA(n_components=3)
    standardscaler=preprocessing.StandardScaler()
    
    veclist=getVecList(countyvecs,vecnumber,"Medicare")
    vecs=standardscaler.fit_transform(veclist)
    Medicareprincipalcomponents=pca.fit_transform(vecs)
    Medicarevar=pca.explained_variance_ratio_
    x1,y1,z1=Medicareprincipalcomponents.T
    
    veclist=getVecList(countyvecs,vecnumber,"Medicaid")
    vecs=standardscaler.fit_transform(veclist)
    Medicaidprincipalcomponents=pca.fit_transform(vecs)
    Medicaidvar=pca.explained_variance_ratio_
    x2,y2,z2=Medicaidprincipalcomponents.T
    
    veclist=getVecList(countyvecs,vecnumber,"Uninsured")
    vecs=standardscaler.fit_transform(veclist)
    Uninsuredprincipalcomponents=pca.fit_transform(vecs)
    Uninsuredvar=pca.explained_variance_ratio_
    x3,y3,z3=Uninsuredprincipalcomponents.T
    
    plt.plot(x1,y1, 'ro',x2,y2,'bo',x3,y3,'go')
    plt.title("PCA of Procedure Based Vectors, Colored By Payment Method")
    plt.show()
    
    diagveclist=getVecList(diagvecs,-1,"Medicare")
    vecs=standardscaler.fit_transform(diagveclist)
    Medicareprincipalcomponents=pca.fit_transform(vecs)
    Medicarevar=pca.explained_variance_ratio_
    x1,y1,z1=Medicareprincipalcomponents.T
    
    diagveclist=getVecList(diagvecs,-1,"Medicaid")
    vecs=standardscaler.fit_transform(diagveclist)
    Medicaidprincipalcomponents=pca.fit_transform(vecs)
    Medicaidvar=pca.explained_variance_ratio_
    x2,y2,z2=Medicaidprincipalcomponents.T
    
    diagveclist=getVecList(diagvecs,-1,"Uninsured")
    vecs=standardscaler.fit_transform(diagveclist)
    Uninsuredprincipalcomponents=pca.fit_transform(vecs)
    Uninsuredvar=pca.explained_variance_ratio_
    x3,y3,z3=Uninsuredprincipalcomponents.T
    plt.plot(x1,y1, 'ro',x2,y2,'bo',x3,y3,'go')
    plt.title("PCA of Diagnosis Based Vectors, Colored By Payment Method")

    plt.show()
    
def basicPredictor(vecnumber):
    procvec,diagvec,diagdict=getFeatures.getFeatures()
    procvec1=procvec["Medicare"]
    diagvec1=diagvec["Medicare"]
    procvec2=procvec["Medicaid"]
    diagvec2=diagvec["Medicaid"]
    procvec3=procvec["Uninsured"]
    diagvec3=diagvec["Uninsured"]
    keylist=procvec1.keys()
    keylist.sort()
    veclist=[]
    diaglist=[]
    statenamelist=[]
    i=vecnumber
    for key in keylist:
        vecs=procvec1[key]
        countvec=vecs[i]
        veclist.append(countvec)
        diaglist.append(diagvec1[key])
        
        try:
            veclist.append(procvec2[key][i])
            diaglist.append(diagvec2[key])
        except:
            pass
        try:
            veclist.append(procvec3[key][i])
            diaglist.append(diagvec3[key])
        except:
            pass
        
        statenamelist.append(key)
    veclist=np.asarray(veclist)
    diaglist=np.asarray(diaglist)
    '''
    #encodes only top 5 diagnoses for each input vector, does not give good accuracy!!
    diagindex=np.argpartition(diaglist,-5,axis=1)[:,-5:]
    hotlist=[]
    for i in range(len(diaglist)):
        hot=np.zeros((len(diaglist[0]),),dtype=float)
        hot[diagindex[i]]=1.0
        hotlist.append(hot)
    hotlist=np.asarray(hotlist)
    hotlist=preprocessing.normalize(hotlist)
    
    '''
    #print diagindex
    hotlist=preprocessing.normalize(diaglist)
    standardscaler=preprocessing.StandardScaler()
    vecs=standardscaler.fit_transform(veclist)
    
  #  for testing how size of training data affects accuracy
    sizevec=[0.11,0.22,0.33,0.44,0.55,0.66]
    error=[]
    for i in sizevec:
        xtrain,xtest,ytrain,ytest=train_test_split(vecs,hotlist,test_size=i,random_state=17)
        knn=neighbors.KNeighborsRegressor()
        knn.fit(xtrain,ytrain)
        predictedys=knn.score(xtest,ytest)
        error.append(predictedys)
    print error
    '''
    #encoding for topn diagnoses after making the predictions, best method!
    xtrain,xtest,ytrain,ytest=train_test_split(vecs,hotlist,test_size=0.11,random_state=17)
    knn=neighbors.KNeighborsRegressor()
    knn.fit(xtrain,ytrain)   
    predictedys=knn.predict(xtest)
    n=3
    topndiagnoses=np.argpartition(ytest,-n,axis=1)[:,-n:]
    topnpredicted=np.argpartition(predictedys,-n,axis=1)[:,-n:]
    numsamelist=[]
    correctdiagnoses=[]
    for i in range(len(topndiagnoses)):
        numsame=list(set(topndiagnoses[i]).intersection(topnpredicted[i]))
        subsetcorrect=[]
        for j in numsame:
            subsetcorrect.append(diagdict[j])
        correctdiagnoses.append(subsetcorrect)
        numsame=len(numsame)
        numsamelist.append(numsame)
    #print numsamelist
    samesum=np.sum(np.asarray(numsamelist))
    totalsum=len(topndiagnoses)*n
    error=float(samesum)/totalsum
    print correctdiagnoses
    print error
    '''

BasicPCAGraphs(0)
'''
BasicPCAGraphs(2)
BasicPCAGraphs(3)
'''
#basicPredictor(0)