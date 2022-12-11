from math import pow
import numpy as np
from random import uniform
import matplotlib.pyplot as plt

from copy import deepcopy

V_MAX = 0.2


class Particle:
    def __init__(self):
        # init vel to random between max and min
        self.vel = np.random.uniform(-V_MAX,V_MAX,2)
        # init randomly
        self.pos = np.random.randint(-5, 6, size=2)
        self.pbest = (self.pos, self.get_cost())
        self.nbest = None
    
    def get_cost(self):
        x = self.pos[0]
        y = self.pos[1]
        return (4 - 2.1 * pow(x, 2) + pow(x, 4) / 3) * pow(x, 2) + x * y + (-4 + 4 * pow(y, 2)) * pow(y, 2)
    
    def updateV(self, params):
        r1 = uniform(0,1)
        r2 = uniform(0,1)
        self.vel = params['w'] * self.vel + params['c1']*r1*(self.pbest[0] - self.pos) + \
            params['c2']*r2*(self.nbest[0] - self.pos)
        
        # clip velocity between [-V_MAX, V_MAX]
        self.vel[self.vel > V_MAX] = V_MAX
        self.vel[self.vel < -V_MAX] = -V_MAX 
            
    
    def updatePos(self):
        self.pos = self.pos + self.vel
    
    def updateBest(self):
        cost = self.get_cost()
        self.pbest = (self.pos, cost) if cost < self.pbest[1] else self.pbest
    


class PSO:
    def __init__(self, swarm_size, weight, c1, c2, iterations):
        self.swarm = [Particle() for i in range(swarm_size)]
        self.params = {'w':weight, 'c1':c1, 'c2':c2}
        self.iterations = iterations
    

    def run(self):
        best_fitness = []
        sum_fitness = 0
        avg_fitness = []
        best_p = min(self.swarm, key = lambda p:p.pbest[1]).pbest

        for i in range(self.iterations):
            sum_fitness = 0
            for particle in self.swarm:
                # update nbest for each particle
                particle.nbest = best_p
                
                particle.updateV(self.params)
                particle.updatePos()
                particle.updateBest()

                # update best particle
                if particle.pbest[1] < best_p[1]:
                    best_p = particle.pbest
                
                sum_fitness += particle.pbest[1]
            
            avg_fitness.append(sum_fitness/len(self.swarm))
            best_fitness.append(best_p[1])

        
        return avg_fitness, best_fitness, best_p




if __name__=="__main__":
    itr = 1000
    pso = PSO(swarm_size=30, weight=0.792, c1=1.495, c2=1.495, iterations=itr)
    avg, best, p = pso.run()
    print("Final x:", p[0][0], "Final y:", p[0][1], "Final z:", p[1])
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    fig.tight_layout(pad=2.0)
    ax1.plot([i for i in range(1,itr+1)], avg)
    ax1.set_title("Iteration vs Average Fitness")
    ax2.plot([i for i in range(1,itr+1)], best)
    ax2.set_title("Iteration vs Best Fitness")

    plt.show()
