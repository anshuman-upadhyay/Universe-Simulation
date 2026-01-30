# 4 planet solar system
import pygame
import utils.constants as C
from physics.body import Body
import random
import math

def spawn_system(bodies,center) :
    #Central massive body (not fixed, just heavy)
    star_radius = 45
    star_density = 3.5
    star_mass = star_density * math.pi *(star_radius**2)

    star = Body(
        position=[center[0],center[1]],
        velocity=[0.0,0.0],
        mass= star_mass,
        radius=star_radius,
        color= C.YELLOW,
        body_id= len(bodies) +1 
    )
    bodies.append(star)

    #spawn orbiting bodies 
    for i in range(4) :
        r= 100 +i *70
        angle = random.uniform(0,2*math.pi)

        x= center[0] + r * math.cos(angle)
        y= center[1] + r * math.sin(angle)

        speed = math.sqrt(C.G * star.mass/r)
        vx = -math.sin(angle) *speed
        vy = math.cos(angle) *speed

        radius =random.randint(6,12)
        mass = math.pi * (radius**2)

        planet = Body(
            position=[x,y],
            velocity=[vx,vy],
            mass= mass,
            radius= radius,
            color = C.BLUE,
            body_id=len(bodies) +1 
        )
        bodies.append(planet)



