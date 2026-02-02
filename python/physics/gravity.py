# ============================================================
# Gravity Calculation
# ============================================================
# Applies Newtonian gravity between two bodies.
# ============================================================

import math


# ------------------------------------------------------------
# Apply mutual gravitational force between two bodies
# ------------------------------------------------------------
def apply_gravity(body_a, body_b, G, dt):
    # --------------------------------------------------------
    # Relative position vector
    # --------------------------------------------------------
    dx = body_b.position[0] - body_a.position[0]
    dy = body_b.position[1] - body_a.position[1]

    # Squared distance between bodies
    dist_sq = dx ** 2 + dy ** 2

    # --------------------------------------------------------
    # Avoid singularity (same position)
    # --------------------------------------------------------
    if dist_sq == 0:
        return

    distance = math.sqrt(dist_sq)

    # --------------------------------------------------------
    # Softening to prevent extreme forces at close range
    # --------------------------------------------------------
    softening = min(body_a.radius, body_b.radius) * 0.1
    dist_sq += softening ** 2

    # --------------------------------------------------------
    # Newtonian gravitational force
    # --------------------------------------------------------
    force = (G * body_a.mass * body_b.mass) / dist_sq

    # Unit direction vector
    nx = dx / distance
    ny = dy / distance

    # --------------------------------------------------------
    # Acceleration computation (F = m * a)
    # --------------------------------------------------------
    ax = force * nx / body_a.mass
    ay = force * ny / body_a.mass

    bx = -force * nx / body_b.mass
    by = -force * ny / body_b.mass

    # --------------------------------------------------------
    # Velocity update using delta time
    # --------------------------------------------------------
    body_a.velocity[0] += ax * dt
    body_a.velocity[1] += ay * dt

    body_b.velocity[0] += bx * dt
    body_b.velocity[1] += by * dt





# ======================================================================
#                           TEACHING SECTION
# ======================================================================
#
# File: gravity.py
#
# Role of this file:
# ------------------
# This file implements Newtonian gravity between two bodies.
# It is responsible for calculating gravitational force and
# converting that force into velocity changes over time.
#
# This function is called for every unique pair of bodies in
# the simulation loop.
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTION: apply_gravity
# =========================
#
# apply_gravity(body_a, body_b, G, dt)
#
# ----------------------------------------------------------------------
# Inputs:
#   - body_a : Body
#   - body_b : Body
#   - G      : float (gravitational constant)
#   - dt     : float (delta time in seconds)
#
# Purpose:
#   - Computes gravitational attraction between two bodies
#   - Applies equal and opposite acceleration
#   - Updates velocities in a frame-rate independent manner
#
# ----------------------------------------------------------------------
#
# =========================
# STEP-BY-STEP EXPLANATION
# =========================
#
# 1. Relative Position Vector
#    - Compute vector from body A to body B
#
# Whiteboard:
#   dx = xB − xA
#   dy = yB − yA
#
# ----------------------------------------------------------------------
#
# 2. Distance Calculation
#    - Uses squared distance for efficiency
#    - Prevents division by zero
#
# Whiteboard:
#   r² = dx² + dy²
#
# ----------------------------------------------------------------------
#
# 3. Softening Term
#    - Adds a small value to r²
#    - Prevents force explosion at very small distances
#    - Improves numerical stability
#
# Whiteboard:
#   r² = r² + ε²
#
# ----------------------------------------------------------------------
#
# 4. Newtonian Gravity Formula
#
#   F = G * m₁ * m₂ / r²
#
# Notes:
#   - G is scaled for visual stability
#   - Units are simulation-based, not real-world
#
# ----------------------------------------------------------------------
#
# 5. Direction Normalization
#    - Converts displacement into a unit vector
#
# Whiteboard:
#   n = (dx, dy) / |dx, dy|
#
# ----------------------------------------------------------------------
#
# 6. Acceleration Calculation
#
# From:
#   F = m * a
#
# We get:
#   a = F / m
#
# Accelerations:
#   aA = +F / mA
#   aB = −F / mB
#
# This ensures Newton’s Third Law:
#   "For every action, there is an equal and opposite reaction"
#
# ----------------------------------------------------------------------
#
# 7. Velocity Integration
#    - Applies acceleration over time
#
# Whiteboard:
#   v = v + a * dt
#
# ----------------------------------------------------------------------
#
# =========================
# WHY PAIRWISE GRAVITY
# =========================
#
# - Simple and intuitive
# - Easy to debug and visualize
# - Accurate for small body counts
# - Ideal foundation for future optimization
#
# ======================================================================
#                       IMPROVEMENT SECTION
# ======================================================================
#
# 1. Spatial Optimization
#    - Replace O(n²) gravity with Barnes–Hut or grid partitioning.
#
# 2. Adaptive Softening
#    - Adjust softening dynamically based on mass or velocity.
#
# 3. Energy Tracking
#    - Monitor kinetic + potential energy for stability checks.
#
# 4. Fixed Timestep Physics
#    - Improve determinism and reproducibility.
#
# 5. C++ Acceleration
#    - Move gravity calculations to a native backend for performance.
#
# ======================================================================
