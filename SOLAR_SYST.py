#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#"""
#Created on Sun Nov 17 14:19:13 2024
# @author: francoisdeberdt
#"""

import pygame
import math as m
pygame.init()

WIDTH, HEIGHT = 1000, 1000 ## Size of the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  ## Def of the window
pygame.display.set_caption("SOLAR SYSTEM simulation (from Holly_Newton)")  ## Caption

#-------------------------------###   COLOR   #### (RGB)--------------------------------------

WHITE = (240, 240, 240)
VENUS_YELLOW = (237, 201, 175)
YELLOW = (255, 255, 0)
BLUE = (34, 139, 230)
RED = (201, 52, 37)
DARK_GREY = (169, 169, 169)
SATURN_COLOR = (210, 180, 140)
JUPITER_COLOR = (200, 100, 50)
SPACE_GREY_BLUE = (10, 12, 40)

FONT = pygame.font.SysFont("arial", 12)
FONT_TITLE = pygame.font.SysFont("arial",30)


#-------------------------------------------------------------------------------------------

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67429e-11
    SCALE = 47/ AU  ## 250 pixels about one AU
    TIMESTEP = 3600*24 ## Like, "I wnat to look one year of this planet mvmt, there it's representating one day
    
    
    
    
    def __init__(self, x, y, radius, color, mass, name, number): ## caracteristics of our planets
        self.number= number
        self.name= name
        self.x= x
        self.y= y
        self.radius= radius
        self.color= color
        self.mass= mass
        
        self.orbit= []  # All the points of trajectory for the line mark
        self.sun= False # don't want the trajectory of the sun
        self.distance_to_sun=0
        
        self.x_vel=0  # Velocity
        self.y_vel=0
        
        
        
    def draw(self, win):  ## Draw metodes
        ## We draw a circle with the different parameters with draw.
        x = self.x * self.SCALE + WIDTH / 2   ## put in center, beacause (0,0) is the top left corner of the window)
        y = self.y * self.SCALE + HEIGHT /2   ## put i n center
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y= point
                x = x*self.SCALE + WIDTH /2
                y = y*self.SCALE + HEIGHT /2
                updated_points.append((x, y))
        
            pygame.draw.lines(win, WHITE, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x,y), self.radius)
        
        #----------Distance render-------------------------------
        
        
        
        
        
        
        
        if not self.sun: 
            
            Velocity= m.sqrt((self.x_vel)**2+(self.y_vel)**2)
            distance_text = FONT.render(f"- {self.name}: distance: {round(self.distance_to_sun/1000000000, 1)}.e6 km  velocity:{round(Velocity/1000, 1)} Km/s", 1, WHITE)  
            win.blit(distance_text, (120, 120 + ((HEIGHT)/30)* self.number))
            #win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
            #print(f"Rendered text: {distance_text}")
            #print(f"Text position: {(x - distance_text.get_width()/2, y - distance_text.get_height()/2)}")
            
        
        #-------------------### MATHS AND PHYSICS ARE LIFE###-------------------------------------

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = m.sqrt(distance_x**2+distance_y**2) ## distance sun/planet
        
        if other.sun: # warning with the sun we classed in "planet" (wich is a star in reality...)
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / (distance**2)
        theta = m.atan2(distance_y, distance_x)
        force_x = m.cos(theta) * force
        force_y = m.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):   ### PAS COMPRIS, A REVOIR !!!!!!!!!
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        self.x_vel += total_fx /self.mass *self.TIMESTEP
        self.y_vel += total_fy /self.mass *self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
   

        

#------------------------------------------------------------------------------------------------


def main():  ## Condition; if run is True, keep running, if quit is True, turn "Keep reunning" flase/ Quit and break
    run =True
    clock = pygame.time.Clock() ## To not update at the speed of the computer
    
    days_passed = 0
    #----------------------### NOW LET'S DEFINE OUR PLANETS !!! ###--------------------------
    
                     
    sun= Planet(0, 0, 11, YELLOW, 1.98892*10**30, "Sun", 0)   #mass in kg
    sun.sun = True # remember the self.sun = False in Planet class
    
    mercury = Planet(0.47 *Planet.AU, 0, 2, DARK_GREY, 3.30 *10**23, "Mercury", 1)
    mercury.y_vel = -38.773 * 1000
    
    venus = Planet(0.728 *Planet.AU, 0, 4, VENUS_YELLOW, 4.8685 *10**24, "Venus", 2)
    venus.y_vel = -34.776 * 1000
    
    earth = Planet(-1.017 *Planet.AU, 0, 4, BLUE, 5.9742*10**24, "Earth", 3)
    earth.y_vel = 29.227 * 1000 
    
    mars = Planet(-1.666 *Planet.AU, 0, 3, RED, 6.39*10**23, "Mars", 4)
    mars.y_vel = 21.983 * 1000
    
    jupiter = Planet(5.455 * Planet.AU, 0, 10, JUPITER_COLOR, 1.898 * 10**27, "Jupiter", 5)
    jupiter.y_vel = -12.450 * 1000 
    
    saturn = Planet(10.123 * Planet.AU, 0, 7, SATURN_COLOR, 5.683 * 10**26, "Saturn", 6)
    saturn.y_vel = -9.099 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn]
    

    #------------------------------### Syst run ###----------------------------------------------
    while run:
        clock.tick(60)  ## Max I will be able to update at
        WIN.fill(SPACE_GREY_BLUE) ## Color of the background (Black as default, not obligate in this case)
        
        
        days_passed+=1
        
        Intern_title=FONT_TITLE.render(f"Solar System Simulation: {days_passed} days passed ", 1, WHITE)
        WIN.blit((Intern_title), (100,100))
        
    
        

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update() ### EXTREMLY IMPORTANT, loop the update, without that nothing....
        
    pygame.quit()
                
main()  ## To open the window

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        