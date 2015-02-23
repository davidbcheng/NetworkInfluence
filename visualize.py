# Load graph from json into graphtool format
# Parse though graph name into numPlayers and numSeeds

import networkx as nx
import json
import sys
import matplotlib.pyplot as plt

graphName = sys.argv[1]
filename = './data/' + graphName + '.json'

with open (filename, "r") as myfile:
	data = myfile.read().replace('\n', '')#.replace('"', '')
dataDict = json.loads(data)

g = nx.Graph()
g.add_nodes_from(map(int, dataDict.keys()))

for i in xrange(len(dataDict)):
	node = str(i)
	for neighbor in dataDict[node]:
		g.add_edge(int(node), int(neighbor))

nx.draw(g)
plt.show()

# return g