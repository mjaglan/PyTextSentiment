# -*- coding: utf-8 -*-
import os

# create a vector
import numpy as np

# get data from csv
import csv

import numpy as np
import Utility

# for clean console output, let's suppress them for now.
import warnings
warnings.filterwarnings("ignore")

from sklearn import cross_validation, metrics


"""
NOTE: Avoid multiple inheritance at all costs, as it can grow too complex to be reliable.
"""
class UnSupervisedInfrastructure:
    def __init__(self):
        self.aBasePath = os.getcwd()
        self.globalCSVDataStorePath = self.aBasePath+"/../TextSentiment.V1.b/twitterData/myJsonOutput.csv"
        try:
            self.fileTrainingDataSet=open(self.globalCSVDataStorePath)
        except:
            self.fileTrainingDataSet = None

    inputList=[]
    tweetVectorList=[]
    noOfCluster=9   # (8+1 clusters)
    vectorKeyList=['anger', 'anticipation', 'disgust', 'enjoyment', 'fear', 'sad', 'surprise', 'trust']
    annotatedVector=[]

    def readFile(self, filePointer=None):
        if filePointer is None:
            filePointer = self.fileTrainingDataSet

        try:
            count=0
            for line in filePointer:
                if count==0:
                    count+=1
                    continue
                tempList=line.strip("\n").split(",")
                tempList2=[]
                tempList2.append(tempList[0])
                vectorString=tempList[5].strip("[]")
                vectorList=vectorString.split("  ")
                tempList2.append(vectorList)
                self.inputList.append(vectorList)
                self.tweetVectorList.append(tempList2)
            # print "total number of tweets to classify "+str(len(inputList))
            filePointer.close()
        except:
            pass
        return self.inputList

    def analyseList(self):
      list=self.readFile(self)
      myDict={}
      for i in list:
          for j in range(len(i)):
              if int(i[j])!=0:

                if myDict.has_key(j):
                  count=myDict[j]
                  count+= float(i[j])
                  myDict[j]=count
                else:
                  myDict[j]= float(i[j])


    def runKmens(self, K):
        # get a classifier
        from sklearn.cluster import KMeans

        data=np.array(self.inputList)
        # print(data)
        kmeanObj = KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
        y_pred = kmeanObj.fit_predict(data)
        # print y_pred #kmeanObj.predict(data)
        return y_pred


    def clusterlable(self, myDict={}):

        if len(myDict)==0:
            return
        lableDict={}
        for key in myDict:
            tempDict=myDict[key]
            high=1
            lable=[]
            for emo in tempDict:
                if tempDict[emo]>=high:
                    if tempDict[emo]==high:
                      lable.append(emo)
                    else:
                      lable[:]=[]
                      lable.append(emo)
                    high=tempDict[emo]
            if len(lable)==0:
                lable.append("No Emotion")
            lableDict[key]=lable

       # print lableDict
        return lableDict


    def printFrequencyDistribution(self, myDict):
        for key in myDict:
          print "Cluster " + str(key)
          print myDict[key]
          print "========================================================================="


    def findFinalClusterLable(self, vectorLable):
        finalLable=[]
        for lable in vectorLable:
            emo=lable.split("-")
            emoDict={}
            for emotions in emo:
                if emoDict.has_key(emotions):
                    countVal=emoDict[emotions]
                    countVal+=1
                    emoDict[emotions]=countVal
                else:
                    emoDict[emotions]=1
            high=1
            lable=""
            for key in emoDict:
                if emoDict[key]>=high:
                    if emoDict[key]==high:
                      lable=lable+"-"+key
                    else:
                      lable=""
                      lable=key
                    high=emoDict[key]
            finalLable.append(lable)
        return finalLable


    def findClusterDestribution(self, noOfTimesToRunKMeans):
        self.readFile()
        for i in range(1, noOfTimesToRunKMeans+1, 1):
            clusterList=self.runKmens(self.noOfCluster)
            #print "Iteration count "+str(i)
            myDict={}
            it=0
            for lable in clusterList:
                tempTuple=self.inputList[it]
                it+=1
                if myDict.has_key(lable):
                      tempVector=myDict[lable]

                      k=0
                      for key in self.vectorKeyList:
                          temp= float(tempVector[key])
                          temp+= float(tempTuple[k])
                          k+=1
                          tempVector[key]=temp
                      myDict[lable]=tempVector
                else:
                    vector={"anger":0,"disgust":0,"enjoyment":0,"fear":0,"sad":0,"surprise":0,"trust":0,"anticipation":0}
                    j=0
                    for key in self.vectorKeyList:
                        vector[key]= float(tempTuple[j])
                        j+=1
                    myDict[lable]=vector
            lableDict=self.clusterlable(myDict)
            kMeanPath = self.aBasePath + "/../TextSentiment.V1.b/twitterData/KMeans"
            for line in range(len(clusterList)):
                tag=lableDict[clusterList[line]]
                if i==1:
                  for emo in tag:
                   self.annotatedVector.append(emo)
                else:
                   for emo in tag:
                     tempEmo=self.annotatedVector[line]+"-"+emo
                     self.annotatedVector[line]=tempEmo

        finalLableList=self.findFinalClusterLable(self.annotatedVector)

        # write code to read CSV properly
        f2 = open(kMeanPath + "/KMeanOutut.csv","w")
        f2.write( u'TWEET' + "," + u"TWEET TIMESTAMP" + "," + u'ORIGINAL LOCALE' + "," + u"ANNOTATION" + "," + u"RAW EN TEXT" + "," + u"EMO VECTOR" + "," + u"CLUSTER TAG" +"\n")
        with open(self.globalCSVDataStorePath, 'rb') as csvfile:
            readFileObj = csv.reader(csvfile, delimiter=',')
            yPredict = []
            y = []
            next(readFileObj) # ditch the methodology
            for row in readFileObj:
                y.append(row[3])
                yPredict.append(finalLableList[0])
                # print(y[-1],yPredict[-1])
                # print ( row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5] + "," + finalLableList[0] + "," + "\n" )
                f2.write( row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5] + "," + finalLableList[0] + "," + "\n" )
                finalLableList.pop(0) # better to keep it here
        assert len(yPredict) == len(y)
        f2.close()
        csvfile.close()
        self.cvPredict(y,yPredict)


    def cvPredict(self, y, predicted):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            print "\n accuracy_score\t", metrics.accuracy_score(y, predicted)
            print "\n precision_score\t", metrics.precision_score(y, predicted)
            print "\n recall_score\t", metrics.recall_score(y, predicted)
            print "\n classification_report:\n\n", metrics.classification_report(y, predicted)
            print "\n confusion_matrix:\n\n", metrics.confusion_matrix(y, predicted)



def getCluster(noOfTimesToRunKMeans=1):
    obj = UnSupervisedInfrastructure()
    # obj.analyseList()
    obj.findClusterDestribution(noOfTimesToRunKMeans)

if __name__ == '__main__': getCluster()