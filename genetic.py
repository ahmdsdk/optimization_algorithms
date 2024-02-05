import random as rand

def func(x, y, z):
    return 6*x**3 + 9*y**2 + 90*z - 25

def fitness(x, y, z):
    ans = func(x, y, z)
    
    if ans == 0:
        return 9999
    else:
        return abs(1/ans)

def generateSolutions(population_size = 1000, steps = 10000, max_x = 10000, max_y = 10000, max_z = 10000):
    solutions = []
    for s in range(population_size):
        x = rand.uniform(-max_x, max_x)
        y = rand.uniform(-max_y, max_y)
        z = rand.uniform(-max_z, max_z)
        solutions.append((x, y, z))
    
    for i in range(steps):
        ranked_solutions = []
        for s in solutions:
            ranked_solutions.append((fitness(s[0], s[1], s[2]), s))
        ranked_solutions.sort()
        ranked_solutions.reverse()
        
        print(f"Generation {i} best solution:")
        print(ranked_solutions[0])
        
        if ranked_solutions[0][0] >= 9999:
            return ranked_solutions[0][1][0], ranked_solutions[0][1][1], ranked_solutions[0][1][2]
        
        best_solutions = ranked_solutions[:100]
        elements = []
        
        for s in best_solutions:
            elements.append(s[1][0])
            elements.append(s[1][1])
            elements.append(s[1][2])
        
        newGeneration = []
        for _ in range(population_size):
            e1 = rand.choice(elements) * rand.uniform(0.99, 1.01)
            e2 = rand.choice(elements) * rand.uniform(0.99, 1.01)
            e3 = rand.choice(elements) * rand.uniform(0.99, 1.01)
            
            newGeneration.append((e1, e2, e3))
        
        solutions = newGeneration
            
        
    return solutions[0][0], solutions[0][1], solutions[0][2]

x, y, z = generateSolutions()

print(f"Best Solutions is {x, y, z} == {func(x, y, z) + 25} with fitness == {fitness(x, y, z)}")