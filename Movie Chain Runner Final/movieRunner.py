from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search

import copy
# from pygraph.readwrite.dot import write

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool



NUM_MOVIES = 6561
movieFileLoc = "/Users/tanayvarma/Desktop/MOVIES.LST"
print "Started"
FILLDEPTH = 10
expandAll = False

movieGraph = digraph()
movieArray = []
moviesToCheck = []
preProcessMovies = []
def readMovies():
	movieNum = 0
	with open(movieFileLoc) as movieList:
		for line in movieList:
			movieGraph.add_node(movieNum)
			movieArray.append(line[:-1])
			movieNum += 1

def preProcess():
	for i in xrange(NUM_MOVIES):
		split = movieArray[i].split(" ")
		preString = ""
		postString = ""
		preSubStrings = []
		postSubStrings = []
		l = len(split)
		for i in xrange(l):
			preString = split[l - 1 -i] + preString
			postString += split[i]
			preSubStrings.append(preString)
			postSubStrings.append(postString)
			preString = " " + preString
			postString += " "
		preProcessMovies.append((preSubStrings,postSubStrings,len(split)))



def overlap(f,s):
	if f == s:
		return False

	postStrings = preProcessMovies[f][0]
	preStrings = preProcessMovies[s][1]

	i = 0
	# print f , s
	while( i < min(preProcessMovies[f][2],preProcessMovies[s][2])):
		if preStrings[i] == postStrings[i]:
			# print movieArray[f], "|", movieArray[s]
			return True
		i += 1

	return False

def addEdges():
	ctr = 0
	for prevMovie in xrange(NUM_MOVIES):
		for nextMovie in xrange(NUM_MOVIES):
			# print ctr
			# 	ctr += 1
			if prevMovie != nextMovie:
				if overlap(prevMovie,nextMovie):
					movieGraph.add_edge((prevMovie,nextMovie))


def moviesToStartSearchWith():
	
    for i in xrange(NUM_MOVIES):
        nextMovies = movieGraph.neighbors(i)
        prevMovies = movieGraph.incidents(i)

        if (nextMovies == []):
            continue

        if (len(nextMovies) == 1 and len(prevMovies) == 1):
            continue

        moviesToCheck.append(i)


def makeInitialChains(startMovie):
	s1 = set([startMovie])
	s2 = set([])
	count = 0
	distance = [-NUM_MOVIES] * NUM_MOVIES 
	chains = [[]] * NUM_MOVIES
	chains[startMovie].append(startMovie)
	while (count < NUM_MOVIES and len(s1) != 0):
		for currMovie in s1:
			for nextMovie in movieGraph.neighbors(currMovie):
				currDistance = distance[currMovie];
				maxDistance = 10000000000
				if (distance[nextMovie] > currDistance + maxDistance):
					if nextMovie in s2:
						continue

				if (distance[nextMovie] == -NUM_MOVIES or nextMovie not in chains[currMovie]):
					distance[nextMovie] = currDistance + 1
					chains[nextMovie] = copy.deepcopy(chains[currMovie])
					chains[nextMovie].append(nextMovie)
					s2.add(nextMovie)
		# print "s1 = " , printMovies(list(s1)),"s2 = ", printMovies(list(s2))
		(s1,s2) = (s2,s1)
		# print "s1 = " , printMovies(list(s1)),"s2 = ", printMovies(list(s2))
		s2.clear()
		count += 1
		# print len(s1), count

	maxLen = 0
	retVal = 0
	for x in chains:
		if len(x) > maxLen:
			maxLen = len(x)
			retVal = x

	return retVal



def makeInitialChains1(startMovie):
	s1 = set([startMovie])
	s2 = set([])
	count = 0
	distance = [-NUM_MOVIES] * NUM_MOVIES 
	chains = [[]] * NUM_MOVIES
	chains[startMovie].append(startMovie)
	while (count < NUM_MOVIES and len(s1) != 0):
		for currMovie in s1:
			for nextMovie in movieGraph.neighbors(currMovie):
				currDistance = distance[currMovie];
				maxDistance = 19
				if (distance[nextMovie] > currDistance + maxDistance):
					if nextMovie in s2:
						continue

				if (distance[nextMovie] == -NUM_MOVIES or nextMovie not in chains[currMovie]):
					distance[nextMovie] = currDistance + 1
					chains[nextMovie] = copy.deepcopy(chains[currMovie])
					chains[nextMovie].append(nextMovie)
					s2.add(nextMovie)
		# print "s1 = " , printMovies(list(s1)),"s2 = ", printMovies(list(s2))
		(s1,s2) = (s2,s1)
		# print "s1 = " , printMovies(list(s1)),"s2 = ", printMovies(list(s2))
		s2.clear()
		count += 1
		# print len(s1), count

	chains.sort(lambda x,y: cmp(len(y),len(x)))
	# print len(chains[0])

	maxLs = 20
	if expandAll: 
		if len(chains) < maxLs:
			end = len(chains)
		else: 
			end = maxLs
	else: end = 1


	for i in xrange(end):
		longChain = copy.deepcopy(chains[i])
		if(len(longChain) > 150):
			longerChain = extendChain(longChain)

			while(len(longerChain) > len(longChain)):
				longChain = copy.deepcopy(longerChain)
				longerChain = extendChain(longChain)

		chains[i] = copy.deepcopy(longChain)

	if(expandAll):
		chains.sort(lambda x,y: cmp(len(y),len(x)))

	longChain = chains[0]
	return longChain


