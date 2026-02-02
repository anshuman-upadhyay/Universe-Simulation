# ============================================================
# Rendering Utilities
# ============================================================
# Contains helper functions responsible for drawing visual
# elements onto the screen.
# ============================================================

import pygame
import utils.constants as C


# ------------------------------------------------------------
# Clear the screen with a solid color
# ------------------------------------------------------------
def clear_screen(screen, color):
    screen.fill(color)


# ------------------------------------------------------------
# Render text on the screen
# ------------------------------------------------------------
def draw_text(screen, text, pos, font, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


# ------------------------------------------------------------
# Draw a physics body (currently rendered as a circle)
# ------------------------------------------------------------
def draw_body(screen, body, font):
    pygame.draw.circle(
        screen,
        body.color,
        (int(body.position[0]), int(body.position[1])),
        body.radius
    )

    # Draw body ID at the center
    text_surface = font.render(str(body.id), True, (0, 0, 0))
    text_rect = text_surface.get_rect(
        center=(
            int(body.position[0]),
            int(body.position[1])
        )
    )
    screen.blit(text_surface, text_rect)


# ------------------------------------------------------------
# Draw visual highlight for the active body
# ------------------------------------------------------------
def draw_active_shadow(screen, body):
    SHADOW_COLOR = C.LIGHT_GRAY
    SHADOW_RADIUS = body.radius + 4

    pygame.draw.circle(
        screen,
        SHADOW_COLOR,
        (int(body.position[0]), int(body.position[1])),
        SHADOW_RADIUS
    )





# ======================================================================
#                           TEACHING SECTION
# ======================================================================
#
# File: draw.py
#
# Role of this file:
# ------------------
# This file contains rendering helper functions responsible for drawing
# all visual elements of the simulation. It does not perform any physics
# or state updates; it only reflects the current simulation state on
# screen.
#
# This separation ensures a clean distinction between simulation logic
# and visual presentation.
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTION: clear_screen
# =========================
#
# clear_screen(screen, color)
#
# ----------------------------------------------------------------------
# Inputs:
#   - screen : pygame.Surface
#   - color  : tuple[int, int, int]
#
# Purpose:
#   - Clears the screen each frame
#   - Prevents artifacts from previous frames
#   - Prepares the canvas for fresh rendering
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTION: draw_text
# =========================
#
# draw_text(screen, text, pos, font, color)
#
# ----------------------------------------------------------------------
# Inputs:
#   - screen : pygame.Surface
#   - text   : str
#   - pos    : tuple[int, int]
#   - font   : pygame.font.Font
#   - color  : tuple[int, int, int]
#
# Purpose:
#   - Renders text onto the screen
#   - Used for UI elements and labels
#   - Abstracts text rendering logic
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTION: draw_body
# =========================
#
# draw_body(screen, body, font)
#
# ----------------------------------------------------------------------
# Inputs:
#   - screen : pygame.Surface
#   - body   : Body
#   - font   : pygame.font.Font
#
# Purpose:
#   - Draws a physical body as a circle
#   - Visualizes body position and size
#   - Displays the body ID for identification
#
# Rendering details:
#   - Circle center → body.position
#   - Circle radius → body.radius
#   - Color         → body.color
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTION: draw_active_shadow
# =========================
#
# draw_active_shadow(screen, body)
#
# ----------------------------------------------------------------------
# Inputs:
#   - screen : pygame.Surface
#   - body   : Body
#
# Purpose:
#   - Highlights the currently active body
#   - Improves user interaction clarity
#   - Makes control focus visually obvious
#
# Visual behavior:
#   - Draws a slightly larger circle
#   - Uses a neutral highlight color
#
# ---------------------------------------------------------
