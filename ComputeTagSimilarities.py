import math
import ast 
import json
import requests

class TagSimilarityMeasurer(object):

    def __init__(self):
        self.tagNames = []
        self.tagCooccurrences = []
        self.mostSimilarTags = []
        self.computedTags = []
        self.tagCount = 0

    def readTagDataFromFiles(self):   
        with open('TagCooccurrences.txt') as f:
            lines = f.readlines()
            for line in lines:
                cooccurrence = ast.literal_eval(line)                # parse string into a dictionary of cooccurrences
                self.tagCooccurrences.append(cooccurrence)           # append to our complete set of lists
        with open('TagNames.txt') as f:
            self.tagNames = f.readlines()

    def computeMostSimilarTags(self):
        print "Computing 50 most similar tags from each of the following tags:"
        numberOfTags = len(self.tagNames)
        for eachTag in range(numberOfTags):
            thisTagSimilarity = []
            thisTagCooccurrence = self.tagCooccurrences[eachTag]     # focus on the cooccurrences between this tag and every other tag
            
            if self.tagCooccurrences[eachTag]:                       # ignore if dictionary is empty: tag removed because it was sparse
                thisTagName = self.tagNames[eachTag].rstrip('\n')    # get the name of this tag, removing an extra \n at end
                print thisTagName
                self.computedTags.append(thisTagName)
                self.mostSimilarTags.append([])
                for eachOtherTag in range(len(self.tagCooccurrences)):          
                    otherTagCooccurrence = self.tagCooccurrences[eachOtherTag]
                    # compute cosine similarity between this tag and every other        
                    thisTagSimilarity.append(self.cosine_similarity(thisTagCooccurrence,otherTagCooccurrence))
                # sort the list of similarities in decreasing order
                rankedIndecesOfTagSimilarities = [i[0] for i in sorted(enumerate(thisTagSimilarity), key=lambda x:x[1], reverse=True)]
    
                for i in range(51): # get top 50 most similar tags to this tag
                    mostSimilarTag = self.tagNames[rankedIndecesOfTagSimilarities[i]].rstrip('\n')  # get the similar tag's name
                    tagSimilarity = thisTagSimilarity[rankedIndecesOfTagSimilarities[i]]            # get its similarity score
                    self.mostSimilarTags[self.tagCount].append((mostSimilarTag, tagSimilarity))     # save tuple (tag, similarity score)
                self.tagCount += 1     

    def cosine_similarity(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return round(float(numerator) / denominator, 3)

    def saveFile(self, fileName, objectData):
        with open(fileName, 'wb') as fileObject:
            for item in objectData:
                fileObject.write("%s\n" % item)

if __name__=='__main__':
    tam = TagSimilarityMeasurer()
    tam.readTagDataFromFiles()
    tam.computeMostSimilarTags()
    tam.saveFile('ComputedTags.txt', tam.computedTags)
    tam.saveFile('TagSimilarities.txt', tam.mostSimilarTags)
