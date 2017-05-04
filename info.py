#!python3
from sys import argv
from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser
import sys
import math

class InfoParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.title = ""
    self.words = []
    self.intag = None
    self.ignore = ["script", "link", "style"]

  def __str__(self):
    return "\tDocument title: " + self.title + \
           "\n\tSize: " + str(len(self.words)) + " words"

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
      self.words.append(word.lower())

  def count(self, s):
    """ Counts the occurences of the given string, allowing skip bigrams. """
    words = self.words
    sp = s.split()

    # If there is only one word to count, no need to use any fanciness
    if len(sp) == 1:
      return words.count(s)

    # Otherwise, we need to account for skip bigrams
    count = 0
    spindex = 0
    index = 0
    skipped = 0

    # Iterate through all of the words in the document
    while index < len(words):
      # If the current word is the one we're looking for
      if words[index] == sp[spindex]:
        # If the current word we're looking for is the last one
        if spindex == len(sp) - 1:
          # Increase the 'found' count by 1 and reset the current word we're
          # looking for to the first word
          count += 1
          spindex = 0
        else:
          # Otherwise, we've found the current word and should move onto the next
          # to check if we have a match for the entire phrase
          spindex += 1

        # No matter what, we'll always reset the skipped to 0 if we found the
        # word in time
        # And we will also move onto the next word
        skipped = 0
        index += 1
        continue
      
      # The current word was not one we're looking for, so increase the skip
      # index and the word index
      skipped += 1
      index += 1

      # If we've skipped 2 words, we've gone too far
      if skipped == 2:
        spindex = 0
        skipped = 0

    return count

  def bm25(self, query):
    """ Returns the bm25 score for the given query on the document """
    qs = query.split();
    N = len(qs)
    if (N == 0):
      print("You must specify a query")
      return
    D = len(self)
    if (D == 0):
      print("You must provide documents")
      return
    dlengths = [len(i) for i in self]
    avg_length = sum(dlengths) / D
    print("Average document length:", avg_length)
    result = {}
    counts = [searchDocument(d, qs) for d in self]
    qn = [0] * N
    for result in counts:
      for x in range(0, N):
        if (result[x] > 0): # count > 0, inc n(qi)
          qn[x] = qn[x] + 1
    idf = [IDF(D, qn_i) for qn_i in qn]
    scores = []
    for d in range(0, D):
      length = dlengths[d]
      count = counts[d]
      score = 0
      for i in range(0, N):
        tfreq = float(count[i]) / length
        numer = tfreq * (k1 + 1)
        denom = (tfreq) + (k1 * (1 - b + (b * length / avg_length)))
        score = score + (idf[i] * numer / denom)
      scores.append(score)
    return scores

# constants
k1 = 1.2
b = 0.75
IDF_FLOOR = 0.1

def IDF(N, qcnt):
  numer = (N - qcnt) + 0.5
  denom = qcnt + 0.5
  val = math.log(numer / denom)
  if (val < IDF_FLOOR):
    val = IDF_FLOOR
  return val

def parse(files):
  data = {}
  for path in files:
    print("Parsing " + path)
    parser = InfoParser()
    content = ""
    with open(path, 'r') as file:
      content = file.read()
    
    parser.data = ""

    parser.feed(content)
    print(parser)
    data[path] = parser

  return data


def main():
  if len(argv) < 2:
    print("Specify a dataset folder", file=sys.stderr)
    return -1
  folder = argv[1] if argv[1].endswith('/') else argv[1] + '/'
  files = [folder + f for f in listdir(folder) if isfile(join(folder, f))]
  print("Analyzing dataset in folder: ", folder)
  data = parse(files)

  print("Count occurence of 'adams'")
  for p in data:
    print("Path " + p + " score: " + bm25(data[p], "adams"))


if __name__ == "__main__":
  main()