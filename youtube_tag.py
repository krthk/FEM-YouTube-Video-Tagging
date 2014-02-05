import json, re, string

"""
Check if a particular phrase is contained in the sentence
"""
def match_phrase(phrase, sentence):
  # Deal with special characters
  for c in "-./[]\*+?(){}|":
    if c in phrase:
      phrase = string.replace(phrase, c, '\\' + c) 
  
  # Regexp word matching
  regex = r'\b' + phrase + r'\b'  
  return re.search(regex, sentence) != None
  
if __name__ == '__main__':
  # Load the dataset to be tagged and all the scraped data
  data    = json.load(open("CodeAssignmentDataSet.json"))
  people  = json.load(open("famous_people.json"))
  movies  = json.load(open("imdb_top_movies.json"))
  tv      = json.load(open("imdb_top_tv.json"))

  tagged_videos = []
  vid = 1
  for video in data:
    # Create two tag sets. tag1 for people and tag2 for movie/TV shows
    tag1, tag2 = set([]), set([])
    
    text = u'\n'.join(((video["title"]), (video["description"]))).encode('utf-8')
    print vid, "\n", text
    
    # Clean up proper nouns in the text
    text = text.replace("'s", "")
    text = text.replace("s'", "s")

    # Get people related tags
    for item in people: 
      if (item) in text: 
        text = text.replace(item, "")
        tag1.add(item)
        
    # Get TV show related tags
    for _,item in tv: 
      if not any(c.isalpha() for c in item): continue
      if (item) in text and match_phrase(item, text): 
        text = text.replace(item, "")
        tag2.add(item)

    # Get movie related tags
    for _,item in movies: 
      if not any(c.isalpha() for c in item): continue
      if (item) in text and match_phrase(item, text): 
        tag2.add(item)
    
    print u"Tags: " + u", ".join(list(tag1 | tag2)).encode('utf-8')
    print

    video["id"]   = vid
    video["tag1"] = list(tag1)
    video["tag2"] = list(tag2)
    tagged_videos.append(video)
    vid += 1
  
  # Write the tags to a file along with the rest of the data
  with open('tagged_videos.json', 'w') as outfile:
    json.dump(tagged_videos, outfile)
    
