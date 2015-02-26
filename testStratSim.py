# Usage:  python testStratSim.py strat1 strat2 FreeStyle.json
# Example: python testSim.py 2.10.22 HighestDegree LocalClustering

import sim
import json
import sys
from strats import Strategies
import graph_tool.all as gt
numTrials = 2

def transformSeeds(graphName, seeds):
    # Convert file containing seed nodes to dictionary format for simulation
    numSeeds = int(graphName.split('.')[1])
    results = [seeds[i:i+numSeeds] for i in xrange(0, len(seeds), numSeeds)]
    return results

def loadGraph(graphName, graphJson):
    args = graphName.split('.')
    numPlayers = int(args[0])
    numSeeds = int(args[1])

    g = gt.Graph()
    g.add_vertex(len(graphJson))
    for i in xrange(len(graphJson)):
        node = str(i)
        for neighbor in graphJson[node]:
            g.add_edge(g.vertex(int(node)), g.vertex(int(neighbor)))

    return g

def saveSeeds(seeds):
    with open('seedsResult', 'w') as f:
        for seedSet in seeds:
            for node in seedSet:
                f.write("%s\n" %node)

# Called if command contains Freestyle.json arg in which case load
# previos game
def loadPrevGame(graphName, jsonFlag, nodes):
    seedsPath = 'results/' + graphName + '-' + jsonFlag
    with open (seedsPath, "r") as f:
        seeds = json.loads(f.read().strip('\n'))
    for team, seedSet in seeds.items():
        if team == "Freestyle":
            continue
        nodes[team] = seedSet

def runGame(graph, stratNames, numPlayers, numSeeds):
    nodes = {}
    Strat = Strategies(graph, numPlayers, numSeeds, numTrials)
    for strategy in stratNames:
        if strategy.endswith('.json'):
            loadPrevGame(graphName, strategy, nodes)
            continue
        Strat.stratFunc = getattr(Strat, strategy)
        seeds = Strat.stratFunc()

        # Relabel strategy if already being used
        if strategy in nodes:
            strategy = strategy + "1"
        nodes[strategy] = transformSeeds(graphName, seeds)

    #nodes['TA_MORE'] = [["6", "40", "24", "11", "93", "211", "59", "58", "213", "159", "5", "1"], ["8", "58", "105", "59", "1", "40", "2", "93", "24", "5", "42", "80"], ["2", "6", "213", "59", "40", "8", "245", "93", "58", "1", "159", "5"], ["213", "40", "80", "11", "245", "59", "5", "201", "93", "2", "8", "6"], ["58", "1", "6", "159", "40", "93", "245", "213", "59", "11", "8", "5"], ["202", "213", "93", "5", "8", "59", "6", "58", "2", "159", "11", "42"], ["24", "213", "93", "40", "5", "1", "58", "80", "6", "2", "8", "11"], ["1", "2", "80", "58", "11", "211", "105", "93", "5", "8", "59", "42"], ["58", "211", "213", "193", "286", "11", "93", "6", "80", "2", "8", "1"], ["5", "1", "58", "105", "80", "6", "201", "11", "93", "213", "59", "40"], ["1", "105", "59", "6", "11", "93", "80", "201", "202", "8", "2", "58"], ["1", "245", "40", "2", "213", "59", "8", "6", "105", "93", "11", "80"], ["58", "24", "11", "2", "59", "40", "93", "5", "80", "213", "8", "201"], ["6", "8", "58", "11", "80", "40", "213", "5", "286", "93", "105", "2"], ["5", "2", "93", "40", "80", "8", "201", "193", "1", "59", "11", "211"], ["1", "40", "105", "193", "5", "93", "24", "2", "11", "8", "202", "42"], ["8", "201", "11", "58", "213", "1", "6", "80", "40", "59", "93", "5"], ["80", "8", "245", "5", "58", "59", "159", "2", "1", "40", "6", "93"], ["6", "93", "80", "213", "11", "58", "1", "42", "2", "245", "59", "5"], ["11", "5", "42", "245", "211", "8", "6", "2", "58", "59", "1", "40"], ["59", "24", "213", "245", "1", "193", "8", "6", "5", "11", "40", "80"], ["11", "40", "1", "24", "93", "80", "8", "2", "211", "213", "59", "6"], ["213", "159", "11", "24", "8", "93", "58", "80", "40", "6", "201", "5"], ["8", "213", "211", "6", "1", "24", "80", "40", "5", "93", "59", "2"], ["80", "58", "213", "11", "2", "42", "40", "59", "5", "6", "1", "201"], ["80", "42", "93", "40", "6", "59", "5", "213", "11", "193", "1", "8"], ["24", "5", "105", "59", "11", "1", "80", "58", "2", "6", "8", "40"], ["8", "40", "211", "213", "1", "11", "5", "59", "2", "6", "58", "193"], ["193", "40", "93", "6", "58", "2", "245", "59", "5", "24", "1", "80"], ["1", "11", "2", "40", "58", "6", "42", "159", "24", "8", "80", "93"], ["42", "40", "1", "2", "8", "59", "5", "6", "80", "58", "211", "202"], ["58", "201", "80", "1", "11", "213", "202", "59", "8", "6", "24", "2"], ["93", "8", "5", "80", "2", "213", "59", "58", "1", "6", "11", "40"], ["245", "213", "11", "5", "42", "58", "286", "202", "1", "40", "6", "8"], ["42", "40", "11", "213", "1", "6", "8", "24", "5", "59", "2", "93"], ["11", "80", "159", "2", "40", "59", "8", "58", "93", "201", "1", "211"], ["11", "286", "5", "6", "2", "93", "80", "1", "8", "213", "202", "201"], ["2", "201", "42", "80", "1", "5", "40", "245", "58", "6", "59", "93"], ["58", "6", "8", "59", "24", "1", "202", "93", "5", "40", "2", "11"], ["80", "105", "11", "40", "213", "1", "93", "42", "2", "8", "5", "58"], ["1", "5", "58", "159", "213", "6", "40", "201", "93", "8", "2", "59"], ["5", "8", "6", "80", "245", "2", "40", "93", "11", "105", "58", "213"], ["80", "5", "8", "58", "6", "213", "40", "93", "59", "105", "286", "2"], ["201", "5", "193", "24", "1", "80", "213", "11", "58", "6", "8", "40"], ["59", "58", "6", "11", "40", "2", "8", "93", "245", "5", "213", "202"], ["6", "1", "42", "2", "213", "202", "59", "201", "80", "11", "93", "245"], ["93", "1", "40", "80", "8", "2", "213", "201", "5", "11", "59", "6"], ["202", "5", "8", "40", "80", "1", "11", "213", "59", "93", "2", "6"], ["6", "93", "213", "2", "105", "59", "11", "8", "40", "193", "80", "1"]]

    #saveSeeds(nodes['Katz'])
    results = sim.run(graphJson, nodes, numTrials)
    for game in results:
        print game[0]
        # for team in game[1].items():
        #     print team

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
    graph = loadGraph(graphName, graphJson)

    runGame(graph, stratNames, numPlayers, numSeeds)
