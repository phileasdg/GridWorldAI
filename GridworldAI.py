import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# the Agent has an environment to navigate, with goal(s) in the environment,
# everywhere it goes, it changes the environment, and this can either be a neutral action (the
# environment is not disturbed by the action of the AI, a positive action (the AI achieves a goal
# and the environment is not disturbed), or negative (the environment is disturbed, or the move
# shifts tha AI away from its goal, or makes makes it harder for the AI to achieve its goal).

# The agent is tasked with finding the most optimal ways of navigating this environment.

# The environment cells can have values between -1 and 1, where 0 is neutral, -1 is negative, and 1 is positive)

class Environment:

    def __init__(self, side_length, decimals=1, empty=None):
        self.side_length = side_length
        self.decimals = decimals
        if empty is True:
            self.grid = np.zeros((side_length, side_length))  # empty grid
        else:
            # Environment grid: array of height == width == side_length; random values b/w -1 and 1, decimals = decimals.
            self.grid_environment = np.around(np.random.uniform(-0.5, 0.5, (side_length, side_length)),
                                              decimals=decimals)  # decimal grid
            # self.grid = np.random.randint(-1, 1, (side_length, side_length))  # alternative integer grid
        self.goals = []
        self.penalties = []
        self.agent_start = ()

    def assign_grid_position_value(self, posyx: tuple, value: int):
        self.grid[posyx] = value

    def assign_goals(self, n_goals):
        for i in range(n_goals):
            x = np.random.randint(0, self.side_length)
            y = np.random.randint(0, self.side_length)
            self.grid_environment[y, x] = 1
            self.goals.append((y, x))

    def assign_penalties(self, n_penalties):
        # NOTE: Make sure the number of penalties you assign is equal or lower than the total number of cells - goals.
        while len(self.penalties) < n_penalties:
            x = np.random.randint(0, self.side_length)
            y = np.random.randint(0, self.side_length)
            if (y, x) not in self.goals and (y, x) not in self.penalties:
                self.grid_environment[y, x] = -1
                self.penalties.append((y, x))
            if len(self.penalties) >= (self.side_length * self.side_length) - len(self.goals):
                break

    def print_goals_and_penalties(self):
        print("(y, x)")
        for i in range(len(self.goals)):
            print("Goal", i, ":", self.goals[i])
        for j in range(len(self.penalties)):
            print("Penalty", j, ":", self.penalties[j])

    def print_env_array_info(self):
        print("\n Environment side length = ", self.side_length, "\n Environment array: \n", self.grid_environment,
              "\n")

    def print_env_utility_map(self):
        plt.imshow(self.grid_environment, cmap='RdYlGn', interpolation='nearest')
        plt.title('Environment "True Utility" Map')
        plt.colorbar()

        # print labels on cells if env_side_length < 15
        if self.side_length <= 15:
            for i in range(self.side_length):
                for j in range(self.side_length):
                    plt.text(j, i, self.grid_environment[i, j], ha="center", va="center", color="k")
        plt.show()

    def assign_agent_start(self, startyx=(0, 0)):
        self.agent_start = [startyx[0], startyx[1]]
        self.grid_environment[startyx[0], startyx[1]] = 0

    def print_agent_start(self):
        print("Agent start:", self.agent_start)

    def get_started(self, agentyx=None):
        self.assign_goals(int(input("How many goals should the agent have? ")))
        self.assign_penalties(int(input("How many penalties should the environment contain? ")))
        if agentyx is None:
            self.assign_agent_start(
                (np.random.randint(0, self.side_length - 1), np.random.randint(0, self.side_length - 1)))
        else:
            self.assign_agent_start(agentyx)
        self.print_goals_and_penalties()
        self.print_agent_start()
        self.print_env_utility_map()


