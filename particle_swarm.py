import random as rand

def func(x):
    return x**2 + 5*x - 6

def fitness(x):
    ans = func(x)
    
    if ans == 0:
        return 9999
    else:
        return abs(1/ans)

def generateSolutions(population_size = 1000, steps = 10000, max_x = 10000, max_y = 10000, max_z = 10000):
    solutions = []
    for s in range(population_size):
        x = rand.uniform(-max_x, max_x)
        solutions.append((x, 0, x))
    
    for i in range(steps):
        ranked_solutions = []
        for s in solutions:
            ranked_solutions.append((fitness(s[0]), s))
        ranked_solutions.sort()
        ranked_solutions.reverse()
        
        print(f"Swarm gbest at {i}:")
        print(ranked_solutions[0])
        gbest = ranked_solutions[0][1][0]
        
        if ranked_solutions[0][0] >= 999:
            return ranked_solutions[:1]
        
        newSolutions = []
        for s in ranked_solutions:
            rnd1 = rand.uniform(0, 1)
            rnd2 = rand.uniform(0, 1)
            # vi+1 = vi + c1 * rnd1 * (pbest - xi) + c2 * rnd2 * (gbest - xi)
            v = s[1][1] + 1.47 * rnd1 * (s[1][2] - s[1][0]) + 1.47 * rnd2 * (gbest - s[1][0])
            x = s[1][0] + v
            # pbest = min(s[1][0], x)
            pbest = s[1][0] if max(fitness(s[1][0]), fitness(x)) == fitness(s[1][0]) else x
            newSolutions.append((x, v, pbest))
        
        solutions = newSolutions
        
    return solutions[:1]

ans = generateSolutions()

print(f"Best Solution: x = {ans[0][1][0]}, f(x) = {func(ans[0][1][0])} with fitness == {fitness(ans[0][1][0])}")