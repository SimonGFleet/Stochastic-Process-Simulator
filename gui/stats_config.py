from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_config import GUI

from tkinter import ttk
import numpy as np
import tkinter as tk

from statsfile import avg_stat, linear_variation, quadratic_variation, cubic_variation


def update_statistics(gui: GUI, data: np.ndarray) -> None:
    '''Checks whichs statsitics are to be displayed
    if they are to be displayed then it calculates the statistic and adds to results'''
    results = []
    if data.ndim == 2:
        final_vals = data[:, -1]
    elif data.ndim == 3:
        final_vals = data[:, -1, -1]
    else: 
        return # Shouldnt run this line
    
    if gui.stat_options["Linear Variation"].get():
        lin = avg_stat(linear_variation, data)
        results.append(f"Linear Var: {lin:.2f}")

    if gui.stat_options["Quadratic Variation"].get():
        quad = avg_stat(quadratic_variation, data)
        results.append(f"Quadratic Var: {quad:.2f}")

    if gui.stat_options["Cubic Variation"].get():
        cubic = avg_stat(cubic_variation, data)
        results.append(f"Cubic Var: {cubic:.2f}")

    if gui.stat_options["Mean (final value)"].get():
        results.append(f"Mean: {np.mean(final_vals):.2f}")

    if gui.stat_options["Variance (final value)"].get():
        results.append(f"Variance: {np.var(final_vals):.2f}")

    # Adds the calculated results to teh display   
    display = "\n".join(results)
    gui.stats_label.config(text=display)


def make_possible_stats(master: tk.Tk) -> dict:
    '''Helper function to get dictionary for possible stats
    Returns:
        possible_stats (dict) options for which statistics to display'''
    possible_stats = {
        "Linear Variation" : tk.BooleanVar(master, value=True),
        "Quadratic Variation" : tk.BooleanVar(master, value=True),
        "Cubic Variation" : tk.BooleanVar(master, value=True),
        "Mean (final value)" : tk.BooleanVar(master, value=True),
        "Variance (final value)" : tk.BooleanVar(master, value=True)
        }
    return possible_stats


def open_stats_menu(gui: GUI):
    '''Creates a new window to select which statistics to calculate'''
    win = tk.Toplevel(gui.root)
    win.title("Select Statistic")
    win.geometry("300x200")

    tk.Label(win, text="Choose statistics:", font=("Arial", 10, "bold")).pack(pady=5)

    for stat, var in gui.stat_options.items():
        ttk.Checkbutton(win, text=stat, variable=var).pack(anchor="w", padx=10)