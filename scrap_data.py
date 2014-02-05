'''
Created on Feb 1, 2014

@author: karthikputhraya@gmail.com
'''

import json
from youtube_tag.nlp import extract_entities
from youtube_tag.imdb_parse import get_actor_imdb_id, get_omdb_people,\
  get_top_movies, get_top_tv

"""
Use NLP to get all the possible proper nouns from the video 
descriptions and titles. Verify against IMDB if the names belong 
a famous person
"""
def get_proper_nouns(json_file):
  # Read and load the data file
  json_data=open(json_file)
  data = json.load(json_data)
  json_data.close()
  
  names = set([])
  
  # Extract proper nouns from the description and title of the videos
  for video in data:
    description = video["description"] + "\n" + video["title"]
    names |= extract_entities(description)
  
  # Check the extracted nouns against IMDB
  valid_names = set([])
  for name in names:
    imdb_data = get_actor_imdb_id(name)
    if imdb_data != None:
      valid_names.add(imdb_data)
      print "Valid", name, imdb_data
    else:
      print "Invalid", name
      
  return valid_names
    
"""
Read a JSON file containing the names of popular movies/TV shows
and get the names of the people (actors and directors) associated 
with the movie/TV show from OMDB
"""
def get_all_people(json_file):
  # Read and load the data file
  json_data=open(json_file)
  data = json.load(json_data)
  json_data.close()
  
  names = set([])
  for movie in data:
    l = get_omdb_people(movie[0])
    print movie[1], l
    names |= set(l)
  return names
  
if __name__ == '__main__':
  # Read the dataset and use NLP to extract the names of popular
  # people from the data set. Write the names to 'names1.json'
  proper_nouns = get_proper_nouns("CodeAssignmentDataSet.json")
  with open('names1.json', 'w') as outfile:
    json.dump(list(proper_nouns), outfile)
   
  # Get the most popular 1000 movies released between 2010 and 2014 
  # Save the IMDB ID and movie titles to 'imdb_top_movies.json'
  res = get_top_movies(2010, 2014, 10)
  with open('imdb_top_movies.json', 'w') as outfile:
    json.dump(res, outfile)

  # Get the most popular 400 TV shows released between 1985 and 2014 
  # Save the IMDB ID and TV show titles to 'imdb_top_tv.json'
  res = get_top_tv(1985, 2014, 4)
  with open('imdb_top_tv.json', 'w') as outfile:
    json.dump(res, outfile)
 
  # Merge the popular names from TV shows and the movies in to one 
  # file named 'names2.json'
  p = set([])
  p |= get_all_people("imdb_top_tv.json")
  p |= get_all_people("imdb_top_movies.json")
  print p
  print len(p)
  with open('names2.json', 'w') as outfile:
    json.dump(list(p), outfile)
 
  # Merge the names scrapped from the web with the names learnt from the 
  # dataset. Save the final popular name dataset to file 'famous_people.json'
  json_data=open("names1.json")
  data1 = json.load(json_data)
  json_data.close()
  json_data=open("names2.json")
  data2 = set(json.load(json_data))
  json_data.close()
  print len(data2)
   
  for name in list(data1):
    if name[1] not in data2:
      print name[1]
      data2.add(name[1])
  print len(data2)
 
  with open('famous_people.json', 'w') as outfile:
    json.dump(list(data2), outfile)
    
