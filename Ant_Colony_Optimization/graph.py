class Graph():
    def __init__(self, distanceMatrix, pheromoneMatrix):
        self.distanceMatrix = distanceMatrix
        self.pheromoneMatrix = pheromoneMatrix

    def getDistanceMatrix(self):
        return self.distanceMatrix

    def getPheromoneMatrix(self):
        return self.pheromoneMatrix