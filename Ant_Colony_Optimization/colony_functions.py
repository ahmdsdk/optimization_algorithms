import random as rand

def calculateTotalAllowedPassingProbabilities(node_i, distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta, Q):
    total = 0
    for i in range(len(distanceMatrix)):
        if node_i == i:
            for j in range(len(distanceMatrix[0])):
                if j in nodes_to_go:
                    weight = 0 if distanceMatrix[i][j] == 0 else 1 / distanceMatrix[i][j]
                    total += weight ** beta * pheromoneMatrix[i][j] ** alpha
    return total
                

def calculatePassingProbability(node_i, node_j, distance, distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta, Q):
    pheromone = pheromoneMatrix[node_i][node_j]
    weight = 0 if distance == 0 else 1 / distance
    allowed_passing_probabilities = calculateTotalAllowedPassingProbabilities(node_i, distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta, Q)
    return (pheromone ** alpha) * (weight ** beta) / allowed_passing_probabilities

def calculateNextNode(node_i, distanceMatrix, pheromoneMatrix, total_nodes, alpha, beta, ro, Q):
    commulativeTotal = []
    nodes_to_go = []
    for j in range(len(distanceMatrix[0])):
        if j != node_i and j not in total_nodes:
            if node_i not in total_nodes:
                total_nodes.append(node_i)
            if j not in nodes_to_go:
                nodes_to_go.append(j)
    
    for node_j in nodes_to_go:
        probability = calculatePassingProbability(node_i, node_j, distanceMatrix[node_i][node_j], distanceMatrix, pheromoneMatrix, nodes_to_go, alpha, beta, Q)
        commulativeTotal.append(probability)

    if len(nodes_to_go) == 1:
        next_node = nodes_to_go[0]
        total_nodes.append(next_node)
        return total_nodes

    for r in range(len(commulativeTotal) - 1):
        commulativeTotal[r + 1] += commulativeTotal[r]
    
    rnd = rand.uniform(0, 1)
    for r in range(len(commulativeTotal)):
        if rnd <= commulativeTotal[r]:
            next_node = nodes_to_go[r]
            break
    calculateNextNode(next_node, distanceMatrix, pheromoneMatrix, total_nodes, alpha, beta, ro, Q)
    return total_nodes

def updatePheromoneMatrix(pheromoneMatrix, distanceMatrix, ants, ro, Q):
    total_distances = []
    ants_to_update = []
    for i, ant in enumerate(ants):
        if ant.did_finish and not ant.did_update_pheromone:
            total_distance = 0
            for d in range(len(ant.path) - 1):
                total_distance += distanceMatrix[ant.path[d]][ant.path[d + 1]]
            ant.did_update_pheromone = True
            total_distances.append(round(total_distance, 1))
            ants_to_update.append(ant)
    
    if len(ants_to_update) > 0:
        for i in range(len(pheromoneMatrix)):
            for j in range(len(pheromoneMatrix[0])):
                pheromoneMatrix[i][j] *= (1 - ro)
                pheromoneMatrix[j][i] *= (1 - ro)

        for a, ant in enumerate(ants_to_update):
            total_nodes = ant.path
            for i in range(len(total_nodes) - 1):
                node = total_nodes[i]
                next_node = total_nodes[i + 1]
                pheromoneMatrix[node][next_node] += (Q / total_distances[a])
                pheromoneMatrix[next_node][node] += (Q / total_distances[a])
        
def getShortestPath(pheromoneMatrix, i, path):
    if i not in path:
        path.append(i)
    next_node = 0
    max_pheromone = -100
    for j in range(len(pheromoneMatrix[0])):
        if pheromoneMatrix[i][j] > max_pheromone and j not in path:
            max_pheromone = pheromoneMatrix[i][j]
            next_node = j
    if next_node not in path:
        path.append(next_node)
        getShortestPath(pheromoneMatrix, next_node, path)
    return path

def generateTSAColony(distanceMatrix, pheromoneMatrix, Q = 4, ro = 0.8, alpha = 1, beta = 1):
    total_nodes = []
    calculateNextNode(0, distanceMatrix, pheromoneMatrix, total_nodes, alpha, beta, ro, Q)
    return total_nodes