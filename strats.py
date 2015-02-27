from graph_tool.all import *
import heapq
import random
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

def minCluster(g, n):
    vertexMap = graph_tool.clustering.local_clustering(g).get_array()
    measure = [(elem, ind) for ind, elem in enumerate(vertexMap)]
    return minMeasure(measure, n)

def maxMeasure(measure, n):
    # Find max n according to measure where measure is list of (measure, vertexIndex)
    # tupels
    heapq.heapify(measure)
    return [str(x[1]) for x in heapq.nlargest(n, measure)]

def minMeasure(measure, n):
    heapq.heapify(measure)
    return [str(x[1]) for x in heapq.nsmallest(n, measure)]

### Strategies ###
class Strategies():

    def __init__(self, g, numPlayers, numSeeds, numTrials):
        self.stratFunc = None
        self.g = g
        self.numPlayers = numPlayers
        self.numSeeds = numSeeds
        self.numTrials = numTrials

    def Combined(self):
        # Run Katz and ArticulationMaxD
        numEach = int(self.numSeeds * self.numTrials / 2)
        return self.ArticulationMaxD()[0:numEach] + self.Katz()[0:numEach]


    def Surround(self):
        # Surround highest degree nodes
        maxDegreeNodes = maxDegree(self.g, self.numSeeds)
        numToSurround = 2
        surroundNum = [5, 5]
        seeds = [] # maxDegreeNodes[0:numToSurround]
        vIndex = self.g.vertex_index
        for i, s in enumerate(surroundNum):
            v = self.g.vertex(s)
            neighbors = v.out_neighbours()
            measure = [(x.out_degree(), vIndex[x]) for x in neighbors
                       if str(vIndex[x]) not in seeds and str(vIndex[x]) not in maxDegreeNodes]
            seeds = seeds + maxMeasure(measure, s)
        return seeds * self.numTrials

    def ArticulationMaxC(self):
        # Find articulation points which are the most number of components
        comp, art, hist = label_biconnected_components(self.g)
        artNodes =  {i:set() for i, x in enumerate(art.a) if x == 1}
        self.g.reindex_edges()
        for i, edge in enumerate(self.g.edges()):
            n1, n2 = edge
            label = comp.a[i]
            if n1 in artNodes:
                artNodes[n1].add(label)
            if (n2 in artNodes):
                artNodes[n2].add(label)

        measure = [(len(lst), ind) for ind, lst in artNodes.items()]
        sortedArtNodes = maxMeasure(measure, len(artNodes))
        maxDegreeNodes = maxDegree(self.g, self.numSeeds)
        addArtNodes = list(set(sortedArtNodes) - set(maxDegreeNodes))
        seeds = maxDegreeNodes[0:5] + addArtNodes[0:5]
        return seeds

    def ArticulationMaxN(self):
        # Find articulation points whose components have the most nodes
        comp, art, hist = label_biconnected_components(self.g)
        artNodes =  {i:0 for i, x in enumerate(art.a) if x == 1}

        # mapping from art node to component it's in
        artMap = {}
        compIndex = 0
        for i, x in enumerate(art.a):
            if x == 1:
                artMap[compIndex] = i
                compIndex += 1
        self.g.reindex_edges()
        for i, edge in enumerate(self.g.edges()):
            label = comp.a[i]
            artNodes[artMap[label]] += 1
        measure = [(numNodes, index) for index, numNodes in artNodes.items()]
        seeds = maxMeasure(measure, len(measure))
        return seeds[0:self.numSeeds] * self.numTrials

    def ArticulationMaxD(self):
        # Find articulation points with max degree
        comp, art, hist = label_biconnected_components(self.g)
        artNodes =  [(self.g.vertex(i).out_degree(), i) for i, x in enumerate(art.a) if x == 1]
        artNodes = maxMeasure(artNodes, len(artNodes))
        seeds = []
        for x in range(self.numTrials):
            seeds = seeds + random.sample(artNodes[0:min(len(artNodes), 20)], self.numSeeds)
        return seeds

    def ClusterDegree(self):
        # Choose nodes out of top 300 degree not in top numSeeds by degree and then
        # sort by clustering
        maxDegreeNodes = maxDegree(self.g, 300)
        vertexMap = graph_tool.clustering.local_clustering(self.g).get_array()
        measure = [(elem, ind) for ind, elem in enumerate(vertexMap)
                   if str(ind) in maxDegreeNodes[self.numSeeds+1:]]
        seeds = maxMeasure(measure, len(measure))
        reversed(seeds)
        seeds = seeds[0:30]
        seedSet = []
        for x in range(self.numTrials):
            seedSet = seedSet + random.sample(seeds, self.numSeeds)
        return seedSet

    def Cluster(self):
        # Choose random nodes out of list of 50 nodes with lowest clustering
        seeds = minCluster(self.g, self.numSeeds)
        seedSet = []
        for x in range(self.numTrials):
            seedSet = seedSet + random.sample(seeds, self.numSeeds)
        return seedSet

    def Degree(self):
        # Choose random nodes out of list of top 2*numSeeds with highest degree
        seeds = []
        maxDegreeNodes = maxDegree(self.g, self.numSeeds*2)
        for x in range(self.numTrials):
            seeds = seeds + random.sample(maxDegreeNodes, self.numSeeds)
        return seeds

    def NextDegree(self):
        # Choose next highest degree after num seeds
        return maxDegree(self.g, self.numSeeds*2)[self.numSeeds:self.numSeeds*2] * self.numTrials

    def Betweeness(self):
        # Choose nodes with max betweeness
        vertexMap, edgeMap = graph_tool.centrality.betweenness(self.g)
        measure = [(elem, ind) for ind, elem in enumerate(vertexMap.get_array())]
        return maxMeasure(measure, self.numSeeds) * self.numTrials

    def Eigenvector(self):
        # Choose nodes with max eigenvector centrality
        maxDegreeNodes = maxDegree(self.g, self.numSeeds)
        maxE, vertexMap = graph_tool.centrality.eigenvector(self.g)
        measure = [(elem, ind) for ind, elem in enumerate(vertexMap.get_array())
                   if str(ind) not in maxDegreeNodes]
        return maxMeasure(measure, self.numSeeds) * self.numTrials

    def PageRank(self):
        # Choose nodes with highest page rank
        maxDegreeNodes = maxDegree(self.g, self.numSeeds)
        vertexMap= graph_tool.centrality.pagerank(self.g)
        measure = [(elem, ind) for ind, elem in enumerate(vertexMap.get_array())
                    if str(ind) not in maxDegreeNodes]
        return maxMeasure(measure, self.numSeeds) * self.numTrials

    def Katz(self):
        # Choose random nodes outside of top degree with highest katz
        maxDegreeNodes = maxDegree(self.g, self.numSeeds)
        katz = list(set(maxKatz(self.g, 100)) - set(maxDegreeNodes))
        seeds = random.sample(katz, self.numSeeds)
        seeds = [str(x) for x in seeds]
        return seeds * self.numTrials

