# ============================================================
# Input Handling Module
# ============================================================
# Responsible for all user input and interaction logic.
# ============================================================

import math
import random
import pygame

import utils.constants as C
from physics.body import Body
from simulation.preset1 import spawn_system


# ============================================================
# Input / Interaction State (Module-Level)
# ============================================================

# ============================================================
# Global Simulation State
# ============================================================
gravity_enabled = True
paused = False

# ============================================================
# Mouse / Interaction State
# ============================================================
is_dragging = False
drag_offset = [0.0, 0.0]
active_body = None

# ============================================================
# Body / Physics Parameters
# ============================================================
body_counter = 0
THROW_STRENGTH = 50
BAT_FORCE = 1200
DAMPING_COEFF = 0.98

#============================================================
# Event Handling
# ============================================================
def handle_events(bodies, dt):
    global is_dragging, drag_offset, active_body
    global body_counter, gravity_enabled, paused
    global THROW_STRENGTH, BAT_FORCE, DAMPING_COEFF

    for event in pygame.event.get():

        # ----------------------------------------------------
        # Quit Simulation
        # ----------------------------------------------------
        if event.type == pygame.QUIT:
            return False

        # ----------------------------------------------------
        # Spawn New Body (Key: N)
        # ----------------------------------------------------
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            body_counter += 1

            # Weighted material selection (many small, few large)
            material_name = random.choices(
                population=list(C.MATERIALS.keys()),
                weights=[1000, 500, 100, 50, 1,0.1],
                k=1
            )[0]

            material = C.MATERIALS[material_name]
 
            # Radius & mass derived from material density
            radius = random.randint(8, 50)
            density = material["density"]
            mass = density * math.pi * (radius ** 2)

            new_body = Body(
                position=[mouse_x, mouse_y],
                velocity=[0.0, 0.0],
                mass=mass,
                radius=radius,
                color=material["color"],
                body_id=body_counter
            )

            bodies.append(new_body)

            # Newly spawned body becomes active
            active_body = new_body
            is_dragging = False

        # ----------------------------------------------------
        # Simulation Toggles
        # ----------------------------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                gravity_enabled = not gravity_enabled

            if event.key == pygame.K_SPACE:
                paused = not paused

        # ----------------------------------------------------
        # Spawn Preset Solar System (Key: Z)
        # ----------------------------------------------------
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            spawn_system(bodies, [mouse_x, mouse_y])

        # ----------------------------------------------------
        # Right Click: Teleport Active Body
        # ----------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and active_body:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            active_body.position[0] = mouse_x
            active_body.position[1] = mouse_y

            # Kill velocity after teleport
            active_body.velocity[0] = 0.0
            active_body.velocity[1] = 0.0

            is_dragging = False

        # ----------------------------------------------------
        # Left Click: Grab Body
        # ----------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for body in reversed(bodies):
                dx = mouse_x - body.position[0]
                dy = mouse_y - body.position[1]
                dist_sq = dx * dx + dy * dy

                if dist_sq <= body.radius ** 2:
                    active_body = body
                    is_dragging = True
                    drag_offset[0] = body.position[0] - mouse_x
                    drag_offset[1] = body.position[1] - mouse_y
                    body.velocity = [0, 0]
                    break

        # ----------------------------------------------------
        # Release Body
        # ----------------------------------------------------
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_dragging = False

        # ----------------------------------------------------
        # Dragging Motion
        # ----------------------------------------------------
        if event.type == pygame.MOUSEMOTION and is_dragging and active_body:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            active_body.position[0] = mouse_x + drag_offset[0]
            active_body.position[1] = mouse_y + drag_offset[1]

            dx, dy = event.rel
            active_body.velocity[0] = dx * THROW_STRENGTH
            active_body.velocity[1] = dy * THROW_STRENGTH

        # ----------------------------------------------------
        # Keyboard Force Control (When Not Dragging)
        # ----------------------------------------------------
        if not is_dragging and active_body:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                active_body.velocity[1] -= BAT_FORCE * dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                active_body.velocity[1] += BAT_FORCE * dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                active_body.velocity[0] -= BAT_FORCE * dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                active_body.velocity[0] += BAT_FORCE * dt

    return True

