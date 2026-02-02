# ============================================================
# Core Imports
# ============================================================
import math
import random
import pygame

# ============================================================
# Project Imports
# ============================================================
import utils.constants as C
from renderer.window import create_window
from renderer.draw import clear_screen, draw_body, draw_active_shadow
from physics.body import Body
from physics.collision import resolve_body_collision
from physics.gravity import apply_gravity
from simulation.preset1 import spawn_system


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


# ============================================================
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
                weights=[600, 250, 100, 50, 1,0.1],
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


# ============================================================
# Main Driver Loop
# ============================================================
def main():
    pygame.init()

    screen, clock = create_window()
    bodies = []

    running = True

    while running:
        # Delta time (seconds)
        dt = clock.tick(C.FPS) / 1000.0

        # Handle input & events
        running = handle_events(bodies, dt)

        # ----------------------------------------------------
        # Physics Update (Skipped When Paused)
        # ----------------------------------------------------
        if not paused:

            # Mutual gravity (pairwise)
            if gravity_enabled:
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
                body.velocity[0] *= DAMPING_COEFF
                body.velocity[1] *= DAMPING_COEFF

        # ----------------------------------------------------
        # Rendering
        # ----------------------------------------------------
        clear_screen(screen, C.BACKGROUND_COLOR)

        font = pygame.font.SysFont(None, 18)

        for body in bodies:
            if body == active_body:
                draw_active_shadow(screen, body)
            draw_body(screen, body, font)

        # ----------------------------------------------------
        # UI State Indicators
        # ----------------------------------------------------
        if paused:
            paused_text = font.render("PAUSED", True, (255, 80, 80))
            screen.blit(paused_text, (10, 10))

        if not gravity_enabled:
            grav_text = font.render("GRAVITY OFF", True, (80, 180, 255))
            screen.blit(grav_text, (10, 30))

        pygame.display.flip()

    pygame.quit()


# ============================================================
# Entry Point
# ============================================================
if __name__ == "__main__":
    main()









