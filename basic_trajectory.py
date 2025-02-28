#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:30:59 2025

@author: francoisdeberdt
"""

###THE GOAL OF THIS PROGRAM IS TO RE_VIEW THE BASICS OF TRAJECTORY SIMULATION/ GRAPHIC VISUALISATION/ AND TRAJECTORY DATA COLLECTION.

import numpy as np
import matplotlib.pyplot as plt

# ASKED INFORMATIONS ------------------------------
v_0 = int(input("enter the t=0 Velocity in m/s : "))
while v_0<0:
    print("error because not in the range asked, retry")
    v_0 = int(input("enter the t=0 Velocity in m/s : "))

teta_0 = int(input("enter the original angle of trajectory in degrees [0;90]: "))
while teta_0>90 or teta_0<0:
    print("error because not in the range asked, retry")
    teta_0 = int(input("enter the original angle of trajectory in degrees [0;90]: "))


y_0 = int(input("enter the t=0 altitude in meters : "))
while y_0<0:
    print("error because not in the range asked, retry")
    y_0 = int(input("enter the t=0 altitude in meters : "))
if y_0 == 0:
    y_0 = 0.01    


#--------------------------------------------------
# constants:
    
time_step = 0.1
G = 6.6742*10**(-11)
M_earth = 5.9737*10**24

#Prorotype specifications:
wet_surface = 1200
lenght = 33
mass = 60000




##------VISCOSITY OF AIR AND FROTTEMENT------------

def Ff(altitude, L, V, W_S):
    # Calcul du Mach number
    Mach = mach_number(altitude, V)
    # Calcul de la densité de l'air à l'altitude donnée
    density = air_density(altitude)
    # Calcul du Reynolds number
    Re = reynolds_number(altitude, L, V)

    # Si la densité ou le Reynolds number est trop bas, return 0
    if density <= 0 or Re <= 0:
        return 0

    # Si le Reynolds number est faible (cas non réaliste), return 0
    if Re < 1e3:
        return 0

    # Calcul du coefficient de frottement (Cf)
    Cf = (0.664 / (Re ** 0.5)) * (1 + 2.1 / Mach)
    # Calcul de la force de frottement
    Ff = 0.5 * density * (V) ** 2 * W_S * Cf

    return Ff*25

def mach_number(altitude, V):
    speed_of_sound = np.sqrt(1.4 * 287.05 * temperature_at_altitude(altitude))  # Vitesse du son
    return V / speed_of_sound

def reynolds_number(altitude,L,V):
    
    P = air_density(altitude)
    mu = dynamic_viscosity(altitude)
    if mu == 0:
        Re = 0
    else:
        Re = (P*V*L)/mu
    return Re


def temperature_at_altitude(altitude):
    if altitude <= 11000:  # Troposphère
        return 288.15 - 0.0065 * altitude
    elif altitude <= 20000:  # Stratosphère (isotherme)
        return 216.65
    elif altitude <= 32000:  # Stratosphère moyenne
        return 216.65 + 0.001 * (altitude - 20000)
    elif altitude <= 47000:  # Stratosphère supérieure
        return 228.65 + 0.0028 * (altitude - 32000)
    elif altitude <= 51000:  # Stratopause (isotherme)
        return 270.65
    elif altitude <= 71000:  # Mésosphère inférieure
        return 270.65 - 0.0028 * (altitude - 51000)
    elif altitude <= 80000:  # Mésosphère supérieure
        return 214.65 - 0.002 * (altitude - 71000)
    else:
        return 0  # Espace, température négligeable

def dynamic_viscosity(altitude):
    """
    Calcule la viscosité dynamique de l'air (μ) en fonction de l'altitude.
    Altitude en mètres, viscosité retournée en Pa·s.
    """
    # Constantes
    mu_0 = 1.716e-5  # Viscosité de référence (Pa·s)
    T0 = 273.15      # Température de référence (K)
    C = 110.4        # Constante de Sutherland (K)

    
    # Température à l'altitude donnée
    T = temperature_at_altitude(altitude)
    if T <= 0:
        T = 1e-3  # Pas de viscosité définie pour l'espace ou températures négatives

    # Loi de Sutherland
    mu = mu_0 * (T / T0)**1.5 * (T0 + C) / (T + C)
    return mu



def air_density(altitude):
    """
    Calcul de la densité de l'air en fonction de l'altitude (en mètres).
    Retourne 0 pour l'espace (>80 km).
    """
    if altitude > 80000:
        return 0.0  # Pas d'air au-delà de 80 km
    
    # Constantes
    R = 287.05       # Constante spécifique de l'air sec (J/kg·K)
    g0 = 9.80665     # Accélération gravitationnelle (m/s²)
    P0 = 101325      # Pression standard au niveau de la mer (Pa)
    T0 = 288.15      # Température standard au niveau de la mer (K)
    
    # Couches atmosphériques : (altitude base, altitude sommet, gradient thermique)
    layers = [
        (0, 11000, -0.0065),   # Troposphère
        (11000, 20000, 0.0),   # Stratosphère inférieure
        (20000, 32000, 0.001), # Stratosphère moyenne
        (32000, 47000, 0.0028),# Stratosphère supérieure
        (47000, 51000, 0.0),   # Stratopause
        (51000, 71000, -0.0028),# Mésosphère inférieure
        (71000, 80000, -0.002) # Mésosphère supérieure
    ]
    
   
    P = P0
    T = T0
    
    for base, top, lapse_rate in layers:
        if altitude <= top:
            if lapse_rate == 0:
                
                # Couche isotherme
                P = P * np.exp(-g0 * (altitude - base) / (R * T))
            else:
                # Couche avec gradient thermique
                T = T + lapse_rate * (altitude - base)
                P = P * (T / (T - lapse_rate * (altitude - base))) ** (-g0 / (lapse_rate * R))
            break
        else:
            # Mise à jour pour la couche suivante
            if lapse_rate == 0:
                P = P * np.exp(-g0 * (top - base) / (R * T))
            else:
                T = T + lapse_rate * (top - base)
                P = P * (T / (T - lapse_rate * (top - base))) ** (-g0 / (lapse_rate * R))
            altitude -= (top - base)
    
    # Calcul de la densité
    rho = P / (R * T)
    return rho

#--------------------------------------------------

def xy_velocity_0(v_0,teta_0):
    Vx=np.cos(np.radians(teta_0))*v_0
    Vy=np.sin(np.radians(teta_0))*v_0
    
    return Vx,Vy


def trajectory(v_0,teta_0,y_0):
    Vx,Vy = xy_velocity_0(v_0,teta_0)
    y = y_0
    x = 0
    time = 0
    x_data = [0]
    y_data = [y_0]
    Vx_data = [Vx]
    Vy_data = [Vy]
    time_data = [0]
    while y>0:
        g = (G * M_earth) / ((y+6371000)**2)   
        Vy = Vy - g*time_step - (Ff(y,lenght,Vy,wet_surface)/mass)*time_step
        Vx = Vx - (Ff(y,lenght,Vx,wet_surface)/mass)*time_step
        x = x + Vx*time_step
        y = y + Vy*time_step
        time=time+time_step
        
        x_data.append(x)
        y_data.append(y)
        Vx_data.append(Vx)
        Vy_data.append(Vy)
        time_data.append(time)
        print(Ff(y,lenght,Vy,wet_surface))
        
    return x_data, y_data, Vx_data, Vy_data, time_data

x_data, y_data, Vx_data, Vy_data, time_data = trajectory(v_0,teta_0,y_0)

def high_time(y_data, time_data):
    max_altitude = max(y_data)
    max_time = time_data[y_data.index(max_altitude)]
    return max_altitude, max_time

print(high_time(y_data,time_data))


#---------------------------------------------

plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data)
plt.xlabel("X trajectory (m)")
plt.ylabel("Height trajectory (m)")
plt.title("X vs Height")
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(time_data, Vy_data)
plt.xlabel("Time (s)")
plt.ylabel("Vy velocity (m/s)")
plt.title("Vy vs Time")
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(time_data, Vx_data)
plt.xlabel("Time (s)")
plt.ylabel("Vx velocity (m/s)")
plt.title("Vx vs Time")
plt.grid(True)
plt.show()
















