import PIL
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

side_length = 15

def animate(data, im):
    im.set_data(data)

def step():
    while True:
        data = np.random.rand(side_length, side_length)
        yield data

fig, ax = plt.subplots()
im = ax.imshow(np.random.rand(side_length, side_length), interpolation='nearest')
ani = animation.FuncAnimation(
    fig, animate, step, interval=100, repeat=True, fargs=(im, ))
# plt.show()
ani.save("sine_wave.gif", writer='pillow')
print("finished")
