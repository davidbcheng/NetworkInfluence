from graph_tool.all import *
from setup import *
import sys
import heapq

# All strategies need these two lines to set up the graph
graphName = sys.argv[1]
g, numPlayers, numSeeds, numTrials = load(graphName)

seeds = []
currMax = 0
while len(seeds) < 8:
	for v in g.vertices():
		if v.out_degree() > currMax and int(v) not in seeds:
			currMax = v.out_degree()
			mostDegreeVertex = v
	currMax = 0
	seeds.append(int(mostDegreeVertex))

while len(seeds) < numSeeds:
	currMax = 0
	v = g.vertex(seeds[0])
	for w in v.out_neighbours():
		if w.out_degree() > currMax and int(w) not in seeds:
			currMax = w.out_degree()
			best = w
	seeds.append(int(best))


# Write to file
with open("../Results/%s.%s" % (graphName, __file__[:-3]), 'w') as myfile:
	for i in xrange(numTrials):
		for node in seeds:
			myfile.write("%d\n" % node)
