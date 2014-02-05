FEM-YouTube-Video-Tagging
=========================

Video tagging task from FEM Inc

Here is an outline of my method

Proper noun detection
---------------------
Since the data set is quite small, I figured that I will have to first discern the people in the video data to be able to do any meaningful tagging/recommendation. So, I resorted to NLP to get the proper nouns from the video titles and descriptions. I tried NLTK and Stanford's NER and got better results with the latter. 

Data scraping
-------------
Once I had the proper nouns, I was able to filter the more popular names by querying IMDB and see if there exists a page for the same name. One by-product of this step is that I was also able to get the IMDB IDs for the names which did have a page. 
I scrapped IMDB again for 1000 popular movies released between 2010-2014. I also got the most popular 400 TV shows released between 1985-2014.
Using the above scraped data for the popular movies and TV shows, I used the OMDBAPI which you recommended to fetch the cast and directors in for each of the movie and TV show.
This gave me a bunch of names which I merged with the names I learned through NLP. I now have data sets for the most probable names, movies and TV shows
All the scraping happens in under 5 mins

Tagging
-------
I used regular expressions to match the names of actors/movies/shows 
Made sure there are no partial matches. Tag only when whole words match
The whole tagging process takes less than 2 seconds

Recommendation
--------------
I used a weighted score model to score every other video with respect to a given video
Videos which successfully get tagged are used to recommend other videos with the same tag. Higher the number of common tags, greater the score. This parameter has the largest weight
I also weigh in the number of common categories. This is weighed moderately
For a third weighted parameter, I used fuzzy string matching using Levenshtein distance which measures the similarity of two given strings. I do such a string matching between the titles and the descriptions to match videos from similar sources. This parameter comes handy when there are no common tags and same number of common categories. 
I recommend five videos with the highest scores
The string matching step is actually a bit computationally expensive, so it can be modified/skipped if necessary
Recommending videos take between 3-6 seconds for each input video
Use "python youtube_recommend.py VIDEO_ID" to get recommendations
