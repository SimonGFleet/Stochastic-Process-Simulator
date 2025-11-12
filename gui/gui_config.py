import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # type: ignore
import numpy as np
from stochastic_processes import EmptyPlot, StochasticProcess, processes
from plotter import plot_data, display_empty_plot
from gui.stats_config import update_statistics, make_possible_stats
from gui.controls import initialise_controls, apply_ui




class GUI:
    '''Main application class, handles the user interface, input controls and plotting.'''
    def __init__(self, window):
        self.root = window
        self.root.title("Stochastic Simulator GUI")
        self.root.geometry("1100x700")

        # Choose class from stochastic_processes.py
        self.path_types = processes
        
        # Create figure
        self.fig = Figure(figsize=(8, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=3)

        # Get the a tool bar to save simulations
        self.toolbar_frame = tk.Frame(self.root)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()
        self.toolbar_frame.grid(row=4, column=0, columnspan=2)

        # Initialise set up
        self.current_process = EmptyPlot
        self.animation_running = False
        self.paths = np.array([])
        initialise_controls(self)
        display_empty_plot(self)
        self.stat_options = make_possible_stats(self.root)
        self.stats_label = tk.Label(self.root, text= "STATISTICS:")
        self.stats_label.grid(row=5, column=0)
        
    def on_process_change(self, event=None):
        '''Handles changing of stochastic process
        creates a new instance of the chosen path and updates the ui accordingly'''
        process_name  = self.path_choice.get() # type: ignore
        ProcessClass  = self.path_types[process_name]
        self.current_process = ProcessClass()   
        spec = self.current_process.ui_spec()       
        apply_ui(self)

    def on_draw_method_change(self, event=None):
        '''Handles changing of draw method, updates the ui accordingly'''
        if hasattr(self, "current_process"):
            apply_ui(self)

    def get_params(self, process: StochasticProcess):
        '''Collects the current values of each of the sliders present.
        Scales the valeus appropriately if they are log in value,

        Args:
            process (StochasticProcess) class instance whos ui_spec defines the slider configurations
            
        Returns:
            params (dict) with name of parameter and its value'''
        params = {}
        # Get info on behaviour of sliders for process
        spec = process.ui_spec()

        for name, slider in self.sliders.items(): # type: ignore
            mode = spec.get(name, {}).get("scale", "float")
            if mode == "log":
                # slider gives exponent, so convert back
                params[name] = int(10 ** slider.get())
            elif mode == "int":
                params[name] = int(slider.get())
            else:
                params[name] = float(slider.get())

        return params

    def run_simulation(self):
        '''Function to run the simulation, it creates an instance of the correct class, 
        gets the correct parameters, simulates the paths, 
        then plots the data and updates the statistics.'''
        # Choose correct class
        process_name  = self.path_choice.get() # type: ignore
        ProcessClass  = self.path_types[process_name]

        # End simulation early if no path is chosen
        if process_name == "Select a Path":
            display_empty_plot(self)
            return
        
        # Initialise class
        process = ProcessClass()

        # Get chosen variables
        params = self.get_params(process)
        num_paths = 1
        if "Number of Paths" in params.keys():
            num_paths = params["Number of Paths"]
        # Simulate paths
        data = np.array([process.simulate(params) for i in range(int(num_paths))])
        plot_data(self, data, process)
        update_statistics(self, data)