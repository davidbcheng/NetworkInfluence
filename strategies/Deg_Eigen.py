from graph_tool.all import *
from setup import *
import sys
import heapq

# All strategies need these two lines to set up the graph
graphName = sys.argv[1]
g, numPlayers, numSeeds, numTrials = load(graphName)

seeds = []
currMax = 0
while len(seeds) < numSeeds-5:
	for v in g.vertices():
		if v.out_degree() > currMax and int(v) not in seeds:
			currMax = v.out_degree()
			mostDegreeVertex = v
	print currMax
	currMax = 0
	seeds.append(int(mostDegreeVertex))

# Main Algorithm
vertex,edge = graph_tool.centrality.betweenness(g)
verticies = vertex.get_array()
heap = [(elem, ind) for ind, elem in enumerate(verticies)]
heapq.heapify(heap)
while len(seeds) < numSeeds:
	(temp, seed) = heapq.heappop(heap)
	if seed not in seeds:
		seeds.append(seed)

# currMax = 0
# v = g.vertex(seeds[7])
# for w in v.out_neighbours():
# 	print int(w)
# 	if w.out_degree() > currMax and int(w) not in seeds and int(w) != 107 and int(w) != 145:
# 		currMax = w.out_degree()
# 		best = w

# seeds.append(int(best))

# seeds.append(101)
# seeds.append(108)


# Write to file
with open("../seeds/%s.%s" % (graphName, __file__[:-3]), 'w') as myfile:
	for i in xrange(numTrials):
		for node in seeds:
			myfile.write("%d\n" % node)
