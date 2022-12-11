import matplotlib.pyplot as plt
import numpy as np
from pandas import read_excel

class ACO:
    def __init__(self, data_file, num_ants, iterations, evap_rate, alpha, beta, q):
        self.num_ants = num_ants
        self.iterations = iterations
        self.evap_rate = evap_rate
        self.a = alpha
        self.b = beta
        self.q = q
        self.distances = self.get_distances(data_file)
        # initialize all pheromones with 1
        self.pheromones = np.ones(self.distances.shape)
        self.ants = None

    def get_distances(self, data_file):
        df = read_excel(data_file)
        df = np.asarray(df)
        df = np.delete(df, 0, 1).astype(float)
        distances = np.zeros((29, 29))
        for i in range(29):
            for j in range(i+1, 29):
                # take inverse of distance for easier calculations
                distances[i][j] = 1 / ((df[i][0] - df[j][0])**2 + (df[i][1]-df[j][1])**2)**0.5

        # symmetrize the distance matrix
        return distances + distances.T - np.diag(distances.diagonal())
    
    def get_cost(self, path):
        distance = 0
        for i in range(len(path)-1):
            distance += 1 / self.distances[path[i]][path[i+1]]
        return distance
    
    def evaporate_pheromones(self, path):
        for i in range(len(path)-1):
            self.pheromones[path[i]][path[i+1]] *= (1-self.evap_rate)
            self.pheromones[path[i+1]][path[i]] *= (1-self.evap_rate)

    def update_pheromones(self, path, cost):
        for i in range(len(path)-1):
            self.pheromones[path[i]][path[i+1]] += self.q/cost
            self.pheromones[path[i+1]][path[i]] += self.q/cost
                

    def run(self):
        best_cost = None
        best_path = []

        avg_fitness = []
        best_fitness = []
        for i in range(self.iterations):
            # reset solutions
            self.ants = np.random.randint(self.distances.shape[0], size=self.num_ants)
            sum_fitness = 0
            for j in range(self.num_ants):
                start_node = self.ants[j]
                visited = [start_node]
                # calculate probabilities
                m = np.multiply(np.power(self.distances[start_node, :], self.a), np.power(self.pheromones[start_node, :], self.b))
                probabilites = m / np.sum(m)
                # choose cities to visit based on probabilities
                while len(visited) < 29:
                    next_node = np.argmax(probabilites)
                    visited.append(next_node)
                    probabilites[next_node] = 0.0
                
                # pheromone evaporation
                self.evaporate_pheromones(visited)
                cost = self.get_cost(visited)
                sum_fitness += cost
                if best_cost is None or cost < best_cost:
                    best_cost = cost
                    best_path = visited
                
                # update pheromone with path ant took
                self.update_pheromones(visited, cost)
            
            # update pheromone with best solution so far
            self.update_pheromones(best_path, best_cost)
            avg_fitness.append(sum_fitness/self.num_ants)
            best_fitness.append(best_cost)
                    
        print("Cost: ", best_cost)
        print("Path: ", best_path)
        return avg_fitness, best_fitness




if __name__ == "__main__":
    iterations = 500
    aco = ACO("Assignment7-city coordinates.xlsx", 100, iterations, 0.4, 1, 2, 1000)
    avg_fit, best_fit = aco.run()
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    fig.tight_layout(pad=2.0)
    ax1.plot([i for i in range(1,iterations+1)], avg_fit)
    ax1.set_title("Generation vs Average Fitness")
    ax2.plot([i for i in range(1,iterations+1)], best_fit)
    ax2.set_title("Generation vs Best Fitness")

    plt.show()