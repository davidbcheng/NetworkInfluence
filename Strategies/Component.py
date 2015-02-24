from graph_tool.all import *
from setup import *
import sys
import heapq

# All strategies need these two lines to set up the graph
graphName = sys.argv[1]
g, numPlayers, numSeeds, numTrials = load(graphName)

seeds = []

comp, hist, is_attractor = graph_tool.topology.label_components(g, attractors=True)
print comp.a


# # Write to file
# with open("../Results/%s.%s" % (graphName, __file__[:-3]), 'w') as myfile:
# 	for i in xrange(numTrials):
# 		for node in seeds:
# 			myfile.write("%d\n" % node)
