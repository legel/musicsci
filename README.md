####In a terminal, run the following:
`python GetTagData.py`

- downloads names and IDs of top 1000 artists from Last.fm API
- downloads up to 100 tag genres for each artist
- records the cooccurrence of each tag with every other tag as a list of dictionaries
- filters tags that appear less than 5 times
- saves TagNames.txt and TagCooccurrences.txt
___
`python ComputeTagSimilarities.py`

- loads files from previous script
- computes the similarity of each tag with every other tag using cosine similarity
- saves TagSimilarities.txt
___
`python CompareSimilarityMetrics.py`

- gets data from Last.fm's API method tag.getsimilar
- computes intersections and differences of our similarity sets with Last.fm's
- examines 10 matches and differences across random tags more closely, and returns a few points of statistics
- plots a histogram showing total cross-over between Last.fm's API and our similarity metric
- saves file SimilarTagMatches.txt
___
`pip install pytagcloud`
`apt-get install python-pygame`
`pip install simplejson`
`python TagCloud.py`

- given a tag index, visualizes by size the similarities of other tags to it
- saves output as cloud.png, would be easy to print more clouds as desired

___
####File Descriptions:
`TagCooccurrences.txt` - Vectors of cooccurrence of each tag with every other tag, formatted as a list of dictionaries [ {d1}, {d2}, ...] with each dictionary giving non-zero counts with the tag number of the dictionary and every other tag.  e.g. "d2" may be {t1:7, t4:1, ...}, means that t2 and t1 cooccur 7 times; t2 and t4 coccur 1 time.

`TagSimilarities.txt` - Contains sets of tag similarities, with each set's first entry with 1.0 being the tag compared to every other. e.g. rock is [('rock', 1.0), ('alternative', 0.965), ('alternative rock', 0.96), ... ]

`SimilarTagMatches.txt` - Compares the 50 most similar tags returned by our similarity metric and Last.fm's similarity metric for 250 tags, and shows what tags are matching and what are different

`SimilarTagComparisonHistogram.png` - Histogram of intersection sizes between sets of similar tags by Last.fm and our metric
