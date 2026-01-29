class Body :
    def __init__(self,position,velocity,mass,radius,color,body_id): 
        self.position = position
        self.velocity = velocity 
        self.mass = mass 
        self.radius =radius 
        self.color = color
        self.id = body_id 
    #Positional changes 
    def update(self,dt) :
        #Changing the xy coordinates of using the veloctiy and delta time 
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    #Handling boundary based collision
    def handle_boundary_collision(self,width,height, restitution = 0.9):
        #Left wall 
        if self.position[0] - self.radius < 0 :
            self.position[0] = self.radius 
            self.velocity[0] *= -restitution
            
        #Right wall 
        if self.position[0] + self.radius > width :
            self.position[0] = width -  self.radius 
            self.velocity[0] *= -restitution
        #Top wall 
        if self.position[1] - self.radius < 0 :
            self.position[1] = self.radius 
            self.velocity[1] *= -restitution
        #Bottom wall 
        if self.position[1] + self.radius > height :
            self.position[1] = height - self.radius 
            self.velocity[1] *= -restitution





















#-----------------------------------------------------------------------------------------------------------------------------------------------------#
# Variable information 
"""
position : [x, y]
velocity : [vx, vy]
mass     : float
radius   : int
color    : (R, G, B)
"""


#For boundary collision logic 
"""
        Bounce the body off screen boundaries.

        restitution < 1 → energy loss
        restitution = 1 → perfect bounce
"""