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

pos = nx.spring_layout(g)
highest_deg = [1, 2, 5, 6, 11, 40, 58, 59, 93, 213]
# TA_more = [2, 5, 6, 11, 40, 58, 59, 93, 193, 201, 213, 245]
TA_more = map(int, ['6', '40', '24', '11', '93', '211', '59', '58', '213', '159', '5', '1'])
overlap = [i for i in highest_deg if i in TA_more]


nx.draw(g)
nx.draw_networkx_nodes(g, pos, highest_deg, node_color='b', node_size=500)
nx.draw_networkx_nodes(g, pos, TA_more, node_color='g', node_size=500)
nx.draw_networkx_nodes(g, pos, overlap, node_color='y', node_size=500)
plt.show()

# return g