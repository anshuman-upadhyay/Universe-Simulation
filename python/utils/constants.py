# ============================================================
# Project Constants
# ============================================================
# This file centralizes all global constants used across the
# simulation: screen settings, colors, and physics parameters.
# ============================================================


# ============================================================
# Game / Window Configuration
# ============================================================
WIDTH  = 800
HEIGHT = 800
FPS    = 30
TITLE  = "PROJECT - 0"


# ============================================================
# Color Definitions
# ============================================================

# Basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# Gray scale
LIGHT_GRAY = (200, 200, 200)
GRAY       = (128, 128, 128)
DARK_GRAY  = (50, 50, 50)

# Extended color palette
YELLOW  = (255, 255, 0)
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE  = (255, 165, 0)
PURPLE  = (128, 0, 128)
SILVER  = (192, 192, 192)
BROWN   = (101, 67, 33)


# ============================================================
# UI / Simulation Visual Colors
# ============================================================
BACKGROUND_COLOR = (14, 0, 53)     # Space-like background
GRID_COLOR       = (40, 40, 60)
TEXT_COLOR       = WHITE
ACCENT_COLOR     = CYAN


# ============================================================
# Default Body Color Presets
# ============================================================
BODY_PRIMARY   = BLUE
BODY_SECONDARY = RED
BODY_TERTIARY  = GREEN


# ============================================================
# Physics Constants
# ============================================================

# Gravitational constant (scaled for simulation feel)
G = 300


# ============================================================
# Material Definitions
# ============================================================
# MATERIALS define physical and visual properties used when
# spawning bodies in the simulation.
#
# Each material includes:
#   - density       : affects mass calculation
#   - radius_range  : suggested size range
#   - color         : rendering color
# ============================================================
MATERIALS = {
    "dust": {
        "density": 0.3,
        "radius_range": (1, 4),
        "color": BROWN
    },
    "rock": {
        "density": 1.0,
        "radius_range": (4, 16),
        "color": SILVER
    },
    "planet": {
        "density": 1.2,
        "radius_range": (16, 30),
        "color": BLUE
    },
    "gaint": {
        "density": 3.0,
        "radius_range": (30, 55),
        "color": RED
    },
    "star": {
        "density": 50.0,
        "radius_range": (70, 150),
        "color": YELLOW
    },
}





# ======================================================================
#                           TEACHING SECTION
# ======================================================================
#
# File: constants.py
#
# Role of this file:
# ------------------
# This file acts as a single source of truth for all global constants
# used throughout the project. It prevents magic numbers from being
# scattered across the codebase and makes tuning, scaling, and visual
# consistency easy.
#
# This file contains NO logic — only data.
#
# ----------------------------------------------------------------------
#
# =========================
# CONSTANT GROUPS EXPLAINED
# =========================
#
# WIDTH, HEIGHT
# -------------
# Inputs:
#   - Integers representing screen dimensions
# Purpose:
#   - Define the simulation window size
#   - Used for rendering and boundary collision checks
#   - Centralizes screen scaling decisions
#
# ----------------------------------------------------------------------
#
# FPS
# ---
# Inputs:
#   - Integer frames per second
# Purpose:
#   - Controls simulation update frequency
#   - Used to compute delta time (dt)
#   - Keeps physics behavior consistent
#
# ----------------------------------------------------------------------
#
# TITLE
# -----
# Inputs:
#   - String
# Purpose:
#   - Sets window title
#   - Helps identify the application
#   - Useful for debugging multiple builds
#
# ----------------------------------------------------------------------
#
# COLOR CONSTANTS (WHITE, BLACK, RED, etc.)
# ----------------------------------------
# Inputs:
#   - RGB tuples
# Purpose:
#   - Standardize color usage across the project
#   - Improve readability of rendering code
#   - Prevent repeated hard-coded color values
#
# ----------------------------------------------------------------------
#
# BACKGROUND_COLOR
# ----------------
# Inputs:
#   - RGB tuple
# Purpose:
#   - Defines the simulation background
#   - Chosen to resemble outer space
#   - Enhances visual contrast with bodies
#
# ----------------------------------------------------------------------
#
# BODY_PRIMARY / BODY_SECONDARY / BODY_TERTIARY
# ---------------------------------------------
# Inputs:
#   - RGB tuples
# Purpose:
#   - Provide default visual presets for bodies
#   - Allow quick styling without custom colors
#   - Useful for debugging or categorization
#
# ----------------------------------------------------------------------
#
# G (Gravitational Constant)
# -------------------------
# Inputs:
#   - Float / Integer
# Purpose:
#   - Scales gravitational force strength
#   - Tuned for visual stability, not real-world units
#   - Centralized to allow easy experimentation
#
# ----------------------------------------------------------------------
#
# MATERIALS
# ---------
# Inputs:
#   - Dictionary of material definitions
# Purpose:
#   - Defines physical + visual properties of bodies
#   - Used during body spawning
#   - Enables diversity
