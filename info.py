#!python3
from sys import argv
from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser

class BasicParser(HTMLParser):
  def __init__(self):
    super().__init__()
    self.data = ""

  def handle_data(self, tag):
    self.data += str(tag)

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

  def getskiplist(i, size):
    slist = []
    for skip in range(3):
      sl = []
      for a in range(size):
        for b in range(skip):



  def count(self, s):
    """ Counts the occurences of the given string, allowing skip bigrams. """
    sp = s.split()
    if len(sp) == 1:
      return self.words.count(s)

    count = 0    
    for word in range(len(self.words)):
      index = word
      if self.words[word] == sp[0]:
        if sp in self.getskiplist(word, len(sp)):
          count = count + 1
    return count

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
    print(p + " contains " + str(data[p].words.count("adams")) + " occurences of 'adams'")


if __name__ == "__main__":
  main()