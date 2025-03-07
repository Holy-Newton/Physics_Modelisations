#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 19:58:35 2025

@author: francoisdeberdt
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import sympy as sp
import statistics
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation

#-------------Inititalisation of the figure:

fig = plt.figure(facecolor='white')
ax = fig.add_subplot(projection = "3d", facecolor='white')

plt.subplots_adjust(bottom=0.5)
fig.set_size_inches(10,7)
ax.set_xlim([-15, 15]) 
ax.set_ylim([-15, 15])
ax.set_zlim([0, 25])

#-------------Variables:



Bx = 0
By = 0
Bz = 0.5
Vx = 0.2
Vy = 0.5
Vz = 0.1
q = 1
m = 1
t_s = 300
Y0 = [0 ,0 ,0 , 0.2, 0.5, 0.1]

#------------Differencials equations resolutions:

def f(t, Y, q, m, Bx, By, Bz):
    x, y, z, Vx, Vy, Vz = Y
    dxdt = Vx
    dydt = Vy
    dzdt = Vz
    ax = (q/m)*(Vy*Bz-Vz*By)
    ay = (q/m)*(Vz*Bx-Vx*Bz)
    az = (q/m)*(Vx*By-Vy*Bx)
    return [dxdt, dydt, dzdt, ax, ay, az]

def resolution(q, m, Bx, By, Bz):
    t=np.linspace(0,t_s, 10*t_s)
    sol = solve_ivp(f, [0,t_s], Y0, t_eval=t, args=(q,m, Bx, By, Bz), atol=1e-5, rtol=1e-5)
    return sol.y



new_plot = resolution(q,m, Bx, By, Bz)
trajectory, = ax.plot(new_plot[0], new_plot[1], new_plot[2], c='r')    

### ---------SLIDERS:
    
ax_slider = plt.axes([0.67, 0.4, 0.25, 0.03])
slider = Slider(ax_slider, 'Charge q', 0.1, 10.0, valinit=q)

ax1_slider = plt.axes([0.11, 0.4, 0.25, 0.03])
slider1 = Slider(ax1_slider, 'masse', 0.01, 5.0, valinit=m)

Bx_slider = plt.axes([0.25, 0.3, 0.25, 0.03])
sliderbx = Slider(Bx_slider, 'Bx', 0.01, 5.0, valinit=Bx)

By_slider = plt.axes([0.25, 0.2, 0.25, 0.03])
sliderby = Slider(By_slider, 'By', 0.01, 5.0, valinit=By)

Bz_slider = plt.axes([0.25, 0.1, 0.25, 0.03])
sliderbz = Slider(Bz_slider, 'Bz', 0.01, 5.0, valinit=Bz)

Vx_slider = plt.axes([0.65, 0.3, 0.25, 0.03])
sliderVx = Slider(Vx_slider, 'Vx', 0.01, 5.0, valinit=Vx)

Vy_slider = plt.axes([0.65, 0.2, 0.25, 0.03])
sliderVy = Slider(Vy_slider, 'Vy', 0.01, 5.0, valinit=Vy)

Vz_slider = plt.axes([0.65, 0.1, 0.25, 0.03])
sliderVz = Slider(Vz_slider, 'Vz', 0.01, 5.0, valinit=Vz)

# -----------Graph and updates options:
def update(val):
    global q
    global m
    global B
    global Y0
    q = slider.val
    m = slider1.val
    Bx = sliderbx.val
    By = sliderby.val
    Bz = sliderbz.val
    Y0[3] = sliderVx.val
    Y0[4] = sliderVy.val
    Y0[5] = sliderVz.val
    new_resol = resolution(q,m,Bx, By, Bz)
    trajectory.set_data(new_resol[0], new_resol[1]) ##set_data ne prends que x, y
    trajectory.set_3d_properties(new_resol[2])
    fig.canvas.draw_idle()    
    

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.text(0.15, 0.9, "Particule trajectory in uniform magnetic field: (by Holy_Newton)", fontsize=15, fontweight="bold", transform=fig.transFigure)


slider.on_changed(update)
slider1.on_changed(update)
sliderbx.on_changed(update)
sliderby.on_changed(update)
sliderbz.on_changed(update)
sliderVx.on_changed(update)
sliderVy.on_changed(update)
sliderVz.on_changed(update)

plt.show()    