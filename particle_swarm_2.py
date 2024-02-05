import random as rand

def func(x, y, z):
    return 6*x**3 + 9*y**2 + 90*z - 25

def fitness(x, y, z):
    ans = func(x, y, z)
    
    if ans == 0:
        return 9999
    else:
        return abs(1/ans)

# class Solution:
#     def __init__(self):
#         self.fitness = []
#         self.positions = []
#         self.velocities = []
#         self.pbest = []

#     def appendData(self, fitness, positions, velocities, pbest):
#         self.fitness.append(fitness)
#         self.positions.append(positions)
#         self.velocities.append(velocities)
#         self.pbest.append(pbest)

#     def getData(self):
#         return self.fitness, self.x, self.y, self.z

def generateSolutions(population_size = 1000, steps = 10000, max_x = 10000, max_y = 10000, max_z = 10000):
    solutions = []
    for s in range(population_size):
        x = rand.uniform(-max_x, max_x)
        y = rand.uniform(-max_y, max_y)
        z = rand.uniform(-max_x, max_z)
        solutions.append(((x, y, z), (0, 0, 0), (x, y, z)))
    
    for i in range(steps):
        ranked_solutions = []
        for s in solutions:
            ranked_solutions.append((fitness(s[0][0], s[0][1], s[0][2]), s))
        ranked_solutions.sort()
        ranked_solutions.reverse()
        
        print(f"Swarm gbest at {i}:")
        print(ranked_solutions[0][1][0])
        gbest_x = ranked_solutions[0][1][0][0]
        gbest_y = ranked_solutions[0][1][0][1]
        gbest_z = ranked_solutions[0][1][0][2]
        
        if ranked_solutions[0][0] >= 999:
            return ranked_solutions[0][1][0][0], ranked_solutions[0][1][0][1], ranked_solutions[0][1][0][2]
        
        newSolutions = []
        for s in ranked_solutions:
            rnd1 = rand.uniform(0, 1)
            rnd2 = rand.uniform(0, 1)
            # vi+1 = vi + c1 * rnd1 * (pbest - xi) + c2 * rnd2 * (gbest - xi)
            v_x = s[1][1][0] + 1.47 * rnd1 * (s[1][2][0] - s[1][0][0]) + 1.47 * rnd2 * (gbest_x - s[1][0][0])
            x = s[1][0][0] + v_x
            # pbest_x = min(s[1][0][0], x)
            
            v_y = s[1][1][1] + 1.47 * rnd1 * (s[1][2][1] - s[1][0][1]) + 1.47 * rnd2 * (gbest_y - s[1][0][1])
            y = s[1][0][1] + v_y
            # pbest_y = min(s[1][0][1], y)
            
            v_z = s[1][1][2] + 1.47 * rnd1 * (s[1][2][2] - s[1][0][2]) + 1.47 * rnd2 * (gbest_z - s[1][0][2])
            z = s[1][0][2] + v_z
            # pbest_z = min(s[1][0][2], z)
            
            pbest_x, pbest_y, pbest_z = [s[1][0][0], s[1][0][1], s[1][0][2]] if max(fitness(s[1][0][0], s[1][0][1], s[1][0][2]), fitness(x, y, z)) == fitness(s[1][0][0], s[1][0][1], s[1][0][2]) else [x, y, z]
            
            newSolutions.append(((x, y, z), (v_x, v_y, v_z), (pbest_x, pbest_y, pbest_z)))
        
        solutions = newSolutions
        
    return 0, 0, 0

x, y, z = generateSolutions()

print(f"Best Solutions is {x, y, z} == {func(x, y, z)} with fitness == {fitness(x, y, z)}")
