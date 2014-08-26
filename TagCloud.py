import ast
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
import webbrowser

def getSimilarities(index):
    with open('TagSimilarities.txt') as obj:
        tags = obj.readlines()
        tagSimilarities = ast.literal_eval(tags[tagIndex]) # get the line of similarities for this tag, parse the string as a list
        return tagSimilarities

def showCloud(tagSimilarities):
    tagCloud = []
    mainTag = tagSimilarities[0][0] #tag that our cloud will be built around
    tagCount = len(tagSimilarities)
    minTagWeight = tagSimilarities[tagCount-1][1]
    mainTagWeight = tagSimilarities[0][1]
    normalizedMainTagWeight = 1.25*100*(mainTagWeight-minTagWeight)   #subtract minTagWeight to normalize, rescale by 1.25 * 100
    tagCloud.append((mainTag, normalizedMainTagWeight))               #append (tag, weight) to be computed by tag cloud
    for index, piece in enumerate(tagSimilarities):
        if index > 1:
            tagCloud.append((tagSimilarities[index][0], 100*(tagSimilarities[index][1]-minTagWeight)))
    tags = make_tags(tagCloud, maxsize=100)
    create_tag_image(tags, 'cloud.png', size=(900, 600), fontname='Lobster')
    webbrowser.open('cloud.png')

if __name__=='__main__':
    tagIndex = 96  # index (line number minus 1) of tag to be displayed from "ComputedTags.txt"
    showCloud(getSimilarities(tagIndex))
   
