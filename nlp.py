'''
Created on Feb 1, 2014

@author: karthikputhraya@gmail.com
'''

import ner

"""
This function extracts possible proper nouns from the text using NLP.
I am using the well-known Stanford Named Entity Recognizer (NER) to 
extract the proper nouns. 
http://nlp.stanford.edu/software/CRF-NER.shtml

The function requires an interface to NER which can be setup as given
at this SO answer
https://stackoverflow.com/questions/15722802/how-do-i-use-python-interface-of-stanford-nernamed-entity-recogniser
"""
def extract_entities(text):
  print text
  tagger = ner.SocketNER(host='localhost', port=8080)
  tags = tagger.get_entities(text)
  if 'PERSON' in tags.keys(): 
    print tags['PERSON']
    print
    return set(tags['PERSON'])
  print
  return set([])
      
# if __name__ == '__main__':
#   sentence = "Beverly D'Angelo reads a copy of More in a meeting with Ari on the HBO Series Entourage."
#   print extract_entities(sentence)
#   print 
#   
  