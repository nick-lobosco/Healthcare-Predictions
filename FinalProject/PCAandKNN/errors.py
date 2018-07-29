# -*- coding: utf-8 -*-
"""
Created on Tue May 08 09:40:55 2018

@author: Charlotte
"""

import matplotlib.pyplot as plt


#for raw diagnoses vectors
sizevec=[0.89,0.78,0.67,0.56,0.45,0.34]
combinedaccuracycount=[0.66396736454821459, 0.67018855928452192, 0.66961137859572561, 0.64602967650584009, 0.62179818706556433, 0.61191377075671127]
#only counts
medicareacc=[0.09148828686138212, 0.11259683934840925, 0.12876317189102482, 0.090271827292939685, 0.080537717232057257, 0.057518081594828102]
medicaidacc=[0.08576666962060886, 0.12164672557570995, 0.097119040601213041, 0.10178368113497768, 0.10627661922568016, 0.089177161055565043]
uninsuredacc=[0.31248807529567058, 0.094219035349243904, 0.087843181609417759, 0.12780847439448847, 0.089176859690944299, 0.13370731037240666]
#only duration
[0.63848760339582666, 0.65597981808925043, 0.6502138282348604, 0.62965296215641231, 0.6112600688438049, 0.59553055887987238]

#only cost
[0.63207164242870706, 0.63889241906055261, 0.64565230519253558, 0.61974670075669747, 0.58485924135954637, 0.57850851224459554]

plt.plot(sizevec,combinedaccuracycount,'o',sizevec,medicareacc,'r--',sizevec,medicaidacc,'b--',sizevec,uninsuredacc,'g--')
plt.ylabel('Accuracy of KNN Regression')
plt.xlabel('fraction of data used for training')
plt.title('KNN Accuracy for Prediction of Diagnoses by Amount of Data and Payment Type')
plt.show()
#when testing on 0.11 of data
topn=[1,2,3,4,5,10]
topnaccuracy=[0.63,0.58,0.603,0.64125,0.639,0.668]

plt.plot(topn,topnaccuracy,'bo')
plt.xlabel('Size of Top Diagnoses Set')
plt.ylabel('Accuracy in Predicting Top Diagnoses')
plt.title('Prediction Accuracy for Combined Payment Methods on 11% of Data')
plt.show()
