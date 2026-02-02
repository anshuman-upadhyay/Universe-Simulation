# ============================================================
# Window Creation
# ============================================================
# Responsible for initializing the application window and
# returning core rendering objects.
# ============================================================

import pygame
import utils.constants as c


# ------------------------------------------------------------
# Create and configure the main application window
# ------------------------------------------------------------
def create_window():
    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    pygame.display.set_caption(c.TITLE)
    clock = pygame.time.Clock()

    return screen, clock





# ======================================================================
#                           TEACHING SECTION
# ======================================================================
#
# File: window.py
#
# Role of this file:
# ------------------
# This file is responsible for initializing the main application window
# and providing essential rendering utilities required by the simulation.
#
# It abstracts window setup logic so that the main loop remains clean and
# focused on simulation control rather than system initialization.
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTION: create_window
# =========================
#
# create_window()
#
# ----------------------------------------------------------------------
# Inputs:
#   - None
#
# Returns:
#   - screen : pygame.Surface
#   - clock  : pygame.time.Clock
#
# Purpose:
#   - Creates the main rendering surface
#   - Sets the application window title
#   - Provides a clock object for frame timing
#
# ----------------------------------------------------------------------
#
# =========================
# DETAILED EXPLANATION
# =========================
#
# 1. pygame.display.set_mode(...)
#    - Initializes the window with given width and height
#    - Returns a Surface object used for all rendering
#
# 2. pygame.display.set_caption(...)
#    - Sets the title text displayed in the window frame
#    - Useful for identification and debugging
#
# 3. pygame.time.Clock()
#    - Creates a clock object
#    - Used to regulate frame rate
#    - Provides delta time calculation
#
# ----------------------------------------------------------------------
#
# =========================
# WHY THIS FILE EXISTS
# =========================
#
# - Keeps window setup logic separate from simulation logic
# - Improves readability of main loop
# - Makes window configuration reusable
# - Simplifies future platform or backend changes
#
# ======================================================================
#                       IMPROVEMENT SECTION
# ======================================================================
#
# 1. Fullscreen / Resizable Support
#    - Add configuration options for fullscreen or resizable windows.
#
# 2. Multi-Monitor Handling
#    - Allow selecting which display to use.
#
# 3. Window Icon Support
#    - Set a custom application icon.
#
# 4. Configuration-Based Setup
#    - Load window parameters from an external config file.
#
# 5. Headless Mode
#    - Support non-graphical simulation runs for testing.
#
# ======================================================================

