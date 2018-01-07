# -*- coding: utf-8 -*-

"""
Authors: anprasad@umail.iu.edu, mjaglan@umail.iu.edu
"""

import nltk
from nltk.corpus import wordnet as wn
import os

class SyntacticTagger:
    def __init__ (self):
        self.basePath = os.getcwd()
        self.path = self.basePath+"/assets/Resource"
        self.patternPath = self.path+"/pattern.txt"
        self.siftMapper = self.path+"/SiftMapper.txt"
        self.emotions=['AngerSynonyms','Anger','DisgustSynonyms','Disgust','EnjoymentSynonyms','Enjoyment','FearSynonyms','Fear','SadSynonyms','Sad','Surprise']
        self.emotionDict={}
        self.patternDict={}
        self.siftMapperDict={}

        for filename in self.emotions:

            list=[]
            openPath=self.path+"/"+filename+".txt"
            file=open(openPath)
            tempKey=""
            for key in self.emotionDict:
                if filename in key:
                   tempKey=key
                   break
            if tempKey.__len__()!=0:
                list=self.emotionDict[tempKey]
                for line in file:
                    list.append(line.strip("\n\r").lower())
                self.emotionDict[tempKey]=list
            else:
                 for line in file:
                    list.append(line.strip("\n\r").lower())
                 self.emotionDict[filename]=list
            file.close()

        patternFile=open(self.patternPath)
        for pattern in patternFile:
            tuple=pattern.strip("\n\r").split("=")
            tempList=[]
            if self.patternDict.has_key(tuple[0]):
                tempList=self.patternDict[tuple[0]]
                tempList.append(tuple[1])
                self.patternDict[tuple[0]]=tempList
            else:
                tempList.append(tuple[1])
                self.patternDict[tuple[0]]=tempList

        patternFile.close()

        siftCalFile=open(self.siftMapper)
        for line in siftCalFile:
            temp=line.strip("\n\r").split("=")
            self.siftMapperDict[temp[0]]=temp[1]


    def similarity(self, w1, w2, sim=wn.path_similarity):
      synsets1 = wn.synsets(w1)
      synsets2 = wn.synsets(w2)
      sim_scores = []
      for synset1 in synsets1:
        for synset2 in synsets2:
          sim_scores.append(sim(synset1, synset2))
      if len(sim_scores) == 0:
        return 0
      else:
        return max(sim_scores)


    def findEmotions(self, sentence):
        #print "======================================================================================================="
        isFound=False
        emoWords={}
        wordList=sentence.lower().split(" ")

        for word in wordList:
           #print word
           isFound=False
           if len(word)>2:
               for key in self.emotionDict:
                    if isFound==True:
                        break
                    for emotion in self.emotionDict[key]:

                        # QUICK: Find exact match in BOW!!
                        if emotion == word:
                            emoWords[emotion.strip("\n\r")]=key
                            isFound=True

                        else:
                            # Think of better ways to extract emo words from raw words
                            pass

                        if isFound==True:
                            break

        if isFound == False:
            for word in wordList:
               #print word
               isFound=False
               if len(word)>2:
                   for key in self.emotionDict:
                        if isFound==True:
                            break
                        for emotion in self.emotionDict[key]:

                            # TIME CONSUMING: Find similarity of words!!
                            if self.similarity(emotion.strip(),word)==1:
                                if len(emotion.strip())-len(word) >3 or len(emotion.strip())-len(word) <-3 :
                                    continue
                                #print "sentence word "+word+" Emotion Word "+emotion
                                isFound=True
                                emoWords[emotion.strip("\n")]=key
                                # print "Emotion family "+key +" Emotion is "+emotion

                            else:
                                # Think of better ways to extract emo words from raw words
                                pass

                            if isFound==True:
                                break

        #print "emo word found "+str(emoWords)
        textList=""
        if len(emoWords)!=0:
             text=nltk.word_tokenize(sentence)
             textList=nltk.pos_tag(text)
        return self.findValanceSift(emoWords,textList)


    def findValanceSift(self, emotion,tokenText):
        """
        Using Bi-grams and N-grams for now.

        :param emotion:
        :param tokenText:
        :return:
        """
        tempString=""
        result={}
        for tag in tokenText:
          tempString=tempString+" "+tag[0]

        # print "old string "+tempString
        newStr=tempString.replace('n\'t','not')

        # print "new String "+newStr
        patternFound=False
        for foundEmoKey in emotion:
            # print "emo ol "+foundEmoKey
            loc=0
            isFound=True
            patternFound=False

            if isFound==True:
                for key in self.patternDict:
                    if patternFound:
                        break
                    if key in newStr:
                        # print "gonna search for "+key
                        patternList=self.patternDict[key]
                        for pattern in patternList:
                            # print "pattern "+pattern
                            tempPat=pattern.split(" ")
                            tempPat[-1]=foundEmoKey
                            tempPat[0]=key
                            foundGlobal=False
                            cannotFind=False
                            if patternFound:
                                break
                            for i in range(len(tokenText)):
                               initialVal=i
                               pos=0
                               if patternFound==True or cannotFind==True:
                                   break
                               while pos<len(tempPat) :
                                   if cannotFind :
                                       break
                                   if pos==0:
                                        if tokenText[i][0]!=tempPat[0] :
                                            pos=0
                                            break
                                        else:
                                            pos+=1
                                   elif len(tempPat)-pos>1 :
                                       if "**" in tempPat[pos] or '~' in tempPat[pos]:
                                           tempPos=pos+1
                                           nextPatern=tempPat[tempPos]
                                           access=1
                                           if len(tempPat)-tempPos==1:
                                               access=0
                                           found=False
                                           i=initialVal
                                           for j in range(i+pos,len(tokenText)):
                                               if '~' in tempPat[pos] :
                                                   token=tempPat[pos].replace("~","")
                                                   if token in tokenText[j][1]:
                                                       cannotFind=True
                                                       break
                                               if access==0:
                                                 if self.similarity(nextPatern,tokenText[j][access])==1 :
                                                   i=j
                                                   found=True
                                                   foundGlobal=True
                                                   break
                                               else:
                                                 if nextPatern in tokenText[j][access]:
                                                   i=j
                                                   found=True
                                                   foundGlobal=True
                                                   break

                                           if not found:
                                                pos=0
                                                break
                                           else :
                                               pos+=1
                                       else:
                                           if foundGlobal :
                                             if tempPat[pos] in tokenText[i][1]:
                                               pos+=1
                                               i+=1
                                             else:
                                               pos=0
                                               break
                                           else:
                                             if tempPat[pos] in tokenText[i+pos][1]:
                                               pos+=1
                                             else:
                                               pos=0
                                               break


                                   else :
                                       if foundGlobal:
                                           if self.similarity(tempPat[pos],tokenText[i][0])==1 :
                                             patternFound=True
                                             result[emotion[foundEmoKey]]=key+" "+tokenText[i][0]
                                             break
                                           else :
                                             pos=0
                                             break
                                       else:
                                           if self.similarity(tempPat[pos],tokenText[i+pos][0])==1 :
                                               patternFound=True
                                               result[emotion[foundEmoKey]]=key+" "+tokenText[i+pos][0]
                                               break
                                           else :
                                              pos=0
                                              break
            if patternFound==False:
                result[emotion[foundEmoKey]]="????"

        return self.calculateFinalValance(result)



    def calculateFinalValance(self, result={}):
        vector={"anger":0,"disgust":0,"enjoyment":0,"fear":0,"sad":0,"surprise":0,"trust":0,"anticipation":0}
        vsift=""
        for emotion in result :
            temp=result[emotion].split(" ")
            try :
               vsift=self.siftMapperDict[temp[0]]
            except KeyError :
                hi=0
            siftedemo=emotion.lower()
            if vsift=='-' :
                siftedemo=self.findReverseOfEmotion(emotion.lower())
                vector[siftedemo]=1
            elif vsift=='.5':
                vector[self.findEmoName(siftedemo)]=0.5
            elif vsift=='0' :
                vector[self.findEmoName(siftedemo)]=0
            elif vsift=='1.5':
                vector[self.findEmoName(siftedemo)]=1.5
            else:
                 vector[self.findEmoName(siftedemo)]=1

        return vector



    def findEmoName(self, emo):
        if "anger" in emo:
            return "anger"
        elif "fear" in emo:
            return "fear"
        elif "disgust" in emo:
            return "disgust"
        elif "trust" in emo:
            return "trust"
        elif "enjoyment" in emo:
            return "enjoyment"
        elif "sad" in emo:
            return "sad"
        elif "surprise" in emo:
            return "surprise"
        else:
            return "anticipation"

    def findReverseOfEmotion(self, emo):
        if "anger" in emo:
            return "fear"
        elif "fear" in emo:
            return "anger"
        elif "disgust" in emo:
            return "trust"
        elif "trust" in emo:
            return "disgust"
        elif "enjoyment" in emo:
            return "sad"
        elif "sad" in emo:
            return "enjoyment"
        elif "surprise" in emo:
            return "anticipation"
        else:
            return "surprise"

    def runTestCase(self):
        readTest=open(self.path+"/TestSentences.txt")
        for line in readTest:
            self.findEmotions(line.strip())


    def splitSentence(self, sen):
        stoper=[".","!","?"]
        l=[]
        for stop in stoper:
         if len(l)!=0:
             for temp in l:
                 if stop in temp:
                  temp1=temp.split(stop)
                  for temp2 in temp1:
                     l.append(temp2)
         else :
             if stop in sen:
              l=sen.split(stop)



        finalList=[]
        for line in l:
         isStoper=False
         for tem in stoper:
           if tem in line:
              isStoper=True
              break
         if not isStoper:
           if len(line.strip())!=0:
             if line not in finalList:
                 finalList.append(line.strip("\n\r\t"))

        return finalList


    def consolodateResult(self, tweet):
       sentenceList=self.splitSentence(tweet+".")
       finalDict={}
       # print sentenceList

       # print sentenceList
       for sentence in sentenceList:
          tempDict=self.findEmotions(sentence+" .")
          for key in tempDict:
              if finalDict.__contains__(key):
                  tempVal=finalDict[key]
                  tempVal=tempVal+tempDict[key]
                  finalDict[key]=tempVal
              else:
                  finalDict[key]=tempDict[key]

       return finalDict


if __name__ == '__main__': print SyntacticTagger().consolodateResult(tweet=u"Forgive people in your life even those who are not sorry for their actions! Holding on to anger only hurts you not them")
