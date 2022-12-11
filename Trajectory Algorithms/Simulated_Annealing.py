import numpy as np
from random import randint, random, uniform

# cost (easom) function
def f(x):
    return -np.cos(x[0])*np.cos(x[1])*np.exp(-(x[0]-np.pi)**2 - (x[1]-np.pi)**2)

# return a random neighbour that is within 5 units of the current solution
def rand_neighbour(x):
    return [uniform(max(x[0] - 2.5, -100), min(x[0] + 2.5, 100)),
            uniform(max(x[1] - 2.5, -100), min(x[1] + 2.5, 100))]

def temp_func(temp, alpha, type):
    if type == 'L':
        return temp - alpha
    if type == 'G':
        return temp*alpha

def simulated_annealing(num_iterations, temp, final_temp, alpha, initial_guess, temp_decrement):

    curr_sol = initial_guess
    curr_cost = f(curr_sol)

    while temp > final_temp:
        for i in range(num_iterations):

            next_sol = rand_neighbour(curr_sol)
            next_cost = f(next_sol)

            delta_cost = next_cost - curr_cost

            if delta_cost < 0:
                probability = 1
            else:
                probability = np.exp(-delta_cost/temp)

            if random() < probability:
                curr_sol = next_sol
                curr_cost = next_cost

        temp = temp_func(temp, alpha, temp_decrement)

    return curr_sol, curr_cost

if __name__ == "__main__":
    num_iterations = 1000
    temp = 100
    final_temp = 0.1
    alpha = 0.05

    # 3b
    print("3b: Randomized Initial Guess with initial temp not too high or low")
    initial_guess = [randint(-100, 100), randint(-100, 100)]

    sol, cost = simulated_annealing(num_iterations, temp, final_temp, alpha, initial_guess, 'L')
    print("Sol:", sol, "Cost:", cost)

    # 3c
    print("\n3c: 10 different initial guesses")
    for i in range(10):
        initial_guess = [randint(-100, 100), randint(-100, 100)]
        sol, cost = simulated_annealing(num_iterations, temp, final_temp, alpha, initial_guess, 'L')
        print("Sol:", sol, "Cost:", cost)

    # 3d
    print("\n3d: 2 lower temperatures and 2 higher temperatures")
    temperatures = [10, 50, 200, 500]
    for new_temp in temperatures:
        sol, cost = simulated_annealing(num_iterations, new_temp, final_temp, alpha, initial_guess, 'L')
        print("Sol:", sol, "Cost:", cost)


    # 3e
    print("\n3e: Geometric temperature reduction")
    alpha = 0.95

    sol, cost = simulated_annealing(num_iterations, temp, final_temp, alpha, initial_guess, 'G')
    print("Sol:", sol, "Cost:", cost)
