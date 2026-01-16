class Body :
    def __init__(self,position,velocity,mass,radius,color): 
        self.position = position
        self.velocity = velocity 
        self.mass = mass 
        self.radius =radius 
        self.color = color 
    def update(self,dt) :
        #Changing the xy coordinates of using the veloctiy and delta time 
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt



#-----------------------------------------------------------------------------------------------------------------------------------------------------#
# Variable information 
"""
position : [x, y]
velocity : [vx, vy]
mass     : float
radius   : int
color    : (R, G, B)
"""