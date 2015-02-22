from graph_tool.all import *
from loadGraph import *
import sys

# All strategies need these two lines to set up the graph
graphName = sys.argv[1]
g, numPlayers, numSeeds, numTrials = load(graphName)

seeds = []
currMax = 0
while len(seeds) < numSeeds:
	for v in g.vertices():
		if v.out_degree() > currMax and int(v) not in seeds:
			currMax = v.out_degree()
			mostDegreeVertex = v
	currMax = 0
	seeds.append(int(mostDegreeVertex))

# Write to file
with open("Results/%s.%s" % (graphName, __file__[:-3]), 'w') as myfile:
	for i in xrange(numTrials):
		for node in seeds:
			myfile.write("%d\n" % node)

