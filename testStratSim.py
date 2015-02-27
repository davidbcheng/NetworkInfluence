# Usage:  python testStratSim.py graphName strat1 strat2
# Example: python testStratSim.py 2.10.22 HighestDegree LocalClustering
# Use arg Freestyle.json to load a previous game in

import sim
import json
import sys
from strats import Strategies
import graph_tool.all as gt
numTrials = 50
indexMap = {}

def transformSeeds(graphName, seeds):
    # Convert file containing seed nodes to dictionary format for simulation
    numSeeds = int(graphName.split('.')[1])
    results = [seeds[i:i+numSeeds] for i in xrange(0, len(seeds), numSeeds)]
    return results

def loadGraph(graphName, graphJson):
    g = gt.Graph()
    g.add_vertex(len(graphJson))

    degree = []
    for i in graphJson.keys():
        node = str(int(i))
        degree.append(len(graphJson[node]))
        for neighbor in graphJson[node]:
            g.add_edge(g.vertex(int(node)), g.vertex(int(neighbor)))
    return g

def loadGraphUnindex(graphName, graphJson):
    g = gt.Graph()
    g.add_vertex(len(graphJson))

    rIndexMap = {}
    for index, node in enumerate(graphJson):
        node = int(node)
        indexMap[index] = node
        rIndexMap[node] = index
    for index, node in enumerate(graphJson):
        for neighbor in graphJson[node]:
            g.add_edge(g.vertex(index), g.vertex(rIndexMap[int(neighbor)]))
    return g

def indexSeeds(seeds):
    return [str(indexMap[int(x)]) for x in seeds]

def saveSeeds(seeds, outputFile):
    with open("seeds/" + outputFile, 'w') as f:
        for seedSet in seeds:
            for node in seedSet:
                f.write("%s\n" %node)

# Called if command contains Freestyle.json arg in which case load
# previous game
def loadPrevGame(graphName, jsonFlag, nodes):
    seedsPath = 'results/' + graphName + '-' + jsonFlag
    with open (seedsPath, "r") as f:
        seeds = json.loads(f.read().strip('\n'))
    for team, seedSet in seeds.items():
        if team == "Freestyle":
            continue
        nodes[team] = seedSet

def printScore(results, nodes):
    pointTable = [20, 15, 12, 9, 6, 4, 2, 1] + [0] * 20
    scores = {strategy:0 for strategy in nodes.keys()}
    for game in results:
        gameRank = sorted([(score, strat) for strat,score in game[0].items()], reverse=True)
        for index, value in enumerate(gameRank):
            scores[value[1]] += pointTable[index]
    print sorted([(score/float(numTrials), strat) for strat,score in scores.items()], reverse=True)

def runGame(graph, stratNames, numPlayers, numSeeds):
    nodes = {}
    Strat = Strategies(graph, numPlayers, numSeeds, numTrials)

    for strategy in stratNames:
        print "Running %s" %strategy
        if strategy.endswith('.json'):
            loadPrevGame(graphName, strategy, nodes)
            continue
        Strat.stratFunc = getattr(Strat, strategy)
        seeds = Strat.stratFunc()
        seeds = indexSeeds(seeds)
        # Relabel strategy if already being used
        if strategy in nodes:
            strategy = strategy + "1"
        nodes[strategy] = transformSeeds(graphName, seeds)
        saveSeeds(nodes[strategy], strategy)
        #if strategy == 'PageRank':


    print "Running simulation"
    results = sim.run(graphJson, nodes, numTrials)

    printScore(results, nodes)


if __name__ == '__main__':
    graphName = sys.argv[1]
    graphPath = "graphs/" + graphName + '.json'
    stratNames = sys.argv[2:]

    numPlayers = int(graphName.split('.')[0])
    numSeeds = int(graphName.split('.')[1])
    # Load graph from json file
    with open (graphPath, "r") as f:
        graphJson = json.loads(f.read().strip('\n'))

    # Load graph into graph tool
    graph = loadGraphUnindex(graphName, graphJson)

    runGame(graph, stratNames, numPlayers, numSeeds)
