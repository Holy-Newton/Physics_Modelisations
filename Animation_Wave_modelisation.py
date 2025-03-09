#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 09:50:17 2025

@author: francoisdeberdt
"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import statistics
from scipy.integrate import solve_ivp
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation


fig = plt.figure()
ax = plt.subplot()
plt.subplots_adjust(bottom = 0.3)

t = 0
k = 1
w = 2
x = np.linspace(0, 30, 500)
fps = 20

sliderk = plt.axes([0.67, 0.2, 0.25, 0.03])
k_slide = Slider(sliderk, "k", 0, 10, valinit= k)

sliderw = plt.axes([0.15, 0.2, 0.25, 0.03])
w_slide = Slider(sliderw, "w", 0, 10, valinit= w)


def f(t, k, w, x): return np.cos(k*x - w*t)


def update(fps):
    global t, k, w
    k = k_slide.val
    w = w_slide.val
    t += +0.1
    ax.clear()
    ax.plot(x, f(t, k, w, x))
    fig.canvas.draw()


ax.plot(x, f(t, k, w, x))
ax.set_xlabel('X')
ax.set_ylabel('Amplitude(x,t)')
plt.text(0.12, 0.9, "Wave Plane progression with cos(kx - wt): (by Holy_Newton)", fontsize=11, fontweight="bold", transform=fig.transFigure)


ani = FuncAnimation(fig, update, interval = 1000/fps)

plt.show







