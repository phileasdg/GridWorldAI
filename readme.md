# This program is designed to facilitate AI agent testing in grid world environments. The program's functionality
includes the following:
- generating AI grid worlds at any scale.
- providing a framework to create and implement AI agents to interact in these grid world environments.
- providing a framework to visualise AI-environment interactions with data export capabilities.
- an example of AI agent implemented to interact with these grid worlds, with adjustable personal utility bias, utility
function, look ahear search, and start position.

![simulation example](https://raw.githubusercontent.com/phileasdg/GridWorldAI/main/simulation2.gif)

# How to use this program:
1) by editing this master program and adding your own AI implementation
- create an environment object from the environment class and specify its size and whether it should be empty.
- run the environment object's get started method - optional: specify in attributes the agent start position and whether
to save the gridworld plots as png files
- create an agent object from the agent class and specify its name and the dimensions of its environment.
- run the agent object's get started function
- run the agent object's run function

2) by importing this program into your program
- add "import GridworldAI" to your python project header
- generate an environment by creating an environment object and following the directions specified above
- generate an agent by creating an agent object, or design an agent which takes as its input the environment object's
environment grid world.
- run the agent and study the results!

# Description:
The Agent has an environment to navigate which contains goals and penalties. Every turn, it moves, and everywhere it
goes, it changes the environment. Every move is associated with a utility value which can be positive or negative.
Thus, an action can either be neutral (the environment is not disturbed by the action of the AI), a positive action
(the AI achieves or approaches a goal and the environment is not disturbed), or negative (the environment is disturbed,
or the move shifts tha AI away from its goal, or makes makes it harder for the AI to achieve its goal).
The agent is tasked with finding the most optimal ways of navigating this environment given specified environment configurations.
