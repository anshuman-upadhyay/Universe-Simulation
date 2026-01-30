import math 
def apply_gravity(body_a,body_b,G,dt) :
    dx = body_b.position[0] -body_a.position[0] 
    dy = body_b.position[1] -body_a.position[1] 

    dist_sq = dx**2 + dy**2

    if dist_sq == 0 :
        return
    
    distance = math.sqrt(dist_sq)

    #Softening to prevent explosion at small distance
    softening= min(body_a.radius,body_b.radius) * 0.1
    dist_sq += softening **2

    #Force function
    force = (G *  body_a.mass * body_b.mass )/ dist_sq

    nx = dx/distance
    ny = dy/distance

    #Constant accelerations
    ax = force * nx/body_a.mass 
    ay = force * ny/body_a.mass 
    bx = -force * nx/body_b.mass 
    by = -force * ny/body_b.mass 

    #Velocity update
    body_a.velocity[0] += ax* dt
    body_a.velocity[1] += ay* dt
    body_b.velocity[0] += bx* dt
    body_b.velocity[1] += by* dt

