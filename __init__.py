'''
Created on Feb 5, 2014

@author: karthik

Create a file with recommendations for all the 474 videos
Recommendations saved to video_recommendations.json
'''
import json
from youtube_tag_recommend.single_recommendation import recommend_videos

if __name__ == '__main__':
  # Read the tagged videos
  data = json.load(open("tagged_videos.json"))
  
  # Find recommendations for each of the 474 videos
  for i in range(474):
    print "Finding recommendations for video", i+1
    video = data[i]
    r = recommend_videos(data, video)
    print r
    data[i]["recommendations"] = [c for c,_ in r]
  
  # Write the recommendations to a file along with rest of the data
  with open('video_recommendations.json', 'w') as outfile:
    json.dump(data, outfile)