# ======================================================================
#                           TEACHING SECTION
# ======================================================================
#
# File: main.py
#
# Role of this file:
# ------------------
# This file acts as the central controller of the gravity simulation.
# It coordinates user input, physics updates, collision handling, and
# rendering. No core physics formulas are implemented here directly;
# instead, this file orchestrates multiple subsystems in a clean loop.
#
# The design follows a classic real-time simulation / game-loop pattern:
#
#   1. Handle user input & events
#   2. Update physics (gravity, motion, collisions)
#   3. Render the updated state
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTIONS USED IN FILE
# =========================
#
# Each function listed below is explained in terms of:
#   - Inputs it takes
#   - What it does
#   - Why it is used here
#
# ----------------------------------------------------------------------
#
# pygame.init()
# --------------
# Inputs:
#   - None
# Purpose:
#   - Initializes all required pygame modules
#   - Prepares the system for graphics, input, and timing
#   - Must be called before using any pygame functionality
#
# ----------------------------------------------------------------------
#
# create_window()
# ----------------
# Inputs:
#   - None
# Returns:
#   - screen : pygame.Surface
#   - clock  : pygame.time.Clock
# Purpose:
#   - Creates the main application window
#   - Sets window dimensions and title
#   - Provides a clock object for frame timing (FPS control)
#
# ----------------------------------------------------------------------
#
# handle_events(bodies, dt)
# -------------------------
# Inputs:
#   - bodies : list[Body]
#   - dt     : float (delta time in seconds)
# Returns:
#   - bool (whether the simulation should continue running)
# Purpose:
#   - Processes all user input (keyboard + mouse)
#   - Spawns, selects, drags, and controls bodies
#   - Toggles simulation state (pause, gravity)
#
# ----------------------------------------------------------------------
#
# spawn_system(bodies, position)
# ------------------------------
# Inputs:
#   - bodies   : list[Body]
#   - position : list[int, int]
# Purpose:
#   - Spawns a predefined multi-body system (e.g. solar system)
#   - Used to quickly demonstrate gravitational interactions
#   - Keeps complex setup logic out of main.py
#
# ----------------------------------------------------------------------
#
# apply_gravity(body1, body2, G, dt)
# ---------------------------------
# Inputs:
#   - body1 : Body
#   - body2 : Body
#   - G     : float (gravitational constant)
#   - dt    : float (delta time)
# Purpose:
#   - Applies Newtonian gravity between two bodies
#   - Updates velocities of both bodies symmetrically
#   - Enables realistic orbital and attraction behavior
#
# ----------------------------------------------------------------------
#
# body.update(dt)
# ---------------
# Inputs:
#   - dt : float (delta time)
# Purpose:
#   - Integrates velocity into position
#   - Updates the body's state based on elapsed time
#   - Keeps physics frame-rate independent
#
# ----------------------------------------------------------------------
#
# resolve_body_collision(body1, body2)
# -----------------------------------
# Inputs:
#   - body1 : Body
#   - body2 : Body
# Purpose:
#   - Detects and resolves collisions between two bodies
#   - Prevents overlap and applies collision response
#   - Maintains physical plausibility of interactions
#
# ----------------------------------------------------------------------
#
# body.handle_boundary_collision(width, height)
# ---------------------------------------------
# Inputs:
#   - width  : int (window width)
#   - height : int (window height)
# Purpose:
#   - Detects collisions with simulation boundaries
#   - Reflects velocity if body hits screen edges
#   - Keeps bodies within the visible simulation space
#
# ----------------------------------------------------------------------
#
# clear_screen(screen, color)
# ---------------------------
# Inputs:
#   - screen : pygame.Surface
#   - color  : tuple[int, int, int]
# Purpose:
#   - Clears the screen each frame
#   - Prevents visual trails or ghosting
#   - Prepares canvas for fresh rendering
#
# ----------------------------------------------------------------------
#
# draw_body(screen, body, font)
# -----------------------------
# Inputs:
#   - screen : pygame.Surface
#   - body   : Body
#   - font   : pygame.font.Font
# Purpose:
#   - Draws a body as a circle
#   - Renders body metadata (id, mass, etc.)
#   - Provides visual feedback for simulation state
#
# ----------------------------------------------------------------------
#
# draw_active_shadow(screen, body)
# --------------------------------
# Inputs:
#   - screen : pygame.Surface
#   - body   : Body
# Purpose:
#   - Highlights the currently active body
#   - Improves user interaction clarity
#   - Helps track which object is being controlled
#
# ----------------------------------------------------------------------
#
# pygame.display.flip()
# ----------------------
# Inputs:
#   - None
# Purpose:
#   - Swaps the back buffer to the screen
#   - Makes rendered frame visible
#   - Final step of every render cycle
#
# ----------------------------------------------------------------------
#
# pygame.quit()
# --------------
# Inputs:
#   - None
# Purpose:
#   - Cleans up pygame resources
#   - Ensures graceful shutdown
#   - Prevents resource leakage
#
# ======================================================================
#                       IMPROVEMENT SECTION
# ======================================================================
#
# NOTE:
# -----
# This section intentionally does NOT affect the current implementation.
# It documents future design considerations and architectural evolution.
#
# 1. Physics Engine Separation
#    - Gravity, collision, and integration logic can be consolidated
#      into a dedicated physics engine module.
#
# 2. Spatial Optimization
#    - Pairwise O(n²) gravity and collision checks can be optimized
#      using spatial partitioning (quadtrees / grids).
#
# 3. Input System Abstraction
#    - Mouse and keyboard handling can be separated into an input manager
#      for cleaner scalability.
#
# 4. C++ Physics Backend
#    - Core physics calculations can be ported to C++ for performance
#      while keeping Python as the orchestration layer.
#
# 5. Deterministic Simulation Mode
#    - Introduce fixed timestep updates for reproducibility and testing.
#
# 6. Debug & Visualization Tools
#    - Force vectors, velocity arrows, and collision normals can be
#      visualized for educational and debugging purposes.
#
# ======================================================================
