#!python3
from sys import argv
from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser
import rank
import sys
import math
import string

BM25_MULTIPLIER = 1.5

class InfoParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.translator = str.maketrans('', '', string.punctuation)
    self.title = ""
    self.words = []
    self.intag = None
    self.ignore = ["script", "link", "style"]

  def __str__(self):
    return "\tDocument title: " + self.title + \
           "\n\tSize: " + str(len(self.words)) + " words"

  def feed(self, document):
    self.words.clear()
    return super().feed(document)

  def handle_starttag(self, tag, attrs):
    if tag == "h1" and ('id', 'firstHeading') in attrs:
      self.intag = "TITLE"
    elif tag in self.ignore:
      self.intag = "IGNORE"

  def handle_endtag(self, tag):
    if tag == "h1" and self.intag == "TITLE":
      self.intag = None
    elif tag in self.ignore:
      self.intag = None

  def handle_data(self, tag):
    if self.intag == "TITLE":
      self.title = tag
    elif self.intag == "IGNORE":
      return
    for word in tag.split():
      if word == "\n":
        continue
      self.words.append(word.lower().translate(self.translator))

  def getWords(self):
    return self.words

def parse(files):
  data = {}
  for path in files:
    print("Parsing " + path)
    parser = InfoParser()

    with open(path, 'r') as file:
      content = file.read()
      parser.feed(content)
      data[path] = parser.getWords()

  return data


def main():
  if len(argv) < 3:
    print("Usage: info <dataset folder> <search phrase>", file=sys.stderr)
    return -1
  folder = argv[1] if argv[1].endswith('/') else argv[1] + '/'
  files = [folder + f for f in listdir(folder) if isfile(join(folder, f))]
  phrase = (" ".join(argv[2:len(argv)])).lower()

  print("Analyzing dataset in folder: ", folder)
  dataset = parse(files)

  data = [(p, dataset[p]) for p in dataset]

  scores = [[] for _ in data]
  if len(argv) - 2 > 1:
    print("Finding the best skip-bigram matches...")
    scores = [[rank.countBigrams(doc[1], phrase)] for doc in data]
  else:
    print("Ignoring skip-bigram matches since only one word is being searched for")

  print("Applying bm25 algorithm to dataset...")
  
  bm25data = [d[1] for d in data]
  bm25result = rank.bm25(bm25data, phrase)

  for i in range(len(bm25data)):
    scores[i].append(bm25result[i] * BM25_MULTIPLIER)
    scores[i] = sum(scores[i])

  bestscore = (0, None)
  final = []
  for i in range(len(scores)):
    if scores[i] > bestscore[0]:
      bestscore = (scores[i], data[i][0])
    final.append((scores[i], data[i][0]))

  sortedfinal = sorted(final, key = lambda tup: tup[0])

  print("Documents score, sorted from highest to lowest:")
  for s in sortedfinal:
    print("\t" + s[1] + " => " + str(s[0]))

  if bestscore[1]:
    print("The document which best matched the search was: " + bestscore[1])
  else:
    print("We didn't find any documents matching your search")


if __name__ == "__main__":
  main()