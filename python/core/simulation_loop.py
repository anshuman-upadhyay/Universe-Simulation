# ============================================================
# Core Simulation Loop
# ============================================================

import pygame
import utils.constants as C
from renderer.draw import clear_screen,draw_body,draw_active_shadow
from physics.gravity import apply_gravity
from physics.collision import resolve_body_collision
from physics.body import Body
import core.input as input_state
# ------------------------------------------------------------
# Run the physics + rendering loop
# ------------------------------------------------------------

def run_simulation(screen,clock) :
    bodies = []
    running = True


    while running:
        # Delta time (seconds)
        dt = clock.tick(C.FPS) / 1000.0
        # Handle input & events
        running = input_state.handle_events(bodies, dt)

        # ----------------------------------------------------
        # Physics Update (Skipped When Paused)
        # ----------------------------------------------------
        if not input_state.paused:

            # Mutual gravity (pairwise)
            if input_state.gravity_enabled:
                for i in range(len(bodies)):
                    for j in range(i + 1, len(bodies)):
                        apply_gravity(bodies[i], bodies[j], C.G, dt)

            # Integrate motion
            for body in bodies:
                body.update(dt)

            # Body-body collisions
            for i in range(len(bodies)):
                for j in range(i + 1, len(bodies)):
                    resolve_body_collision(bodies[i], bodies[j])

            # Boundary collisions + damping
            for body in bodies:
                body.handle_boundary_collision(C.WIDTH, C.HEIGHT)
                body.velocity[0] *=  input_state.DAMPING_COEFF
                body.velocity[1] *=  input_state.DAMPING_COEFF

        # ----------------------------------------------------
        # Rendering
        # ----------------------------------------------------
        clear_screen(screen, C.BACKGROUND_COLOR)

        font = pygame.font.SysFont(None, 18)

        for body in bodies:
            if body == input_state.active_body:
                draw_active_shadow(screen, body)
            draw_body(screen, body, font)

        # ----------------------------------------------------
        # UI State Indicators
        # ----------------------------------------------------
        if input_state.paused:
            paused_text = font.render("PAUSED", True, (255, 80, 80))
            screen.blit(paused_text, (10, 10))

        if not input_state.gravity_enabled:
            grav_text = font.render("GRAVITY OFF", True, (80, 180, 255))
            screen.blit(grav_text, (10, 30))

        pygame.display.flip()
    #Tell caller that simulation ended
    return "EXIT"

