# -*- coding: utf-8 -*-

import os
import sys
import numpy

# source: https://github.com/geduldig/TwitterAPI
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRequestError, TwitterConnectionError
import re

# for clean console output, let's suppress them for now.
import warnings
warnings.filterwarnings("ignore")

aBasePath = os.getcwd()
# fullPath=aBasePath+"/smm.emotions"
# sys.path.insert(0, fullPath)
import EmotionTagger

import NBC
import SVM
import KMeans
import GeoLocationModule
import TranslationModule
import time

reload(sys)
sys.setdefaultencoding('utf8')

globalCSVDataStorePath = aBasePath+"/../TextSentiment.V1.b/twitterData/myJsonOutput.csv"

globalAppObj = None
def getAppObject():
    global globalAppObj

    if globalAppObj is None:
        # Using OAuth1...
        o = TwitterOAuth.read_file()
        globalAppObj = TwitterAPI(o.consumer_key, o.consumer_secret, o.access_token_key, o.access_token_secret)

    return globalAppObj

def getFeedsByText(api=None, f1=None, isLive=True, annotation=None, queryText=u'a', textLang=None, isTrain=False, locationArea=None):
    # ts = time.time()
    # st = unicode(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

    iteratorRunCount = 0
    isDuplicateList = []
    tweetsRecorded = 0
    reTryCount = 0
    MAX_TWEET = 5
    MAX_TRIES = 10
    while True:
        try:

            # TODO: think of better ways to handle this
            if (iteratorRunCount >= 2): # hack, this limits the number of tweets you want to retrieve
                print( "\n ASSUMPTION: there are no tweets as of now. Let's go back! \n\n")
                print(u"\n\n\n")
                return
            elif (iteratorRunCount >= 1):
                if (queryText[0] == '#'):
                    queryText = queryText[1:]
                else:
                    print( "\n ASSUMPTION: there are no tweets as of now. Let's go back! \n\n")
                    print(u"\n\n\n")
                    return
            else:
                # try first iteration with original search
                pass

            time.sleep(int(3600/100)+4) # Let's take 40 seconds pause; twitter rate limit is 100 API calls per hour in total per account; source: https://blog.twitter.com/2008/what-does-rate-limit-exceeded-mean-updated

            if (textLang is not None):
                queryText = queryText + ' lang:' + textLang

            if isLive==True:
                if locationArea is None:
                    # live tweets without location filter
                    iterator = api.request('statuses/filter', {'track':queryText}).get_iterator()
                else:
                    # live tweets with location filter
                    coordinateString=GeoLocationModule.getGeoArea(area=locationArea)
                    iterator = api.request('statuses/filter', {'track':queryText, 'locations':coordinateString}).get_iterator()

            else: # isLive==False
                if locationArea is None:
                    # search tweets without location filter
                    iterator = api.request('search/tweets', {'q':queryText}).get_iterator()
                else:
                    # search tweets with location filter
                    coordinateString=GeoLocationModule.getGeoArea(area=locationArea)
                    iterator = api.request('search/tweets', {'q':queryText, 'locations':coordinateString}).get_iterator()

            iteratorRunCount += 1

            for item in iterator:
                if ( ('text' in item) and (item[u'id'] not in isDuplicateList) and (item[u'retweeted']==False) ):

                    rawTextClean1 = item[u'text'].encode('utf-8')
                    rawTextClean2 = rawTextClean1.strip()
                    rawTextClean3 = rawTextClean2.replace("#"," ")  # remove hashtags
                    rawTextClean4 = re.sub(r'https?:\/\/.*[\r\n]*', '', rawTextClean3, flags=re.MULTILINE) # remove urls

                    if (25 < len(rawTextClean4))   and   (len(item[u'text']) < 140): # take tweets with sufficient text
                        isDuplicateList.append(item[u'id'])
                        tweetsRecorded += 1

                        rawEnText = TranslationModule.getEnglish(rawTextClean4)
                        fineEnText = rawEnText.replace(",", " ").replace(";", " ")
                        print( str(tweetsRecorded) + ":\t" + item[u'lang'] + ",\t\t" + annotation.lower() + "\t\t:" + queryText + "\t\t:" + str(len(fineEnText)) + "\n\t:" + fineEnText)

                        emoVector = EmotionTagger.consolodateResult(fineEnText)
                        listRes = []
                        keyRes  = sorted(emoVector)
                        for key in keyRes:
                            listRes.append(emoVector[key])
                        print(listRes, keyRes)

                        if isTrain == True:
                            f1.write( item[u'id_str'] + "," + unicode(item[u'created_at']) + "," + item[u'lang'] + "," + annotation.lower() + "," + fineEnText.replace("\n", " ").replace("\r", " ") + "," + str(listRes).replace(",", " ") + "," + "\n" )
                            f1.flush()
                            os.fsync(f1.fileno())
                        else:
                            NBC.mainNBC(numpy.array([ listRes ]))
                            SVM.mainSVC(numpy.array([ listRes ]))

                        if (tweetsRecorded >= MAX_TWEET) or (reTryCount >= MAX_TRIES):
                            print( "\n ReTry Count: " + str(reTryCount) + "\n\n")
                            print(u"\n\n\n")
                            return

                        print(u"\n\n\n")

                elif 'disconnect' in item:
                    event = item['disconnect']
                    reTryCount += 1

                    if event['code'] in [2,5,6,7]:
                        # something may or may NOT need to be fixed before re-connecting
                        raise Exception(event['reason'])
                    else:
                        # temporary interruption, re-try request
                        break

                elif (iteratorRunCount > 0) and (tweetsRecorded < MAX_TWEET): # Condition when no more unique tweets are found, go back
                    # TODO: think of better ways to handle this
                    if (queryText[0] == '#'):
                        queryText = queryText[1:]
                        break
                    else:
                        print( "\n No more tweets as of now \n\n")
                        print(u"\n\n\n")
                        return

                else:
                    pass

        except TwitterRequestError as e:
            if e.status_code < 500:
                print "\n\nMJAGLAN EXCEPTION:\n"+str(e)+"\n\n"
                pass
            else:
                # temporary interruption, re-try request
                pass
                # if (queryText[0] == '#'):     # this has certain side-effects
                #     queryText = queryText[1:]
                #     pass
                # else:
                #     print( "\n Seems like there are no tweets as of now \n\n")
                #     print(u"\n\n\n")
                #     return

        except TwitterConnectionError:
            # temporary interruption, re-try request
            pass



