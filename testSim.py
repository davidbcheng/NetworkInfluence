# Usage:  python testSim.py <graphName> <results1> <results2> ...
# Example: python testSim.py 2.10.020 2.10.020.HighestDegree 2.10.020.LocalClustering

import sim
import sys
import json

def transform(filename):
	with open(filename, 'r') as myFile:
		data = myFile.read().split('\n')[:-1]
	result = []
	numSeeds = int(filename.split('.')[1])
	results = [data[i:i+numSeeds] for i in xrange(0, len(data), numSeeds)]
	return results

graphData = sys.argv[1]
strategies = sys.argv[2:]

with open ("./data/" + graphData + '.json', "r") as myfile:
	data = myfile.read().replace('\n', '')#.replace('"', '')
graph = json.loads(data)
nodes = {}
for strategy in strategies:
	nodes[strategy] = transform("Results/" + strategy)
games = 50

print sim.run(graph, nodes, games)