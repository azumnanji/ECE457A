import csv
import random as rd
from itertools import combinations

# convert csv data into a 2d list
def inputData(csv_file):
    out = list(csv.reader(open(csv_file)))
    return [list(map(int, row)) for row in out]

# return the cost of a given solution
def cost(solution, distance, flow, sol_len):
    cost = 0
    for i in range(sol_len):
        for j in range(sol_len):
            cost += distance[i][j]*flow[solution[i] - 1][solution[j] - 1]
    return cost

# create random initial solution
def getInitialSolution(sol_len, seed, show=False):
    n_jobs = sol_len
    initial_solution = list(range(1, n_jobs+1))
    rd.seed(seed)
    rd.shuffle(initial_solution)
    if show == True:
        print("initial Random Solution: {}".format(initial_solution))
    return initial_solution

# swap two given departments within a solution
def swapMove(solution, i ,j):
    solution = solution.copy()
    i_index = solution.index(i)
    j_index = solution.index(j)
    solution[i_index], solution[j_index] = solution[j_index], solution[i_index]
    return solution

# return the tabu short term memory structure
def getTabuStructure(sol_len):
    swap_dict = {}
    for swap in combinations(range(1, sol_len+1), 2):
        swap_dict[swap] = {'tabu_time': 0, 'Cost': 0}
    return swap_dict

def tabuSearch(distance, flow, sol_len, tabu_tenure, starting_seed, neighborhood_size=1, frequency=False, aspiration=False):
    # Parameters:
    tabu_structure = getTabuStructure(sol_len)
    best_solution = getInitialSolution(sol_len, starting_seed)
    best_cost = cost(best_solution, distance, flow, sol_len)
    current_solution = best_solution.copy()
    current_cost = best_cost
    frequency_dict = {}

    iter = 1
    Terminate = 0
    while Terminate < 100:
        # Get all possible neighbors
        moves = tabu_structure.keys()
        # reduce neighborhood if necessary
        if neighborhood_size < 1:
            moves = rd.sample(moves, int((len(moves)-1)*neighborhood_size))
            # reset all costs
            for move in tabu_structure:
                tabu_structure[move]['Cost'] = float('inf')

        for move in moves:
            candidate_solution = swapMove(current_solution, move[0], move[1])
            candidate_cost = cost(candidate_solution, distance, flow, sol_len)
            tabu_structure[move]['Cost'] = candidate_cost

        while True:
            # select the move with the lowest cost
            best_move = min(tabu_structure, key =lambda x: tabu_structure[x]['Cost'])
            best_move_cost = tabu_structure[best_move]["Cost"]
            tabu_time = tabu_structure[best_move]["tabu_time"]
            # Not Tabu
            if tabu_time < iter:
                # make the move
                current_solution = swapMove(current_solution, best_move[0], best_move[1])

                if not tuple(current_solution) in frequency_dict:
                    frequency_dict[tuple(current_solution)] = 1
                else:
                    frequency_dict[tuple(current_solution)] += 1
                
                freq_val = (frequency_dict[tuple(current_solution)] - 1) if frequency else 0
                
                current_cost = best_move_cost + freq_val

                # Best Improving move
                if current_cost < best_cost:
                    best_solution = current_solution
                    best_cost = current_cost
                    Terminate = 0
                else:
                    Terminate += 1
                # update tabu_time for the move
                tabu_structure[best_move]['tabu_time'] = iter + tabu_tenure
                iter += 1
                break
            # If tabu
            else:
                # Aspiration
                if aspiration and best_move_cost < best_cost:
                    current_solution = swapMove(current_solution, best_move[0], best_move[1])

                    if not tuple(current_solution) in frequency_dict:
                        frequency_dict[tuple(current_solution)] = 1
                    else:
                        frequency_dict[tuple(current_solution)] += 1
                    
                    freq_val = (frequency_dict[tuple(current_solution)] - 1) if frequency else 0
                    
                    current_cost = best_move_cost + freq_val
                    if current_cost < best_cost:
                        best_solution = current_solution
                        best_cost = current_cost
                        Terminate = 0
                        iter += 1
                        break
                else:
                    tabu_structure[best_move]["Cost"] = float('inf')
                    continue
    return tabu_structure, best_solution, best_cost


if __name__=="__main__":
    distance = inputData("A5-Distance.csv")
    flow = inputData("A5-Flow.csv")
    SOLUTION_LENGTH = 20

    print("###  Q2 - Part 2 ###")
    tenure = 3
    starting_seed = 14
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, neighborhood_size=1, aspiration=False)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))

    print("\n### Q2 - Change Initial Solution ###")
    starting_seed = 5    
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, neighborhood_size=1, aspiration=False)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))
    starting_seed = 20
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, neighborhood_size=1, aspiration=False)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))

    print("\n### Q2 - Change Tabu Tenure ###")
    tenure = 2
    starting_seed = 14
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, neighborhood_size=1, aspiration=False)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))
    tenure = 4
    starting_seed = 14
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, neighborhood_size=1, aspiration=False)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))

    print("\n### Q2 - Add Aspiration ###")
    tenure = 3
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, neighborhood_size=1, aspiration=True)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))

    print("\n### Q2 - Reduce Neighborhood Size to 50% ###")
    tenure = 3
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, neighborhood_size=0.5, aspiration=True)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))

    print("\n### Q2 - Add Frequency ###")
    tenure = 3
    _, sol, sol_cost = tabuSearch(distance, flow, SOLUTION_LENGTH, tenure, starting_seed, frequency=True, neighborhood_size=0.5, aspiration=True)
    print("Cost: " + str(sol_cost), "Sol: " + str(sol))