import sys
import ast
import json
import requests
from random import randint
import matplotlib
import numpy
from numpy.random import randn
import matplotlib.pyplot as plt

class SimilarityMetricComparer(object):

    def __init__(self):
        self.computedTags = []
        self.legelSimilarTags = []
        self.lastAPISimilarTags = []
        self.legelSimilarTagsSet = []
        self.lastAPISimilarTagsSet = []
        self.intersectionOfSimilarTags = []
        self.sizesOfIntersectionOfSimilarTags = []
        self.sumOfMatches = 0                          # total matches between Last.fm API and our similarity metric                  
        self.numberOfTagsToCompare = 250               # number of tags to get from Last.fm API, up to len(self.computedTags) ~5000
        self.averageMatches = 0                        
 
    def readSimilarityDataFromFiles(self):   
        with open('ComputedTags.txt') as f:
            self.computedTags = f.readlines()
        with open('TagSimilarities.txt') as f:
            self.legelSimilarTags = f.readlines()

    def getLastAPISimilarTags(self):
        perPageTags = 50     # number of tags returned by each JSON request 
        apiurl = ('http://ws.audioscrobbler.com/2.0/?api_key=10b2cd686c5d87c1'
                  '0e3ebebe151f5b70&format=json&method=tag.getsimilar&tag=')
        print 'Getting Last API tag.getsimilar data for ' + str(self.numberOfTagsToCompare) + ' tags for comparison with our calculations'
        for eachTag in range(self.numberOfTagsToCompare):
            print eachTag/float(self.numberOfTagsToCompare)*100,"% completed         \r",
            sys.stdout.flush()
            self.lastAPISimilarTags.append([])
            try: # in case the web request fails
                url = apiurl + str(self.computedTags[eachTag])    
                output = json.loads(requests.get(url).content)                      
                for eachOtherTag in range(perPageTags):
                    try: # in case there is no JSON data of similar tags for this particular tag
                        tagName = output['similartags']['tag'][eachOtherTag]['name']
                        self.lastAPISimilarTags[eachTag].append(tagName.encode('utf8'))
                    except:
                        break
            except:
                pass

    def getIntersectionOfSets(self):  # how many matching tags are there in our set of similar tags and Last.fm's?
        for eachTag in range(self.numberOfTagsToCompare):
            theseLegelSimilarTags = ast.literal_eval(self.legelSimilarTags[eachTag])  #our set of similar tags for this tag
            theseLastAPISimilarTags = self.lastAPISimilarTags[eachTag]                #Last.fm's set of similar tags for this tag
            setA = [x[0] for x in theseLegelSimilarTags]                              #get the tag name and ignore the score from our set
            setB = theseLastAPISimilarTags
            self.legelSimilarTagsSet.append(setA)                 
            self.lastAPISimilarTagsSet.append(setB)
            xSet = set(setA).intersection( set(setB) )                                #compute the set intersection
            self.intersectionOfSimilarTags.append(xSet)                               #add this to our list of intersections for each tag
            self.sizesOfIntersectionOfSimilarTags.append(len(xSet))
            self.sumOfMatches += len(xSet)                                            #add the size of this intersection to our total matches
        self.averageMatches = self.sumOfMatches/float(self.numberOfTagsToCompare)     #compute the average matches across all tags
    
    def returnStats(self):
        numberOfTags = self.numberOfTagsToCompare
        print 'Looking closer at differences in 10 random tags:'
        for tag in range(10):
            randomTag = randint(0,numberOfTags-1)
            print '\nMatches for "' + str(self.computedTags[randomTag].rstrip('\n')) + '":'
            print list(self.intersectionOfSimilarTags[randomTag])
            print 'Tags from our similarity metric but not in Last.fm API:'
            print list ( set(self.legelSimilarTagsSet[randomTag]) - set(self.intersectionOfSimilarTags[randomTag]) )
            print 'Tags from Last.fm API not in our similarity metric:'
            print list ( set(self.lastAPISimilarTagsSet[randomTag]) - set(self.intersectionOfSimilarTags[randomTag]) ) 
        print '\nComparing matches of Last.fm API similar tags and our similar tags for each tag'
        print str(self.sumOfMatches) + ' total matches across ' + str(numberOfTags) + ' tags:'
        print 'Average of ' + str(self.averageMatches) + ' matches per tag'
    
    def showHistogram(self):
        plt.hist(self.sizesOfIntersectionOfSimilarTags, 12)
        plt.xlabel('Size of Set Intersection Between Last.fm and Legel Sets of Similar Tags')
        plt.ylabel('Number of Tags With This Intersection Size')
        plt.title('Correlation of Similar Tag Computations by Last.fm and Legel')
        plt.show()

    def saveFile(self, fileName, objectData, encode=True):
        with open(fileName, 'wb') as fileObject:
            for item in objectData:
                 if encode:
                    fileObject.write("%s\n" % item.encode('utf8')) 
                 else:
                    fileObject.write("%s\n" % item)
    
    def saveMatchData(self):
        with open('SimilarTagMatches.txt', 'wb') as fileObject:
            for tag in range(self.numberOfTagsToCompare):
                fileObject.write('\n\nMatches for "' + str(self.computedTags[tag].rstrip('\n')) + '":')
                fileObject.write('\n' + str (list(self.intersectionOfSimilarTags[tag])) )
                fileObject.write('\n' + 'Tags from our similarity metric but not in Last.fm API:')
                fileObject.write('\n' + str( list ( set(self.legelSimilarTagsSet[tag]) - set(self.intersectionOfSimilarTags[tag]) )) )
                fileObject.write('\n' + 'Tags from Last.fm API not in our similarity metric:')
                fileObject.write('\n' + str( list ( set(self.lastAPISimilarTagsSet[tag]) - set(self.intersectionOfSimilarTags[tag])) ))      

if __name__=='__main__':
    smc = SimilarityMetricComparer()
    smc.readSimilarityDataFromFiles()
    smc.getLastAPISimilarTags()
    smc.getIntersectionOfSets()
    smc.saveFile('LastTagSimilarities.txt', smc.lastAPISimilarTags, False)
    smc.saveFile('IntersectionOfSimilarTags.txt', smc.intersectionOfSimilarTags, False)
    smc.saveMatchData()
    smc.returnStats()
    smc.showHistogram()

