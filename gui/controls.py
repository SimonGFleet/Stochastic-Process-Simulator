import tkinter as tk
from tkinter import ttk
import numpy as np
from gui.stats_config import open_stats_menu


def initialise_controls(gui):
    '''Adds the initial required controls to the user interface'''
    # Button to produce plot
    gui.sim_button = ttk.Button(gui.root, text="Simulate", command=gui.run_simulation)
    gui.sim_button.grid(row=0, column=0)

    # Choose path to simulate
    gui.path_choice = ttk.Combobox(gui.root, values=list(gui.path_types.keys()))
    gui.path_choice.set("Select a Path")
    gui.path_choice.grid(row=0, column=1)
    gui.path_choice.bind("<<ComboboxSelected>>", gui.on_process_change) 

    # Choose drawing method
    drawing_methods = ["Instant", "Animated", "Histogram"]
    gui.draw_method = ttk.Combobox(gui.root, values=drawing_methods)
    gui.draw_method.bind("<<ComboboxSelected>>", gui.on_draw_method_change)
    gui.draw_method.set("Instant")
    gui.draw_method.grid(row=0, column=2)  

    gui.stats_button = ttk.Button(gui.root, text="Statistics", command=lambda: open_stats_menu(gui))
    gui.stats_button.grid(row=0, column=3)


def apply_ui(gui):
    '''Adds in parameter selection for the given ui_spec of the current stochastic process'''
    # Clear existing sliders
    for widget in getattr(gui, "slider_widgets", []):
        widget.destroy()
    gui.slider_widgets = []
    gui.sliders = {}

    # Dictionary of specific UI requirements for path type
    spec = gui.current_process.ui_spec()

    if gui.draw_method.get() == "Histogram":
        # Force number of paths slider
        spec = spec.copy()  # don't mutate class dict
        spec["Number of Paths"] = {"min": 10, "max": 1000, "default": 100, "scale": "int"}
        spec["Number of Steps"] = {"min": 10, "max": 10000, "default": 100, "scale": "log"}

    column = 0

    for name, params in spec.items():

        # detect scale mode
        if params.get("scale") == "log":
            # log step slider (integer exponent slider)
            slider = tk.Scale(gui.root, label=name, from_=np.log10(params["min"]), to=np.log10(params["max"]),
                            orient="horizontal", resolution=1)
            slider.set(np.log10(params["default"]))

        elif params.get("scale") == "int":
            slider = tk.Scale(gui.root, label=name, from_=params["min"], to=params["max"],
                            orient="horizontal", resolution=1)
            slider.set(params["default"])
        else:
            slider = tk.Scale(gui.root, label=name, from_=params["min"], to=params["max"],
                            orient="horizontal", resolution=0.1)
            slider.set(params["default"])

        # Set position of slider 
        slider.grid(row=1, column=column)
        # Add slider to widgets 
        gui.slider_widgets.append(slider)

        gui.sliders[name] = slider
        column += 1