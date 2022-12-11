from random import randint, uniform
from math import pow
from matplotlib import pyplot as plt

POP_SIZE = 50
GEN_SIZE = 100
C_SIZE = 14

# holds a potential solution
class Candidate:
    def __init__(self, x, y, fitness):
        self.x = x
        self.y = y
        self.fitness = fitness

# we want to minimize this function
def fitness(x, y):
    return (4 - 2.1 * pow(x, 2) + pow(x, 4) / 3) * pow(x, 2) + \
        x * y + (-4 + 4 * pow(y, 2)) * pow(y, 2)

# return decimal value of chromosome
def decodeChromosome(chromosome):
    out = int(chromosome[1:], 2)
    sign = -1 if int(chromosome[0]) == 1 else 1
    out = out * sign / 1000.0
    return out

# generate a potential chromosome within [-5,5]
def generateChromosome():
    chromosome = ""

    for i in range(C_SIZE):
        temp = str(randint(0, 1))
        chromosome += temp
    
    if abs(decodeChromosome(chromosome)) > 5:
        generateChromosome()

    return chromosome


# select parents by roulette method
def selectParents(candidates, sum_fitness):
    rand_A = uniform(0,1) * sum_fitness
    rand_B = uniform(0,1) * sum_fitness
    partial_A = 0
    partial_B = 0
    p_A = candidates[0]
    p_B = candidates[0]

    for i in range(POP_SIZE):
        if partial_A > rand_A:
            p_A = candidates[i]
            break
        partial_A += -candidates[i].fitness
        

    for i in range(POP_SIZE):
        if partial_B > rand_B:
            p_B = candidates[i]
            break
        partial_B += -candidates[i].fitness

    return p_A, p_B

# perform uniform crossover on parents A and B to return children X and Y
def uCrossover(p_A, p_B):
    child_X = ""
    child_Y = ""

    for i in range(C_SIZE):
        if randint(0, 1):
            child_X += p_B[i]
            child_Y += '0' if p_B[i] == '1' else '1'
        else:
            child_X += p_A[i]
            child_Y += '0' if p_A[i] == '1' else '1'

    return child_X, child_Y

# use pm to apply mutation
def mutate(child):
    x = list(child.x)
    y = list(child.y)
    mut_rate = 1.0/C_SIZE
    for i in range(C_SIZE):
        if uniform(0, 1) < mut_rate:
            x[i] = str(randint(0, 1))
    
    for i in range(C_SIZE):
        if uniform(0, 1) < mut_rate:
            y[i] = str(randint(0, 1))

    child.x = ''.join(x)
    child.y = ''.join(y)
    return child

# simple genetic algorithm with p_crossover = 0.5
def simpleGA(p_crossover = 0.5):
    # variables to keep track of fitness
    best_fitness = 0
    sum_fitness = 0
    avg_fitness = 0
    best_x = 0
    best_y = 0

    # variables for plotting
    all_avg = []
    all_best = []

    candidates = []

    for i in range(POP_SIZE):
        # generate random solution
        x = generateChromosome()
        y = generateChromosome()
        fit = fitness(decodeChromosome(x), decodeChromosome(y))
        if i == 0 or fit < best_fitness:
            best_fitness = fit
            best_x = decodeChromosome(x)
            best_y = decodeChromosome(y)
        sum_fitness += fit
        candidates.append(Candidate(x, y, fit))

    avg_fitness = sum_fitness / POP_SIZE

    for i in range(GEN_SIZE):
        # generate new children
        new_candidates = []

        for i in range(0,POP_SIZE,2):
            p_A, p_B = selectParents(candidates, -sum_fitness)
            child_X, child_Y = p_A, p_B

            if uniform(0,1) < p_crossover:
                child_X.x, child_Y.x = uCrossover(p_A.x, p_B.x)
                child_X.y, child_Y.y = uCrossover(p_A.y, p_B.y)
            
            child_X = mutate(child_X)
            child_Y = mutate(child_Y)

            new_candidates.append(child_X)
            new_candidates.append(child_Y)
        
        candidates = new_candidates

        # calculate new fitness
        sum_fitness = 0
        for i in range(POP_SIZE):
            fit = fitness(decodeChromosome(candidates[i].x), decodeChromosome(candidates[i].y))
            sum_fitness += fit
            if fit < best_fitness:
                best_fitness = fit
                best_x = decodeChromosome(x)
                best_y = decodeChromosome(y)
        
        avg_fitness = sum_fitness / POP_SIZE

        all_avg.append(avg_fitness)
        all_best.append(best_fitness)
 
    return all_avg, all_best, best_x, best_y, best_fitness


if __name__ == "__main__":
    avg, best, x, y, z = simpleGA()
    print("Final x:", x, "Final y:", y, "Final z:", z)
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    fig.tight_layout(pad=2.0)
    ax1.plot([i for i in range(1,GEN_SIZE+1)], avg)
    ax1.set_title("Generation vs Average Fitness")
    ax2.plot([i for i in range(1,GEN_SIZE+1)], best)
    ax2.set_title("Generation vs Best Fitness")

    plt.show()



