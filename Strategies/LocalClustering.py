from graph_tool.all import *
from setup import *
import sys
import heapq

# All strategies need these two lines to set up the graph
graphName = sys.argv[1]
g, numPlayers, numSeeds, numTrials = load(graphName)


# Main Algorithm
clusters = graph_tool.clustering.local_clustering(g)
clusters = clusters.get_array()
heap = [(elem, ind) for ind, elem in enumerate(clusters)]
heapq.heapify(heap)
largestN = heapq.nlargest(numSeeds, heap)

seeds = [tup[1] for tup in largestN]

# Write to file
with open("Results/%s.%s" % (graphName, __file__[:-3]), 'w') as myfile:
	for i in xrange(numTrials):
		for node in seeds:
			myfile.write("%d\n" % node)
