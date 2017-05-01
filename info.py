#!python3
import sys
from html.parser import HTMLParser

class InfoParser(HTMLParser):
  def handle_starttag(self, tag, attrs):
    print("Start tag: ", tag)

  def handle_endtag(self, tag):
    print("End tag: ", tag)

  def handle_data(self, tag):
    print("Data tag: ", tag)

def main():
  parser = InfoParser()
  parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')
  # TODO



if __name__ == "__main__":
  main()