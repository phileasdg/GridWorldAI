import PIL
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.animation as animation



side_length = 15

def animate(data, im):
    im.set_data(data)

def step():
    while True:
        # data = self.utility_map
        data = np.random.rand(side_length, side_length)
        yield data

fig, ax = plt.subplots()
ax.add_patch(Rectangle((1 - 0.5, 5 - 0.5), 1, 1, fill=False, edgecolor='k', lw=4))
im = ax.imshow(np.random.rand(side_length, side_length), interpolation='nearest')
ani = animation.FuncAnimation(
    fig, animate, step, interval=100, repeat=True, fargs=(im, ))
# plt.show()
ani.save("sine_wave.gif", writer='pillow')
print("finished")
