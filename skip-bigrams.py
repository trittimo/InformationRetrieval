#!python3

def defCountBigram(words, query):
  """
  Counts the occurences of the query in the given word list.
  Accounts for bigrams, so if the word list contains
  ['abe', 'lincoln','was', 'assasinated'], and the query is 'lincoln assasinated',
  we'll still find 1 occurence.
  """

  queryWords = query.split()

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
    print("Analyzing " + word + " against " + qword)

    # We found an occurence of the current query word
    if word == qword:
      # In-case backtracking is needed, append the current wordIndex and the
      # number that have been skipped at this point in time
      wordResetIndex.append((wordIndex, queryIndex, skipped))

      # Reset skipped, go to the next word, and increase the query index
      skipped = 0
      wordIndex += 1
      queryIndex += 1

      # If we're at the last word in the query, we've successfuly found a match
      if queryIndex == len(queryWords):
        print("Found occurence: " + str(wordResetIndex))
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

  return count

print(str(defCountBigram("dogs and dogs and cats".split(), "dogs and cats")))
