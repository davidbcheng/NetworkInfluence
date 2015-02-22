# Load graph from json into graphtool format
# Parse though graph name into numPlayers and numSeeds

from graph_tool.all import *
import json

def load(graphName):
	args = graphName.split('.')
	numPlayers = int(args[0])
	numSeeds = int(args[1])
	filename = '../data/' + graphName + '.json'
	numTrials = 50

	with open (filename, "r") as myfile:
		data = myfile.read().replace('\n', '')#.replace('"', '')
	dataDict = json.loads(data)

	g = Graph()
	vlist = g.add_vertex(len(dataDict))

	for i in xrange(len(dataDict)):
		node = str(i)
		for neighbor in dataDict[node]:
			g.add_edge(g.vertex(int(node)), g.vertex(int(neighbor)))

	return g, numPlayers, numSeeds, numTrials