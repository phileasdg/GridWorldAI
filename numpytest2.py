# # import numpy as np
# #
# # array = np.around(np.random.uniform(-0.9, 0.9, (10, 10)), decimals=1)  # decimal grid
# # array[0, 0] = 2
# # array[-1, 0] = 5
# # print(array)
#
# n = 1
# posyx = [3, 1]
# listy = []
# listx = []
# for i in range(n+1):
#     if i == 0:
#         listy.append(posyx[0])
#         listx.append(posyx[1])
#     else:
#         listy.append(posyx[0]+i)
#         listy.append(posyx[0]-i)
#         listx.append(posyx[1]+i)
#         listx.append(posyx[1]-i)
# print(listy, listx)
#
#
# lst = [1, 5]
# K = 6
# print(lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))])

# goalpositions = [(5, 5), (10, 12), (9, 4), (30, 21)]
# goalsdist = [(1, 0), (1, 5), (0, 0), (10, -15)]
#
# def sort(goals, goal_distances):
#     # takes in as parameters two lists: goal distances (the vectors needed to get to goals) and goal coordinates
#     # sort list of goal distances
#     def sortgoals(e):
#         return e[0][0] + e[0][1]
#     goals = [goals for _, goals in sorted(zip(goal_distances, goals), key=sortgoals, reverse=True)]
#     print(goals)
#
# print(goalsdist)
# print(goalpositions)
#
# sort(goalpositions, goalsdist)

currentyx = (-4, 0)
proposedyx = (5, 7)
goal = (5, 5)

current_distance_yx_to_goal_yx = (currentyx[0] - goal[0])+(currentyx[1] - goal[1])
proposed_distance_yx_to_goal_yx = (proposedyx[0] - goal[0])+(proposedyx[1] - goal[1])

print("current distance yx", current_distance_yx_to_goal_yx, "proposed distance yx", proposed_distance_yx_to_goal_yx)
# if proposed distance x is less than current distance x, add points to proposed distance x
