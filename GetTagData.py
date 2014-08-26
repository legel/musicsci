import sys
import json
import requests

class TagScraper(object):

    def __init__(self):
        self.artistNames = []
        self.artistIDs = []
        self.tagNames = []
        self.tagCooccurrences = []
        self.apiurl = 'http://ws.audioscrobbler.com/2.0/?api_key=10b2cd686c5d87c10e3ebebe151f5b70&format=json'

    def getArtistIDs(self):
        print 'Getting identities of top 1000 artists from Last.fm API'
        totalPagesArtists = 20				 
        perPageArtists = 50

        for page in range(totalPagesArtists):
            self.printPercentCompleted(page,totalPagesArtists)				     
            url = self.apiurl + '&method=chart.gettopartists&page=' + str(page+1)    # URL to get each page of artists
            webpage = requests.get(url).content					     
            topArtists = json.loads(webpage)                                         # formats webpage as JSON object
            
            for eachArtist in range(perPageArtists):
                artistName = topArtists['artists']['artist'][eachArtist]['name']     # get each artist name
                artistID = topArtists['artists']['artist'][eachArtist]['mbid']       # get each artist ID
                self.artistNames.append(artistName)                                      
                self.artistIDs.append(artistID) 
                                                       
    def getTagCooccurrences(self):
        print 'Recording cooccurring tags across all of the following 1000 artists:'
        for i, artistID in enumerate(self.artistIDs):
            print str(i+1) + '. ' + self.artistNames[i]

            # ignore the few cases where API provided empty string for artist ID
            if artistID != '':                                     
                url = self.apiurl + '&method=artist.gettoptags&mbid=' + str(artistID)    # URL to get top tags for each artist
                webpage = requests.get(url).content					 
                artistTags = json.loads(webpage)                                         # formats webpage as JSON object   
                try:                                                                     # ignore if artist has no tags and returns error
                    self.indexEachTag(artistTags)
                    self.recordEachCooccurringTag(artistTags)
                except:
                    pass

    def indexEachTag(self, artistTags):
        numberOfTags = len(artistTags['toptags']['tag'])                         # count total tags on page
        for eachTag in range(numberOfTags):
            if self.tagIsSignificant(artistTags,eachTag):	                                     
                thisTagName = artistTags['toptags']['tag'][eachTag]['name']      # get the name of this tag
                if thisTagName not in self.tagNames:			        
                    self.tagNames.append(thisTagName)                            # if new, add tag to our list of names
                    tagIndex = self.tagNames.index(thisTagName)
                    # initialize dictionary to list for counting cooccurrences with this new tag
                    self.tagCooccurrences.append({tagIndex: 0})
    
    def recordEachCooccurringTag(self, artistTags):
        numberOfTags = len(artistTags['toptags']['tag'])			 # count total tags on page
        for eachTag in range(numberOfTags):  
            if self.tagIsSignificant(artistTags,eachTag):           
                thisTagName = artistTags['toptags']['tag'][eachTag]['name']	 # get the name of this tag
                thisTagIndex = self.tagNames.index(thisTagName) 
                for eachOtherTag in range(numberOfTags):                         # save this tag's occurence with each other tag     
                    if self.tagIsSignificant(artistTags,eachOtherTag): 
                        otherTagName = artistTags['toptags']['tag'][eachOtherTag]['name']  
                        otherTagIndex = self.tagNames.index(otherTagName)   
                        if otherTagIndex not in self.tagCooccurrences[thisTagIndex]:	            
                            self.tagCooccurrences[thisTagIndex][otherTagIndex] = 1   # if first time these tags occur together
                        else:
                            self.tagCooccurrences[thisTagIndex][otherTagIndex] += 1  # else add to previous occurence count
                    
    def printPercentCompleted(self, current, total):
        print current/float(total)*100,"% completed         \r",
        sys.stdout.flush()
    
    # return whether or not count for tag is above 1, while handling the rare condition of a null count
    def tagIsSignificant(self, artistTags, thisTag):                       
        try:
            significant = int(artistTags['toptags']['tag'][thisTag]['count']) > 0
        except:
            significant = False
        return significant

    def filterSparseTagCooccurrences(self):
        occurrenceThreshold = 5
        print 'Filtering out sparse tag cooccurences, defined as less than ' + str(occurrenceThreshold) + ' counts'
        for eachTagVector in self.tagCooccurrences:	        	
            tagsToRemove = []						       
            for eachTag in eachTagVector:				
                if eachTagVector[eachTag] < occurrenceThreshold:		# if the tag does not co-occur beyond the threshold
                    tagsToRemove.append(eachTag)   				# then add to list of tags to be popped
            for removeThisTag in range(len(tagsToRemove)):				
                eachTagVector.pop(tagsToRemove[removeThisTag],None)             # and pop them

    def saveFile(self, fileName, objectData, encode=True):
        with open(fileName, 'wb') as fileObject:
            for item in objectData:
                 if encode:
                    fileObject.write("%s\n" % item.encode('utf8')) 
                 else:
                    fileObject.write("%s\n" % item)
     
if __name__=='__main__':
    ts = TagScraper()
    ts.getArtistIDs()
    ts.getTagCooccurrences()
    ts.filterSparseTagCooccurrences()
    ts.saveFile('TagNames.txt', ts.tagNames)
    ts.saveFile('TagCooccurrences.txt', ts.tagCooccurrences, False)

