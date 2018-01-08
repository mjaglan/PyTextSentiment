# -*- coding: utf-8 -*-

# create a vector
import numpy as np
import Utility

# for clean console output, let's suppress them for now.
import warnings
warnings.filterwarnings("ignore")

# get data from csv
import csv

import os
aBasePath = os.getcwd()
globalCSVDataStorePath = aBasePath+"/assets/twitterData/myJsonOutput.csv"
resPath = aBasePath + '/assets/twitterData'

# get a classifier
from sklearn import cross_validation, metrics



# Experimental purpose
from dircache import listdir
from genericpath import isfile
from string import join


"""
NOTE: Avoid multiple inheritance at all costs, as it can grow too complex to be reliable.
"""
class SupervisedInfrastructure:
    # keep it this way for now
    def __init__(self):
        self.TagMapperDictionary = {"anger":0,"anticipation":1,"disgust":2,"enjoyment":3,"fear":4,"sad":5,"surprise":6,"trust":7}
        self.TagMapperList = ["anger" , "anticipation" , "disgust" , "enjoyment" , "fear" , "sad" , "surprise" , "trust"]

    def GetTrainVectors(self, filePath):
        with open(filePath, 'rb') as csvfile:
            readFile = csv.reader(csvfile, delimiter=',')
            X = None
            y = None
            for row in readFile:
                # aRow = row[-1]
                listStrA = row[3]
                listStr1 = row[5]
                listStr2 = listStr1[1:-1]
                listStr3 = listStr2.split()
                listVector = [float(i) for i in listStr3 if Utility.RepresentsNum(i)]

                # print (type(row), len(row), listVector)
                # newrow = [1,2,3]
                # print(">>", len(listVector), listVector)

                if len(listVector) != 0:
                    assert (len(listVector) == 8) # emo-vector length should be 8;
                    if True: # Training Only
                        emoTypesCount = 0
                        for i in range(0,8,1):
                            if (listVector[i] > 0.0):
                                emoTypesCount += 1

                        if (emoTypesCount == 0):
                            emoLabel = 8 # "neutral"     # Future Road Map Label
                            break
                        elif (emoTypesCount <= 5):      # Boundary line
                            emoLabel = self.TagMapperDictionary[listStrA]
                        else:
                            emoLabel = 9 # "mixed" # Future Road Map Label
                            break

                    if X is None and y is None:
                        X = np.array(listVector)
                        y = np.array([emoLabel])
                    else:
                        X = np.vstack( (X, np.array(listVector)) )
                        y = np.hstack( (y, np.array([emoLabel])) )

        assert list(X.shape)[0] == list(y.shape)[0]
        return X, y


    def cvredictNBC(self, clf):
        X, y = self.GetTrainVectors(globalCSVDataStorePath)
        # print(X.shape)
        # print(y.shape)
        clf.fit(X, y)
        predicted = cross_validation.cross_val_predict(clf, X, y, cv=5)  # better at cv==5
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            print "\n accuracy_score\t", metrics.accuracy_score(y, predicted)
            print "\n precision_score\t", metrics.precision_score(y, predicted)
            print "\n recall_score\t", metrics.recall_score(y, predicted)
            print "\n classification_report:\n\n", metrics.classification_report(y, predicted)
            print "\n confusion_matrix:\n\n", metrics.confusion_matrix(y, predicted)


    def mainNBC(self, clf, emoVector = np.array([[1,0,0,1,0,0,0,0]])):
        X, y = self.GetTrainVectors(globalCSVDataStorePath)
        # print(X.shape)
        # print(y.shape)
        clf.fit(X, y)

        outList = clf.predict(emoVector)

        outListCat = []
        for anItem in outList:
            outListCat.append(self.TagMapperList[anItem])
        return outListCat


    def bulkMain(self, clf):
        onlyfiles = sorted([f for f in listdir(resPath) if (f.endswith(".csv"))])
        for aFile in onlyfiles:
            X, y = self.GetTrainVectors(resPath +"/"+ aFile)
            # print(X.shape)
            # print(y.shape)
            clf.fit(X, y)
            predicted = cross_validation.cross_val_predict(clf, X, y, cv=5)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                print "\n Train File\t", aFile
                print "\n accuracy_score\t", metrics.accuracy_score(y, predicted)
                print "\n precision_score\t", metrics.precision_score(y, predicted)
                print "\n recall_score\t", metrics.recall_score(y, predicted)
                print "\n classification_report:\n\n", metrics.classification_report(y, predicted)
                print "\n confusion_matrix:\n\n", metrics.confusion_matrix(y, predicted)


    def read2ColumnTrend(self, clf):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            X, y = self.GetTrainVectors(globalCSVDataStorePath)
            # print(X.shape)
            # print(y.shape)
            clf.fit(X, y)
            filePath = resPath + "/test/TestJsonOutput.csv"
            ofilePath = resPath + "/test/TestOutput.csv"
            ofile = open(ofilePath, 'w')
            ofile.write("NAME" + "," + "anger,anticipation,disgust,enjoyment,fear,sad,surprise,trust,\n")
            consolidated = {}
            with open(filePath, 'r') as csvfile:
                readFile = csv.reader(csvfile, delimiter=',')
                next(readFile)
                for row in readFile:
                    listStrA = row[0]
                    listStr1 = row[1]
                    listStr2 = listStr1[1:-1]
                    listStr3 = listStr2.split()
                    listVector = [float(i) for i in listStr3 if Utility.RepresentsNum(i)]
                    outList = clf.predict(np.array(listVector))
                    # print(outList)
                    if listStrA in consolidated.keys():
                        consolidated[listStrA][outList[0]] += 1
                    else:
                        consolidated[listStrA] = [0]*8
                    # print (listStrA + "," + TagMapperList[outList] + "\n")
            for k in consolidated.keys():
                ofile.write(k + "," + str(consolidated[k])[1:-1] + "\n")
            csvfile.close()
            ofile.close()


    def read2ColumnTrendTagger(self, clf):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            filePath = resPath + "/test/TestJsonOutput.csv"
            ofilePath = resPath + "/test/TestOutput.csv"
            ofile = open(ofilePath, 'w')
            ofile.write("NAME" + "," + "anger,anticipation,disgust,enjoyment,fear,sad,surprise,trust,\n")
            consolidated = {}
            with open(filePath, 'r') as csvfile:
                readFile = csv.reader(csvfile, delimiter=',')
                next(readFile)
                for row in readFile:
                    listStrA = row[0]
                    listStr1 = row[1]
                    listStr2 = listStr1[1:-1]
                    listStr3 = listStr2.split()
                    listVector = [float(i) for i in listStr3 if Utility.RepresentsNum(i)]
                    if listStrA in consolidated.keys():
                        for i in range(0,8,1):
                            consolidated[listStrA][i] += listVector[i]
                    else:
                        consolidated[listStrA] = [0]*8
            for k in consolidated.keys():
                ofile.write(k + "," + str(consolidated[k])[1:-1] + "\n")
            csvfile.close()
            ofile.close()


def getPrediction(npVector=None, model=""):

    modelName = model.lower()
    if(modelName == "svc"):
        from sklearn.svm import SVC
        from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
        clf = OneVsRestClassifier(SVC(C=1, kernel = 'linear', gamma=1, verbose= False, probability=False))
    elif (modelName == "nbc"):
        from sklearn.naive_bayes import MultinomialNB
        clf = MultinomialNB(alpha=0.1, class_prior=None, fit_prior=True)
    else:
        print(unicode(model) + u" not found!")
        exit(-1)

    obj = SupervisedInfrastructure()

    if npVector is None:
        npVector = np.array([[1,0,0,1,0,0,0,0]])
    print(model, obj.mainNBC(clf, emoVector = npVector))


def test():
    getPrediction (model='SVc')
    getPrediction (model='NBC')

if __name__ == '__main__': test()


