'''
Created on Feb 1, 2014

@author: karthikputhraya@gmail.com
'''

from bs4 import BeautifulSoup
import requests, json

"""
Scrap the top n*100 movies which were released between the yr_start and yr_end 
"""
def get_top_movies(yr_start, yr_end, n):
  movies = []
  count =1
  for i in range(n):
    search_url = "http://www.imdb.com/search/title?at=0&sort=moviemeter,asc&title_type=feature&count=100&start="+str(i*100+1)+"&year="+str(yr_start)+","+str(yr_end)
    page = requests.get(search_url).text
    soup = BeautifulSoup(page)
    for movie in soup.find_all("tr", class_="even detailed")+soup.find_all("tr", class_="odd detailed"):
      title = movie.find_all("td")[2].a
      imdb_id, imdb_title = title.get('href')[-10:-1], title.string
      print count, imdb_id, imdb_title
      count += 1
      movies.append((imdb_id, imdb_title))
  return movies
  
"""
Scrap the top n*100 TV shows which were released between the yr_start and yr_end 
"""
def get_top_tv(yr_start, yr_end, n):
  tv = []
  count =1
  for i in range(n):
    search_url = "http://www.imdb.com/search/title?at=0&sort=moviemeter,asc&title_type=tv_series&count=100&start="+str(i*100+1)+"&year="+str(yr_start)+","+str(yr_end)
    page = requests.get(search_url).text
    soup = BeautifulSoup(page)
    for movie in soup.find_all("tr", class_="even detailed")+soup.find_all("tr", class_="odd detailed"):
      title = movie.find_all("td")[2].a
      imdb_id, imdb_title = title.get('href')[-10:-1], title.string
      print count, imdb_id, imdb_title
      count += 1
      tv.append((imdb_id, imdb_title))
  return tv
  
"""
Get the most likely IMDB id for the actor with 'name'. None if the name does not belong to a popular person
"""
def get_actor_imdb_id(name):
  page = requests.get("http://www.imdb.com/search/name?name="+name).text
  soup = BeautifulSoup(page)
  for l in soup.find_all("td", class_="name"):
    imdb_id = l.a.get('href')[-10:-1]
    imdb_name = l.a.string
    return (imdb_id, imdb_name)

"""
Get all the people (actors and directors) associated with a movie/TV show from OMDB
"""
def get_omdb_people(imdb_id):
  page = requests.get("http://www.omdbapi.com/?i="+imdb_id).text
  json_data=json.loads(page)
  return json_data["Actors"].split(", ")+json_data["Director"].split(", ")

# if __name__ == '__main__':
#   res = get_top_movies(1985, 2014, 10)
#   with open('imdb_top_movies.json', 'w') as outfile:
#     json.dump(res, outfile)
#   res = get_top_tv(2010, 2014, 3)
#   with open('imdb_top_tv.json', 'w') as outfile:
#     json.dump(res, outfile)
# 
#   l = get_omdb_people("tt0133093")
#   print l
#   print type(l), len(l)
#   