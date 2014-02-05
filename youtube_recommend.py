#! /usr/bin/python

'''
Created on Feb 4, 2014

@author: karthik
'''
import nltk, json
import sys

"""
Compute the similarity of two strings. The function returns
the Levenshtein distance between the two strings. Smaller the
distance, more similar are the strings
"""
def fuzzy_text_match(text1, text2):
  return nltk.metrics.edit_distance(text1, text2)

"""
Return the top five recommendations for the target video 
from the given data
"""
def recommend_videos(data, target):
  a, b, c = 100, 10, 1 # Weights for the scoring algorithm 
  recommendations = []
  
  # All the tags corresponding to the target video
  tags = target["tag1"] + target["tag2"]
  
  # Compute the recommendation score for each video
  for video in data:
    score = 0
    if video == target: continue
    
    # The score is computed as a weighted mean of three different parameters. 
    # 'a' weights the number of common 'tags' between the two videos. This has the highest weight
    # 'b' weights the number of common 'categories' between the two videos
    # 'c' weighs the dissimilarity between the video titles and descriptions
    score = (a * len(set(tags) & (set(video["tag1"]) | set(video["tag2"]))) + 
             b * len(set(target["categories"]) & set(video["categories"])) +
             -c * (min(fuzzy_text_match(target["title"], video["title"]), 
                       fuzzy_text_match(target["description"], video["description"]))+1))
    
#     print video["id"], score
    recommendations.append((video["id"], score))
  
  # Sort the videos according to the computed scores. This can be done in linear
  # time using k-th order statistics if the number of videos is very large
  recommendations.sort(key=lambda tup: tup[1], reverse=True)
  
#   print "\n", recommendations[:5], "\n"
  
  # Return the top five recommendations and their scores
  return recommendations[:5]


if __name__ == '__main__':
  if len(sys.argv) != 2 or not (1 <= int(sys.argv[1]) <= 474): 
    print "Usage: youtube_recommend [VIDEO_ID]"
    print "Enter the ID of the video between 1-474. The program will print the"
    print "five most recommended videos relating to the input video. The data"
    print "needs to have been scrapped and tagged before recommendation. Please"
    print "run scrape_data.py and youtube_tag.py before using recommendation."
    sys.exit()
    
  # Read the tagged videos
  data    = json.load(open("tagged_videos.json"))
  
  vid = data[int(sys.argv[1])-1]
#   vid = data[274-1]
  
  # Print the original video and the recommendations
  # Use unicode to deal with pesky accented names
  print "Input video:"
  print "------------"
  print "ID ", vid["id"]
  print u"\n". join([vid["title"], vid["description"]]).encode('utf-8') 
  print u"Tag1: ", ", ".join(vid["tag1"]).encode('utf-8')
  print u"Tag2: ", ", ".join(vid["tag2"]).encode('utf-8')

  r = recommend_videos(data, vid)
  print "\nRecommendations"
  print "---------------"
  for id,_ in r:
    print "ID: ", id
    print u"\n". join([data[id-1]["title"], data[id-1]["description"]]).encode('utf-8')
    print u"Tag1:", ", ".join(data[id-1]["tag1"]).encode('utf-8')
    print u"Tag2:", ", ".join(data[id-1]["tag2"]).encode('utf-8'), "\n\n"
