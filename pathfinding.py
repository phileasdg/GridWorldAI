import itertools
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

side_length = 10
decimals = 1
n_goals = 5
goals = []

environment = np.around(np.random.uniform(-0.9, 0.9, (side_length, side_length)), decimals=decimals)  # decimal grid
agent_environment = np.zeros((side_length, side_length))
agent_start = []
all_neighbours = []

def assign_goals(n_goals):
    for i in range(n_goals):
        x = np.random.randint(0, side_length)
        y = np.random.randint(0, side_length)
        environment[y, x] = 1
        goals.append((y, x))

def assign_agent_start(starty, startx):
    global agent_start
    agent_start = [starty, startx]
    environment[starty, startx] = 0

def print_agent_utility_map(data, title="Utility Map"):
    plt.imshow(data, cmap='RdYlGn', interpolation='nearest')
    plt.title((title))
    plt.colorbar()

    # print frame around current AI position
    ax = plt.subplot()
    ax.add_patch(Rectangle((agent_start[1]-0.5, agent_start[0]-0.5), 1, 1, fill=False, edgecolor='k', lw=4))

    # print labels on cells if env_side_length < 15
    if side_length <= 15:
        for i in range(side_length):
            for j in range(side_length):
                plt.text(j, i, data[i, j], ha="center", va="center", color="k")

    plt.show()

assign_goals(n_goals)
assign_agent_start(5, 3)

#TODO: transfer this back into the main code.
def list_neighbours(posyx, repeat=0):
    global all_neighbours
    neighboursy = []
    neighboursx = []

    for i in range(repeat+2):
        if i == 0:
            neighboursy.append(posyx[0])
            neighboursx.append(posyx[1])
        else:
            neighboursy.append(posyx[0] + i)
            neighboursy.append(posyx[0] - i)
            neighboursx.append(posyx[1] + i)
            neighboursx.append(posyx[1] - i)
    print(neighboursy, neighboursx)

    for i in neighboursy:
        for j in range(len(neighboursx)):
            all_neighbours.append((i, neighboursx[j]))

def update_agent_environment(env, source):  # parameters are the source environment, and the receiver environment
    for i in all_neighbours:
        env[i] = source[i]

# the pathfinding function will be the same for each agent, but the utility function will be different
def find_path():
    pass
    #according to what the AI knows, what is the best path to the goals which avoid the penalties.

list_neighbours(agent_start, 1)
update_agent_environment(agent_environment, environment)
print(all_neighbours)
print_agent_utility_map(environment)
print_agent_utility_map(agent_environment)

# find best and cheapest or most profitable way go towards goal in as few steps as possible
# find the best way to goal
# find the cheapest way to goal
# find the most profitable way to goal
# find a balance between these approaches
# add listed values to array
# as it moves around, the agent discovers the array values and makes decisions accordingly.
