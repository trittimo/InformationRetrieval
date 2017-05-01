# bm25.py
# Implementation of Okapi BM25
# Andrew McKee and Michael Trittin


# constants
k1 = 1.2
b = 0.75

def IDF(N, qcnt):
	numer = (N - qcnt) + 0.5
	denom = qcnt + 0.5
	return math.log(numer / denom)

def searchDocument(doc, q):
	# TODO
	length = 0
	count = 0
	return length, count
	

def bm25(docs, query):
	qs = query.split();
	N = len(qs)
	if (N == 0):
		print "You must specify a query"
		return
	avg_length = 1 # average doc length: TODO
	result = {}
	for qi in qs:
		scores = []
		search = []
		n = 0
		for doc in docs:
			info = searchDocument(doc, qi)
			search.append(info)
			if (info[1] > 0): # count > 0, inc n(qi)
				n = n + 1
		idf = IDF(N, n)
		for i in range(0, len(search)):
			length = search[i][0]
			tfreq = search[i][1] / search[i][0]
			numer = tfreq * (k1 + 1)
			denom = (tfreq) + (k1 * (1 - b + (b * length / avg_length)))
			scores.append(idf * numer / denom)
		result[qi] = scores
	# Print result for debugging
	print "[DEBUG] Score Results: (Pre-Summation)"
	for key, value in d.iteritems():
		print key, ':', value
	# Compute final summed scores for the documents
	scores = []
	for i in range(0, N):
		score = 0
		for qscore in result:
			score += qscore[i]
		scores.append(score)
	# Print what we are returning
	print "[DEBUG] Final Scores:", scores
	return scores

