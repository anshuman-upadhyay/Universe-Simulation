import pygame
from renderer.window import create_window
from renderer.draw import clear_screen, draw_body
import utils.constants as C
from physics.body import Body
# ---------------- Global Variables----------------
is_dragging = False
drag_offset = [0.0,0.0]


# ---------------- Event handling ----------------
def handle_events(body,dt):
    #Mouse grabbing 
    global is_dragging, drag_offset
    #Event selection 
    for event in pygame.event.get():
        #Over simulation
        if event.type == pygame.QUIT:
            return False
        #Trackpad control
        #Ball Teleportation 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 :
            mouse_x,mouse_y = pygame.mouse.get_pos()

            #instant teleportation 
            body.position[0]= mouse_x
            body.position[1]= mouse_y

            #Kill Velocity
            body.velocity[0] = 0.0 
            body.velocity[1] = 0.0 

            #Cancle drag
            is_dragging = False


        # Mouse Ball grab
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x,mouse_y = pygame.mouse.get_pos()

            dx= mouse_x - body.position[0]
            dy= mouse_y - body.position[1]
            dist_sq = dx *dx + dy* dy

            if dist_sq <= body.radius * body.radius :
                is_dragging = True
                drag_offset[0]= body.position[0] - mouse_x
                drag_offset[1]= body.position[1] - mouse_y
                body.velocity = [0,0]
        
         #Ball has been released     
        if event.type == pygame.MOUSEBUTTONUP and event.button ==1 :
            is_dragging = False
        
        #Mouse motion while draggign
        if event.type == pygame.MOUSEMOTION and is_dragging :
            mouse_x,mouse_y = pygame.mouse.get_pos()
            body.position[0] = mouse_x + drag_offset[0]
            body.position[1] = mouse_y + drag_offset[1]


            #Inertia after release
            dx,dy = event.rel
            THROW_STRENGTH = 50
            body.velocity[0] = dx*THROW_STRENGTH
            body.velocity[1] = dy*THROW_STRENGTH
        
        #If the mouse is not holding on to the ball 
        if not is_dragging:
            #KeyBoard Control
            keys=pygame.key.get_pressed()
            BAT_FORCE = 1200
            
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                body.velocity[1] -= BAT_FORCE *dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                body.velocity[1] += BAT_FORCE *dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                body.velocity[0] -= BAT_FORCE *dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                body.velocity[0] += BAT_FORCE *dt


    return True


# ---------------- Driver function ----------------
def main():
    pygame.init()

    screen, clock = create_window()

    # Body creation
    body = Body(
        position=[C.WIDTH // 2, C.HEIGHT // 2],
        velocity=[0.0, 0.0],   # pixels per second
        mass=10,
        radius=15,
        color=C.WHITE
    )

    running = True  # loop control flag

    while running:
        # Delta time (seconds)
        dt = clock.tick(C.FPS) / 1000.0

        #Loop control variable
        running = handle_events(body,dt)

        # Update physics
        body.update(dt)
        body.handle_boundary_collision(C.WIDTH, C.HEIGHT)


        #Motion Damping
        body.velocity[0] *= 1
        body.velocity[1] *= 1


        # Render
        clear_screen(screen, C.BACKGROUND_COLOR)
        draw_body(screen, body)
        pygame.display.flip()

    pygame.quit()


# ---------------- Entry point ----------------
if __name__ == "__main__":
    main()
