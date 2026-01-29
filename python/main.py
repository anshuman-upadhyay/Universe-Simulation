import pygame
from renderer.window import create_window
from renderer.draw import clear_screen, draw_body,draw_active_shadow
import utils.constants as C
from physics.body import Body
from physics.collision import resolve_body_collision
# ---------------- Global Variables----------------
is_dragging = False
drag_offset = [0.0,0.0]
active_body = None
body_counter = 0
THROW_STRENGTH = 50
BAT_FORCE = 1200
DAMPING_COEFF = 1
# ---------------- Event handling ----------------
def handle_events(bodies,dt):
    #Mouse grabbing 
    global is_dragging, drag_offset,active_body,body_counter,THROW_STRENGTH,BAT_FORCE,DAMPING_COEFF
    #Event selection 
    for event in pygame.event.get():
        #Over simulation
        if event.type == pygame.QUIT:
            return False
        
        #Spawn new bodies on the ball 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n :
            mouse_x,mouse_y = pygame.mouse.get_pos()
            body_counter += 1
            new_body = Body(
                    position=[mouse_x,mouse_y],
                    velocity=[0.0,0.0],
                    mass=10,
                    radius=15,
                    color=C.WHITE,
                    body_id=body_counter
                    )
            bodies.append(new_body) 
            #Set the active default body the latest one
            active_body=new_body
            is_dragging=False  
            

        #Trackpad control

        #Ball Teleportation 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and active_body:
            mouse_x,mouse_y = pygame.mouse.get_pos()

            #instant teleportation 
            active_body.position[0]= mouse_x
            active_body.position[1]= mouse_y

            #Kill Velocity
            active_body.velocity[0] = 0.0 
            active_body.velocity[1] = 0.0 

            #Cancle drag
            is_dragging = False


        # Mouse Ball grab
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            for body in reversed(bodies):
                dx= mouse_x - body.position[0]
                dy= mouse_y - body.position[1]
                dist_sq = dx *dx + dy* dy

                if dist_sq <= body.radius**2 :
                    active_body=body
                    is_dragging = True
                    drag_offset[0]= body.position[0] - mouse_x
                    drag_offset[1]= body.position[1] - mouse_y
                    body.velocity = [0,0]
                    break
            
         #Ball has been released     
        if event.type == pygame.MOUSEBUTTONUP and event.button ==1 :
            is_dragging = False
            
        
        #Mouse motion while draggign
        if event.type == pygame.MOUSEMOTION and is_dragging and active_body :
            mouse_x,mouse_y = pygame.mouse.get_pos()
            active_body.position[0] = mouse_x + drag_offset[0]
            active_body.position[1] = mouse_y + drag_offset[1]


            #Inertia after release
            dx,dy = event.rel
            active_body.velocity[0] = dx*THROW_STRENGTH
            active_body.velocity[1] = dy*THROW_STRENGTH

        #If the mouse is not holding on to the ball 
        if not is_dragging and active_body:
            #KeyBoard Control
            keys=pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                active_body.velocity[1] -= BAT_FORCE *dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                active_body.velocity[1] += BAT_FORCE *dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                active_body.velocity[0] -= BAT_FORCE *dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                active_body.velocity[0] += BAT_FORCE *dt
            

    return True


# ---------------- Driver function ----------------
def main():
    pygame.init()

    screen, clock = create_window()

    # bodies creation
    bodies=[]

    running = True  # loop control flag
    

    while running:
        # Delta time (seconds)
        dt = clock.tick(C.FPS) / 1000.0

        #Loop control variable
        running = handle_events(bodies,dt)

        for body in bodies :
            body.update(dt)# Update physics  
         #Body-body collisions
        for i in range(len(bodies)) :
            for j in range(i+1,len(bodies)) :
                resolve_body_collision(bodies[i],bodies[j])

        #Boundary + damping
        for body in bodies :
            body.handle_boundary_collision(C.WIDTH,C.HEIGHT)
            body.velocity[0] *= DAMPING_COEFF
            body.velocity[1] *= DAMPING_COEFF



        # Render
        clear_screen(screen, C.BACKGROUND_COLOR)
        #Handle n bodies 
        font=pygame.font.SysFont(None,18)
        for body in bodies :
            if body == active_body :
                draw_active_shadow(screen,body)
            draw_body(screen,body,font)


        pygame.display.flip()

    pygame.quit()


# ---------------- Entry point ----------------
if __name__ == "__main__":
    main()