class Agent:

    def __init__(self, name, env_side_length):
        self.name = name
        self.env_side_length = env_side_length
        self.utility_map = np  # array of values between 1 and -1.
        self.position = ()
        self.lastposition = ()
        self.goals = []
        self.goal_distances = []
        self.finished_goals = []
        self.penalties = []
        self.vision_range = 2
        self.look_ahead_list = []
        self.immediate_neighbours = []
        self.all_neighbours = []
        self.last_neighbours = []
        self.score = 0

    def set_goals(self, goals):
        self.goals = goals

    def set_penalties(self, penalties):
        self.penalties = penalties

    def set_position(self, posyx):
        self.lastposition = self.position
        self.position = posyx

    def list_neighbours(self, posyx=None, repeat=0):
        self.last_neighbours = self.all_neighbours

        if posyx is None:
            posyx = self.position
            self.immediate_neighbours = []
            self.look_ahead_list = []
        neighboursy = []
        neighboursx = []

        for i in range(repeat + 1):
            if i == 0:
                neighboursy.append(posyx[0])
                neighboursx.append(posyx[1])
            else:
                neighboursy.append(posyx[0] + i)
                neighboursy.append(posyx[0] - i)
                neighboursx.append(posyx[1] + i)
                neighboursx.append(posyx[1] - i)

                if i == 1 and posyx == self.position:
                    for j in neighboursy:
                        for k in range(len(neighboursx)):
                            self.immediate_neighbours.append((j, neighboursx[k]))
                elif i == 1:
                    for j in neighboursy:
                        for k in range(len(neighboursx)):
                            self.look_ahead_list.append((j, neighboursx[k]))

        for i in neighboursy:
            for j in range(len(neighboursx)):
                if posyx == self.position:
                    self.all_neighbours.append((i, neighboursx[j]))

    def update_utility_map(self, source_map, data_positions=None, first_run=None):
        if data_positions is None:
            data_positions = []
        if first_run is True:
            self.utility_map = np.zeros((self.env_side_length, self.env_side_length))
            for i in range(len(self.goals)):
                self.utility_map[self.goals[i]] = 1
            for j in range(len(self.penalties)):
                self.utility_map[self.penalties[j]] = -1
            self.utility_map[(self.position[0], self.position[1])] = 0
        for i in data_positions:
            if i not in self.finished_goals:
                # if the data position is not a goal:
                try:
                    self.utility_map[i] = source_map[i]
                except IndexError:
                    print("vision scope has reached environment edges")

    def print_agent_utility_map(self):
        plt.imshow(self.utility_map, cmap='RdYlGn', interpolation='nearest')
        plt.title((self.name + ' "Subjective Utility" Map'))
        plt.colorbar()

        # print frame around current AI position
        ax = plt.subplot()
        ax.add_patch(Rectangle((self.position[1] - 0.5, self.position[0] - 0.5), 1, 1, fill=False, edgecolor='k', lw=4))

        # print frame around current goals
        for i in self.goals:
            ax.add_patch(
                Rectangle((i[1] - 0.5, i[0] - 0.5), 1, 1, fill=False, edgecolor='green', lw=4))

        # print labels on cells if env_side_length < 15
        if self.env_side_length <= 15:
            for i in range(self.env_side_length):
                for j in range(self.env_side_length):
                    plt.text(j, i, self.utility_map[i, j], ha="center", va="center", color="k")

        plt.show()

    def sort_goals(self):  # sorts agent goals
        for q in self.goals:
            if self.position == q:
                self.utility_map[q] = 0
                self.score += 1
                self.finished_goals.append(q)
                self.goals.remove(q)

        # re-initialise goal distances list
        self.goal_distances = []

        # repopulate the goal_distances list
        for i in self.goals:
            posyx = self.position
            goalyx = i
            self.goal_distances.append(((abs(posyx[0] - goalyx[0])), (abs(posyx[1] - goalyx[1]))))

        # sort list of goal distances
        def sort_goal_distances(e):
            # return e[0] + e[1]
            return e[0][0] + e[0][1]

        # sort goals according to distance (nearest to furthest)
        self.goals = [self.goals for _, self.goals in
                      sorted(zip(self.goal_distances, self.goals), key=sort_goal_distances)]

    def sort_moves(self):
        def compare_distances(move, goal):
            # compare current distance to goal with proposed distance to goal
            currentyx = ((self.position[0] - goal[0]), (self.position[1] - goal[1]))
            proposedyx = ((move[0] - goal[0]), (move[1] - goal[1]))
            return proposedyx, currentyx

        for i in self.immediate_neighbours:
            try:
                if self.utility_map[i] < 0:
                    self.utility_map[i] = round(self.utility_map[i] - 1 / 8, 2)
                self.list_neighbours(i)
                for k in self.look_ahead_list:
                    for g in self.goals:
                        proposed_distanceyx, current_distanceyx = compare_distances(k, g)
                        if abs(proposed_distanceyx[0]) < abs(current_distanceyx[0]) and abs(proposed_distanceyx[1]) < abs(
                                current_distanceyx[1]):
                            self.utility_map[k] = round(
                                self.utility_map[k] + 0.25 / (len(self.goals) + self.goals.index(g)),
                                2)
                            self.utility_map[i] = round(
                                self.utility_map[i] + 0.5 / (len(self.goals) + self.goals.index(g)),
                                2)
                        elif abs(proposed_distanceyx[0]) < abs(current_distanceyx[0]) or abs(proposed_distanceyx[1]) < abs(
                                current_distanceyx[1]):
                            self.utility_map[k] = round(
                                self.utility_map[k] + 0.125 / (len(self.goals) + self.goals.index(g)),
                                2)
                            self.utility_map[i] = round(
                                self.utility_map[i] + 0.25 / (len(self.goals) + self.goals.index(g)),
                                2)
                for j in self.goals:
                    proposed_distanceyx, current_distanceyx = compare_distances(i, j)
                    if abs(proposed_distanceyx[0]) < abs(current_distanceyx[0]) and abs(proposed_distanceyx[1]) < abs(
                            current_distanceyx[1]):
                        self.utility_map[i] = round(
                            self.utility_map[i] + 2 / (len(self.goals) + self.goals.index(j)), 2)
                    elif abs(proposed_distanceyx[0]) < abs(current_distanceyx[0]) or abs(proposed_distanceyx[1]) < abs(
                            current_distanceyx[1]):
                        self.utility_map[i] = round(
                            self.utility_map[i] + 1 / (len(self.goals) + self.goals.index(j)), 2)
            except IndexError:
                print("immediate neighbours are beyond the limits of the environment")

    def move_agent(self, posyx=None):  # , utility_map=self.utility_map):
        utility_list = []
        for i in self.immediate_neighbours:
            try:
                utility_list.append(self.utility_map[i])
            except IndexError:
                print("can't append utility for immediate neighbours beyond environment edge")
        if posyx is None:
            posyx = self.immediate_neighbours[utility_list.index(max(utility_list))]
        self.set_position(posyx)

    def run_agent(self, environment, moves=10):
        for i in range(moves):
            # needs to list neighbours to populate neighbours and past neighbours lists
            self.list_neighbours(repeat=self.vision_range)
            # needs to update utility map environment with last neighbours list
            self.update_utility_map(environment, self.last_neighbours)
            print(1, self.utility_map)
            # needs to update utility map environment with current all neighbours list
            self.update_utility_map(environment, self.all_neighbours)
            print(2, self.utility_map)
            # need to sort goals and moves
            self.sort_goals()
            self.sort_moves()
            # update utility map should not be called here because it will overwrite the output of sort_moves
            self.list_neighbours(repeat=self.vision_range)
            self.print_agent_utility_map()
            self.move_agent()

    def get_started(self, environment, start_position=(0, 0), goals=None, penalties=None, vision_range=0,
                    print_map=None):
        self.vision_range = vision_range
        if goals is None:
            goals = []
        self.set_position(start_position)
        self.set_goals(goals)
        self.set_penalties(penalties)
        self.sort_goals()
        self.sort_moves()
        self.list_neighbours(repeat=self.vision_range)
        self.update_utility_map(environment, self.all_neighbours, first_run=True)
        if print_map is True:
            self.print_agent_utility_map()


def main():
    moves = 10
    env_side_length = 10
    vision_range = 2
    E1 = Environment(env_side_length)  # creates an environment
    E1.get_started((5, 5))

    A1 = Agent("Classic Utilitarian", env_side_length)
    A1.get_started(E1.grid_environment, E1.agent_start, E1.goals, E1.penalties, vision_range, print_map=True)
    A1.run_agent(E1.grid_environment, moves=moves)
    # reset utility map here


# figure out what the agent does when it has no goals
# the agent's goals need to yield higher utility than the other immediate neighbours.
# the agent gets confused and doesn't move
# when the agent gets near the environment boundaries, it returns an error because it is trying to calculate
# utility for something that does not exist

if __name__ == '__main__':
    main()
