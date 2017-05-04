#!python3
import math

def countBigrams(words, query):
  """
  Counts the occurences of the query in the given word list.
  Accounts for bigrams, so if the word list contains
  ['abe', 'lincoln','was', 'assasinated'], and the query is 'lincoln assasinated',
  we'll still find 1 occurence.
  """

  queryWords = query[0].split()

  # We don't need to do anything fancy for one word queries
  if len(queryWords) == 1:
    return words.count(query)

  count = 0
  wordIndex = 0
  queryIndex = 0
  wordResetIndex = []
  skipped = 0

  while wordIndex < len(words):
    word = words[wordIndex]
    qword = queryWords[queryIndex]
    #print("Analyzing " + word + " against " + qword)

    # We found an occurence of the current query word
    if word == qword:
      # In-case backtracking is needed, append the current wordIndex and the
      # number that have been skipped at this point in time
      wordResetIndex.append((wordIndex, queryIndex, skipped))

      # Reset skipped, go to the next word, and increase the query index
      skipped = 0
      wordIndex += 1
      queryIndex += 1

      # If we're at the last word in the query, we've successfully found a match
      if queryIndex == len(queryWords):
        count += 1

        # Reset the word index to just after the first occurence of the first word
        wordIndex = wordResetIndex[0][0] + 1
        wordResetIndex.clear()

        # And reset to the first word of the query
        queryIndex = 0
      continue

    # We haven't found an occurence of the current query word
    # If we've skipped too many, try to reset
    if skipped == 2:
      if wordResetIndex:
        wordIndex, queryIndex, skipped  = wordResetIndex.pop()
        wordIndex += 1
      else:
        # The occurence couldn't be found here: let it continue from current
        skipped = 0
        queryIndex = 0
        continue
    else:
      wordIndex += 1
      skipped += 1

  return [count]

# Constants
k1 = 1.2
b = 0.75
IDF_FLOOR = 0.1


# Inverse document frequency
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

def bm25(docs, query, searchFn = searchDocument):
  qs = searchFn == searchDocument and query.split() or [query];
  N = len(qs)
  if (N == 0):
    # print "You must specify a query"
    return
  D = len(docs)
  if (D == 0):
    # print "You must provide documents"
    return
  dlengths = [len(i) for i in docs]
  avg_length = sum(dlengths) / D
  # print "Average document length:", avg_length
  result = {}
  # print "Searching..."
  counts = [searchFn(d, qs) for d in docs]
  #print "Counts:", counts
  # print "Processing..."
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
      # print("Score: D=", d, "Q=", qs[i], "==>", score)
    scores.append(score)
  # Print what we are returning
  # print "Final Scores:", scores
  return scores