def find(l,x):
	if x in l:
		return l.index(x)
	else:
		return -1


def findNewChain(start,chainSegment,alreadyInChain,currentChain):
	
	# chainSegment is a list of movies starting with movie Start, and alreadyInChain
	# has all the movies that were in the original longChain
	#Current chain is what we are trying to maximise, to longer than the chainSegment
	
	# if we have recursed FILLDEPTH times stop recursing
	if len(currentChain) == FILLDEPTH:
		return currentChain

	#currentChain keeps track of recursion depth
	currentChain.append(start)

	bestList = []

	neighbors = movieGraph.neighbors(start)
	currDepth = len(currentChain)

	for i in xrange(len(neighbors)):
		#movie that connects from start movie
		nextMovie = neighbors[i]

		#If this is the movie already in chainSegment then do nothing
		if currDepth < len(chainSegment) and chainSegment[currDepth] == nextMovie:
			continue

		# checks if nextMovie is in our chainSegment
		indexEnd = find(chainSegment,nextMovie)

		# if movie not in current segment but in longer chain do nothing
		# because there are at least filldepth movies in the middle of start and next movie
		# in longer chain it doesnt make sense to change that here so do nothing
		if alreadyInChain[nextMovie] == 1 and indexEnd == -1:
			continue

		#We already put nextMovie in current chain and there is a cycle here so do nothing
		if nextMovie in currentChain:
			continue

		p = []

		if indexEnd >= 0 and indexEnd < currDepth:
	
			p = copy.deepcopy(currentChain)
			#Add all the movies from nextMovie in chainSegment to end of currentChain
			for j in xrange(indexEnd , len(chainSegment)):
				#However if any movie already in currentChain reset p and break
				n = chainSegment[j]

				if n in p:
					p = []
					break

				p.append(n)

			#update bestList if p is better
			if len(p) > len(bestList):
				bestList = copy.deepcopy(p)

		#call findNewChain again with nextMovie as start and currentChain having startMovie
		p = findNewChain(nextMovie,chainSegment,alreadyInChain,copy.deepcopy(currentChain))


		#update bestList if p is better
		if p != [] and len(p) > len(bestList):
			bestList = copy.deepcopy(p)

	return bestList



def extendChain(longestChain):
	margin = FILLDEPTH
	# chainSet = set(longestChain)
	alreadyInChain = [0] * NUM_MOVIES

	# update all the movies already in longerChain to 1
	for x in longestChain:
		alreadyInChain[x] = 1
	i = 0
	while( i < len(longestChain) - margin -1 ):
		i += 1
		nextChain = []
		# Create a chain of length margin starting from index i
		for j in xrange(margin):
			nextChain.append(longestChain[i+j])
		
		#current movie to find a new chain from
		start = longestChain[i]

		#retChain is the best possible Chain starting from Start and ending the last element of nextChain
		retChain = findNewChain(start,nextChain,alreadyInChain,[])

		if len(retChain) > len(nextChain):
			# print start, i, "....", retChain, "....................", nextChain
			# print len(longestChain)
			assert(retChain[0] == nextChain[0])
			assert(retChain[-1] == nextChain[-1])

			#We remove the nextChain segment from longerList
			for j in xrange(margin):
				alreadyInChain[longestChain[i]] = 0
				longestChain = longestChain[:i] + longestChain[i+1:]

			#Add the chain segment back to longerChain and update AlreadyInChain
			for j in xrange(len(retChain)):
				alreadyInChain[retChain[j]] = 1
				longestChain = longestChain[:i+j] + [retChain[j]] + longestChain[i+j:]

			# print len(longestChain)
			assert(longestChain[i] == nextChain[0])

	return longestChain
	



def printMovies(l):
	a = ""
	for x in l:
		a += movieArray[x] + " | "
	return a


readMovies()

preProcess()
# print preProcessMovies
addEdges()


moviesToStartSearchWith()
print len(moviesToCheck)
# # print printMovies(makeInitialChains1(5))
# b =  makeInitialChains1(147)
# # print b.count("|")
# for i in xrange(len(b)-1):
# 	if overlap(b[i],b[i+1]) == False:
# 		print i , ":", b[i], b[i+1]
#  		# assert False

# print
# print
# print len(b)
# print printMovies(b)

moviesToCheck1 = [42,45,47,50,54,56,60,67,69,72,76,77,92,103,107,108,116,120,124,137,139,142,145,147,148,151,155,161,162,165]
moviesToCheck2 = moviesToCheck[2000:2965]
moviesToCheck3 = [3661, 3717]
maxLen = 0
retVal = 0
for movie in moviesToCheck2:
	b = makeInitialChains1(movie)
	len_b = len(b)
	print movie, "-", len_b
	if(len_b > maxLen):
		maxLen = len_b
		retVal = b

print
print
print len(retVal)
print printMovies(retVal)


# pool = ThreadPool(4)
# results = pool.map(makeInitialChains,moviesToCheck[:4])


# for x in results:
# 	if len(x) > maxLen:
# 		maxLen = len(x)
# 		retVal = x


# expandAll = True
# extendChain(retVal)
# print(printMovies(retVal))

# for x in xrange(1):
# 	print moviesToCheck[], 

# print len(makeInitialChains1(moviesToCheck[3383]))

# for x in results:
# 	print x[0] , len(x)








