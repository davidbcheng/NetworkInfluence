from graph_tool.all import *
import json
import sys

numPlayers = 1
numSeeds = 2
numTrials = 50

with open ("../data/example", "r") as myfile:
	data = myfile.read().replace('\n', '')#.replace('"', '')
dataDict = json.loads(data)

g = Graph()
vlist = g.add_vertex(len(dataDict))

for i in xrange(len(dataDict)):
	node = str(i)
	for neighbor in dataDict[node]:
		g.add_edge(g.vertex(int(node)), g.vertex(int(neighbor)))

seeds = []
currMax = 0
while len(seeds) < numSeeds:
	for v in g.vertices():
		if v.out_degree() > currMax and int(v) not in seeds:
			currMax = v.out_degree()
			mostDegreeVertex = v
	currMax = 0
	seeds.append(int(mostDegreeVertex))

with open("%sResults" % __file__[:-2], 'w') as myfile:
	for node in seeds:
		myfile.write("%d\n" % node)
