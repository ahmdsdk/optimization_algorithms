import random as rand

class Graph:
    def __init__(self):
        self.distanceMatrix = [[0, 4, 8, 1], [4, 0, 5, 15], [8, 5, 0, 4], [1, 15, 4, 0]]
        self.pheromoneMatrix = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
    
    def getDistanceMatrix(self):
        return self.distanceMatrix
    def getPheromoneMatrix(self):
        return self.pheromoneMatrix

def calculateTotalAllowedPassingProbabilities(node_i, distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta):
    total = 0
    for i in range(len(distanceMatrix)):
        if node_i == i:
            for j in range(len(distanceMatrix[0])):
                if j in nodes_to_go:
                    weight = 0 if distanceMatrix[i][j] == 0 else 1 / distanceMatrix[i][j]
                    total += weight ** beta * pheromoneMatrix[i][j] ** alpha
    return total
                

def calculatePassingProbability(node_i, node_j, distance, distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta):
    pheromone = pheromoneMatrix[node_i][node_j]
    weight = 0 if distance == 0 else 1 / distance
    allowed_passing_probabilities = calculateTotalAllowedPassingProbabilities(node_i, distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta)
    return (pheromone ** alpha) * (weight ** beta) / allowed_passing_probabilities

def calculateNextNode(node_i, distanceMatrix, pheromoneMatrix, total_nodes, alpha, beta):
    commulativeTotal = []
    nodes_to_go = []
    for j in range(len(distanceMatrix[0])):
        if j != node_i and j not in total_nodes:
            if node_i not in total_nodes:
                total_nodes.append(node_i)
            if j not in nodes_to_go:
                nodes_to_go.append(j)
    
    for node_j in nodes_to_go:
        probability = calculatePassingProbability(node_i, node_j, distanceMatrix[node_i][node_j], distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta)
        commulativeTotal.append(probability)
    
    if len(nodes_to_go) == 1:
        next_node = nodes_to_go[0]
        total_nodes.append(next_node)
        return total_nodes
    for r in range(len(commulativeTotal) - 1):
        commulativeTotal[r + 1] += commulativeTotal[r]
        
    rnd = rand.uniform(0, 1)
    next_node = nodes_to_go[0] if rnd <= commulativeTotal[0] else nodes_to_go[1] if rnd <= commulativeTotal[1] else nodes_to_go[2]
    calculateNextNode(next_node, distanceMatrix, pheromoneMatrix, total_nodes, alpha, beta)
    return total_nodes

def updatePheromoneMatrix(pheromoneMatrix, distanceMatrix, total_nodes, ro, Q):
    total_distance = 0
    for i in range(len(total_nodes) - 1):
        total_distance += distanceMatrix[total_nodes[i]][total_nodes[i + 1]]
    for i in range(len(total_nodes) - 1):
        node = total_nodes[i]
        next_node = total_nodes[i + 1]
        pheromoneMatrix[node][next_node] *= (1 - ro)
        pheromoneMatrix[node][next_node] += (Q / total_distance)
        pheromoneMatrix[next_node][node] *= (1 - ro)
        pheromoneMatrix[next_node][node] += (Q / total_distance)

def printShortestPath(pheromoneMatrix):
    path = []
    path.append(0)
    next_node = 0
    for i in range(len(pheromoneMatrix)):
        max_pheromone = 0
        for j in range(len(pheromoneMatrix[0])):
            if pheromoneMatrix[i][j] > max_pheromone and j not in path:
                max_pheromone = pheromoneMatrix[i][j]
                next_node = j
        if next_node not in path:
            path.append(next_node)
    print(f"shortest path: {path}")

def generateTSAColony(population_size = 10, steps = 10, Q = 4, ro = 0.4, alpha = 1, beta = 1):
    graph = Graph()
    distanceMatrix = graph.getDistanceMatrix()
    pheromoneMatrix = graph.getPheromoneMatrix()
    for step in range(steps):
        for ant in range(population_size):
            total_nodes = []
            print(f"ant {ant} at node {0}", end = " ")
            calculateNextNode(0, distanceMatrix, pheromoneMatrix, total_nodes, alpha, beta)
            updatePheromoneMatrix(pheromoneMatrix, distanceMatrix, total_nodes, ro, Q)
            print(f"total_nodes: {total_nodes}")
            print(f"pheromoneMatrix: {pheromoneMatrix}")
    printShortestPath(pheromoneMatrix)

generateTSAColony()