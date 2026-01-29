#physics/collision.py

import math


#Elastic collisions between two bodies(circular)
def resolve_body_collision(body_a,body_b,restitution=0.9):
    dx = body_b.position[0] - body_a.position[0]
    dy = body_b.position[1] - body_a.position[1]
    distance = math.hypot(dx,dy)

    #Avoid division by 0 
    if distance == 0 :
        return 
    # Overlap check :
    overlap= body_a.radius + body_b.radius - distance
    if overlap <= 0 :
        return
    
    #collision normal
    nx = dx/distance
    ny = dy/distance

    #Separate bodies (Correction in positions)
    body_a.position[0] -= nx*overlap / 2
    body_a.position[1] -= ny*overlap / 2
    body_b.position[0] += nx*overlap / 2
    body_b.position[1] += ny*overlap / 2
    
    #Relative Velocity
    rvx = body_b.velocity[0] - body_a.velocity[0]
    rvy =  body_b.velocity[1] - body_a.velocity[1]

    #Velocity along normal
    vel_along_normal = rvx*nx +rvy*ny
    if vel_along_normal > 0 :
        return 
    
    #Compute impulse Scalar
    impulse = -(1+restitution) * vel_along_normal
    impulse /= (1/body_a.mass  + 1/body_b.mass)

    ix = impulse * nx 
    iy = impulse * ny

    #Apply impulse
    body_a.velocity[0] -= ix/body_a.mass
    body_a.velocity[1] -= iy/body_a.mass
    body_b.velocity[0] += ix/body_b.mass
    body_b.velocity[1] += iy/body_b.mass











