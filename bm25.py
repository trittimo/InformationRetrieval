#! C:\Python27\python.exe

# bm25.py
# Implementation of Okapi BM25
# Andrew McKee and Michael Trittin

import math

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

def searchDocument(doc, qs):
  count = [0] * len(qs)
  for word in doc:
    for i in range(0, len(qs)):
      if (word == qs[i]):
        count[i] = count[i] + 1
  return count

def bm25(docs, query):
  qs = query.split();
  N = len(qs)
  if (N == 0):
    print "You must specify a query"
    return
  D = len(docs)
  if (D == 0):
    print "You must provide documents"
    return
  dlengths = [len(i) for i in docs]
  avg_length = reduce(lambda x, y: x + y, dlengths) / D
  print "Average document length:", avg_length
  result = {}
  print "Searching..."
  counts = [searchDocument(d, qs) for d in docs]
  #print "Counts:", counts
  print "Processing..."
  qn = [0] * N
  for result in counts:
    for x in range(0, N):
      if (result[x] > 0): # count > 0, inc n(qi)
        qn[x] = qn[x] + 1
  #print "qn:", qn
  idf = [IDF(D, qn_i) for qn_i in qn]
  #print "idf:", idf
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
      #print "Score: D=", d, "Q=", qs[i], "==>", score
    scores.append(score)
  # Print what we are returning
  print "Final Scores:", scores
  return scores

'''
docs = [
  ["a", "b", "c", "c"],
  ["a", "d", "d", "e"],
  ["a", "c", "d", "e"],
  ["b"],
  ["c"]
]

bm25(docs, "b")
bm25(docs, "a b")
'''