# Method intended to find most popular tends on twitter in a city
def liveFeedsByLocation(api=getAppObject(), locationArea="New York City, NY"):
    coordinateString=GeoLocationModule.getGeoArea(area=locationArea)
    while True:
        try:
            time.sleep(int(3600/100)+4) # Let's take 40 seconds pause; twitter rate limit is 100 API calls per hour in total per account; source: https://blog.twitter.com/2008/what-does-rate-limit-exceeded-mean-updated
            iterator = api.request('statuses/filter', {'locations': coordinateString}).get_iterator()
            for item in iterator:
                if 'text' in item:
                    print(item[u'lang'] + ":\t" +  item['text'].encode('utf-8').strip() + '\n\n\n' )
                elif 'disconnect' in item:
                    event = item['disconnect']
                    if event['code'] in [2,5,6,7]:
                        # something needs to be fixed before re-connecting
                        raise Exception(event['reason'])
                    else:
                        # temporary interruption, re-try request
                        break

        except TwitterRequestError as e:
            if e.status_code < 500:
                # something needs to be fixed before re-connecting
                raise
                # print "\n\nMJAGLAN EXCEPTION:\n"+str(e)+"\n\n"
                # pass
            else:
                # temporary interruption, re-try request
                pass

        except TwitterConnectionError:
            # temporary interruption, re-try request
            pass



from os import listdir
from os.path import isfile, join
def main():

    apiObj = getAppObject()

    if not os.path.isfile(globalCSVDataStorePath):
        f2 = open(globalCSVDataStorePath, 'a+')
        f2.write( u'TWEET' + "," + u"TWEET TIMESTAMP" + "," + u'ORIGINAL LOCALE' + "," + u"ANNOTATION" + "," + u"RAW EN TEXT" + "," + u"EMO VECTOR"+"\n")
    else:
        f2 = open(globalCSVDataStorePath, 'a')

    # QUERY CONSTRAINTS #
    regionName  = None # "Seoul, South Korea"
    localeCode  = None # "ko"
    setTrainMode = False
    setLive = False

    if setTrainMode == False:
        resPath = aBasePath + '/../TextSentiment.V1.b/Resource/searchKeys/testFiles'
    else:
        resPath = aBasePath + '/../TextSentiment.V1.b/Resource/searchKeys'

    onlyfiles = sorted([f for f in listdir(resPath) if (isfile(join(resPath, f)) and not f.endswith("~"))])
    for aFile in onlyfiles:
        myAnnotation, extension = os.path.splitext(aFile.lower())
        with open(join(resPath,aFile), 'r') as f1:
            read_data = f1.readlines()
            for eachWord in read_data[0:300]:
                aWord = str(eachWord).strip('\r\n').lower()
                if len(aWord) > 2: # avoid mess
                    aWord = "#" + aWord # prepend hashtag for better relevance
                    getFeedsByText(api=apiObj, f1=f2, isLive=setLive, annotation=myAnnotation, queryText=unicode(aWord), textLang=localeCode, isTrain=setTrainMode, locationArea=regionName)
                else:
                    print("\n[NOTE]: Bad query text!")

            f1.close()
    f2.close()

    if setTrainMode == True:
        KMeans.findClusterDestribution(noOfTimesToRunKMeans=17)



# liveFeedsByLocation(api=getAppObject(), locationArea="Seoul, South Korea")
# main()
