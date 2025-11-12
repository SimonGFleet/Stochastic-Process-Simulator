from matplotlib.figure import Figure
import numpy as np

#---INSTANT PLOTTING---

def instant_plot_1d(data, ax, canvas):
    '''Creates a plot in one dimension'''
    fig = canvas.figure
    fig.clf()

    ax = fig.add_subplot(111)
    for path in data:
        ax.plot(path)
    ax.set_xlabel("Steps")
    ax.set_ylabel("Value")
    ax.grid(True)
    canvas.draw()


def instant_plot_2d(data, ax, canvas):
    '''Creates a plot in two dimensions'''
    data = data[0]
    N = data.shape[0]
    
    X, Y = np.meshgrid(np.linspace(0,1,N), np.linspace(0,1,N))

    fig = canvas.figure
    fig.clf()

    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, data, cmap='viridis')

    ax.set_title("Brownian Sheet")
    ax.set_xlabel("x steps")
    ax.set_ylabel("y steps")
    ax.set_zlabel("Value")

    canvas.draw()



#---HISTOGRAM PLOTTING---
def histogram_plot_1d(data, ax, canvas):
    '''Plots histogram of final values of paths'''

    # Should update this so final_values is different depending on whether we have one or two dimensional path
    final_values = data[:, -1]

    fig = canvas.figure
    fig.clf()

    ax = fig.add_subplot(111)

    ax.hist(final_values, bins=10, edgecolor="black")
    ax.set_xlabel("Final Value")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    canvas.draw()


def histogram_plot_2d(data, ax, canvas):
    '''Plots histogram of final values of paths'''
    final_values = data[:, -1, -1]
    fig = canvas.figure
    fig.clf()

    ax = fig.add_subplot(111)

    ax.hist(final_values, bins=10, edgecolor="black")
    ax.set_xlabel("Final Value")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    canvas.draw()



#---ANIMATED PLOTTING---
def animate_plot_1d(data, ax, canvas, root, delay_ms=20):
    '''Animates the plotting of the paths
    It theoretically takes 10 seconds for the animation but this is subject to speed of the program.'''

    fig = canvas.figure
    fig.clf()

    ax = fig.add_subplot(111)
    current_step = 0
    max_steps = len(data[0])

    # Gets time for animation
    #speed = self.animation_speed.get()
    speed = 3
    speed_conversion = {1: 40, 2 : 20, 3 : 10, 4 : 5, 5 : 2}
    animation_time = speed_conversion[speed]

    total_frames = (1000 / delay_ms) * animation_time
    steps_per_update = max(int(max_steps / total_frames), 1)

    animate_step_1d(data, ax, canvas, current_step, max_steps, steps_per_update, delay_ms, root)


def animate_step_1d(data, ax, canvas, current_step, max_steps, steps_per_update, delay_ms, root):
    '''args: 
    steps_per_update - how many steps are plotted each time the function is called
    delay_ms - time in milliseconds between each call of the function
    function is recursively called plotting extra steps of the path each time until the full path is plotted'''
    # Clears plot 
    ax.clear()
    ax.set_xlabel("Steps")
    ax.set_ylabel("Value")
    ax.grid(True)
    # Plots paths up to a given step
    for p in data:
        ax.plot(p[: current_step])
    canvas.draw_idle()
    #Update new plotting limit
    current_step += steps_per_update

    if current_step < max_steps:
        # Waits a certain amount of time, then calls the function recursively until plot is finished.
        root.after(delay_ms, lambda: animate_step_1d(data, ax, canvas, current_step, max_steps, steps_per_update, delay_ms, root))


#---2D---

def animate_plot_2d(data, ax, canvas, root, delay_ms=30):
    fig = canvas.figure
    fig.clf()

    data = data[0]  # remove batch dimension
    N = data.shape[0]

    ax = fig.add_subplot(111, projection="3d")
    current_step = 1
    max_steps = N

    speed = 3
    speed_conversion = {1:40, 2:20, 3:10, 4:5, 5:2}
    animation_time = speed_conversion[speed]

    total_frames = (1000 / delay_ms) * animation_time
    steps_per_update = max(int(N / total_frames), 1)

    # start animation
    animate_step_2d(data, ax, canvas, current_step, max_steps, steps_per_update, delay_ms, root)
    


def animate_step_2d(data, ax, canvas, current_step, max_steps, steps_per_update, delay_ms, root):
    ax.clear()
    ax.set_title("")
    ax.set_xlabel("s")
    ax.set_ylabel("t")
    ax.set_zlabel("W(s,t)")

    N = current_step
    partial = data[:N, :N]

    X, Y = np.meshgrid(np.linspace(0,1,N), np.linspace(0,1,N))
    ax.plot_surface(X, Y, partial, cmap='viridis')

    canvas.draw_idle()

    current_step += steps_per_update

    if current_step < max_steps:
        root.after(delay_ms, lambda: animate_step_2d(data, ax, canvas, current_step, max_steps, steps_per_update, delay_ms, root))

#---EMPTY PLOT---
def display_empty_plot(gui):
    '''Sets the initial plot to be empty'''
    gui.ax.clear()
    gui.ax.set_title("Select a Path Type to Simulate")
    gui.ax.set_xlabel("Steps")
    gui.ax.set_ylabel("Value")
    gui.ax.grid(True)
    gui.canvas.draw()




def plot_data(gui, data, process):
    draw_method = gui.draw_method.get()
    gui.ax.clear()

    plot_dict = {
                1 : {"Instant" : instant_plot_1d, 
                    "Animated" : lambda data, ax, canvas: animate_plot_1d(data, ax, canvas, gui.root), 
                    "Histogram" : histogram_plot_1d},
                2 : {"Instant" : instant_plot_2d, 
                    "Animated" : lambda data, ax, canvas: animate_plot_2d(data, ax, canvas, gui.root),  
                    "Histogram" : histogram_plot_2d}
            }
    plot_dict[process.dim][draw_method](data, gui.ax, gui.canvas)

    