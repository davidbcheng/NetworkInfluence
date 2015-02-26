from graph_tool.all import *
import heapq

### Computations on Graph ###
import math
def maxDegree(g, n):
    # Find n max degree nodes of graph g
    measure = [(vertex.out_degree(), ind) for ind, vertex in enumerate(g.vertices())]
    return maxMeasure(measure, n)

def maxKatz(g, n):
    # Find n max katz nodes
    vertexMap = graph_tool.centrality.katz(g).get_array()
    measure = [(elem, ind) for ind, elem in enumerate(vertexMap)]
    return maxMeasure(measure, n)

def maxCluster(g, n):
    vertexMap = graph_tool.clustering.local_clustering(g).get_array()
    measure = [(elem, ind) for ind, elem in enumerate(vertexMap)]
    return maxMeasure(measure, n)

def maxMeasure(measure, n):
    # Find max n according to measure where measure is list of (measure, vertexIndex)
    # tupels
    heapq.heapify(measure)
    return [str(x[1]) for x in heapq.nlargest(n, measure)]


### Strategies ###
class Strategies():

    def __init__(self, g, numPlayers, numSeeds, numTrials):
        self.stratFunc = None
        self.g = g
        self.numPlayers = numPlayers
        self.numSeeds = numSeeds
        self.numTrials = numTrials

    def Combined(self):
        pass

    def Surround(self):
        maxDegreeNodes = maxDegree(self.g, self.numSeeds)
        numToSurround = 2
        surroundNum = [5]
        seeds = []
        pass

    def Articulation(self):
        comp, art, hist = label_biconnected_components(self.g)
        print comp.a
        print art.a
        print hist


    def Cluster(self):
        return maxCluster(self.g, self.numSeeds) * self.numTrials

    def Degree(self):
        return maxDegree(self.g, self.numSeeds) * self.numTrials

    def Katz(self):
        maxDegreeNodes = maxDegree(self.g, self.numSeeds)
        katz = list(set(maxKatz(self.g, 20)) - set(maxDegreeNodes))
        numCancel = math.floor(self.numSeeds * 0.5)
        numKatz = self.numSeeds - numCancel
        seeds = maxDegreeNodes[0:numCancel] + katz[0:numKatz]
        seeds = [str(x) for x in seeds]
        return seeds * self.numTrials

