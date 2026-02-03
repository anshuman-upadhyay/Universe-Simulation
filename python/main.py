# ============================================================
# Core Imports
# ============================================================
import pygame

# ============================================================
# Project Imports
# ============================================================

from renderer.window import create_window
from screens.home import home_screen
from screens.simulation import simulation_screen



# ============================================================
# Game Simulation State
# ============================================================
def app() :
    pygame.init()
    screen,clock = create_window()

    state= "HOME"
    while state != "EXIT" :
        if state == "HOME" :
            state = home_screen(screen,clock)
        elif state == "SIMULATION" :
            state = simulation_screen(screen,clock)
        
    pygame.quit()

# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    app()









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
