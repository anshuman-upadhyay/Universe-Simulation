# ============================================================
# Collision Resolution
# ============================================================
# Handles elastic collisions between two circular bodies.
# ============================================================

import math


# ------------------------------------------------------------
# Elastic collision resolution between two bodies
# ------------------------------------------------------------
def resolve_body_collision(body_a, body_b, restitution=0.6):
    # Clamp restitution to a valid range [0, 1]
    restitution = max(0.0, min(restitution, 1.0))

    # --------------------------------------------------------
    # Relative position
    # --------------------------------------------------------
    dx = body_b.position[0] - body_a.position[0]
    dy = body_b.position[1] - body_a.position[1]
    distance = math.hypot(dx, dy)

    # --------------------------------------------------------
    # Avoid division by zero (perfect overlap case)
    # --------------------------------------------------------
    if distance == 0:
        dx = 1e-6
        dy = 0
        distance = 1e-6

    # --------------------------------------------------------
    # Overlap check
    # --------------------------------------------------------
    overlap = body_a.radius + body_b.radius - distance
    if overlap <= 0:
        return

    # --------------------------------------------------------
    # Collision normal (unit vector)
    # --------------------------------------------------------
    nx = dx / distance
    ny = dy / distance

    # --------------------------------------------------------
    # Positional correction (mass-weighted)
    # --------------------------------------------------------
    total_mass = body_a.mass + body_b.mass

    body_a.position[0] -= nx * overlap * (body_b.mass / total_mass)
    body_a.position[1] -= ny * overlap * (body_b.mass / total_mass)

    body_b.position[0] += nx * overlap * (body_a.mass / total_mass)
    body_b.position[1] += ny * overlap * (body_a.mass / total_mass)

    # --------------------------------------------------------
    # Relative velocity
    # --------------------------------------------------------
    rvx = body_b.velocity[0] - body_a.velocity[0]
    rvy = body_b.velocity[1] - body_a.velocity[1]

    # Velocity component along collision normal
    vel_along_normal = rvx * nx + rvy * ny

    # If bodies are separating, do nothing
    if vel_along_normal > 0:
        return

    # --------------------------------------------------------
    # Impulse calculation
    # --------------------------------------------------------
    impulse = -(1 + restitution) * vel_along_normal
    impulse /= (1 / body_a.mass + 1 / body_b.mass)

    ix = impulse * nx
    iy = impulse * ny

    # --------------------------------------------------------
    # Apply impulse
    # --------------------------------------------------------
    body_a.velocity[0] -= ix / body_a.mass
    body_a.velocity[1] -= iy / body_a.mass

    body_b.velocity[0] += ix / body_b.mass
    body_b.velocity[1] += iy / body_b.mass





# ======================================================================
#                           TEACHING SECTION
# ======================================================================
#
# File: collision.py
#
# Role of this file:
# ------------------
# This file implements elastic collision resolution between two circular
# bodies. It is responsible for:
#   - Preventing bodies from overlapping
#   - Computing realistic post-collision velocities
#   - Conserving momentum (with optional energy loss)
#
# The logic here is physics-focused and independent of rendering or input.
#
# ----------------------------------------------------------------------
#
# =========================
# FUNCTION: resolve_body_collision
# =========================
#
# resolve_body_collision(body_a, body_b, restitution=0.6)
#
# ----------------------------------------------------------------------
# Inputs:
#   - body_a      : Body
#   - body_b      : Body
#   - restitution : float (0.0 → inelastic, 1.0 → elastic)
#
# Purpose:
#   - Detects collision between two circular bodies
#   - Separates overlapping bodies
#   - Applies impulse-based velocity correction
#
# ----------------------------------------------------------------------
#
# =========================
# STEP-BY-STEP EXPLANATION
# =========================
#
# 1. Relative Position Calculation
#    - Compute vector from body A to body B
#    - Distance determines whether bodies overlap
#
# 2. Overlap Detection
#    - overlap = rA + rB − distance
#    - If overlap ≤ 0 → no collision
#
# 3. Collision Normal
#    - Normalized direction of collision
#    - Used to project velocities and impulses
#
# Whiteboard view:
#    n = (dx, dy) / |dx, dy|
#
# ----------------------------------------------------------------------
#
# 4. Positional Correction
#    - Bodies are moved apart along the normal
#    - Correction is mass-weighted
#
# Why mass-weighted?
#   - Heavier bodies move less
#   - Lighter bodies move more
#   - Prevents jitter and tunneling
#
# ----------------------------------------------------------------------
#
# 5. Relative Velocity
#    - Computes velocity of B relative to A
#
# Whiteboard:
#   v_rel = vB − vA
#
# ----------------------------------------------------------------------
#
# 6. Velocity Along Normal
#    - Projects relative velocity onto collision normal
#
# Whiteboard:
#   v_n = v_rel · n
#
# If v_n > 0:
#   - Bodies are already separating
#   - No impulse needed
#
# ----------------------------------------------------------------------
#
# 7. Impulse Calculation
#
# Formula:
#   j = −(1 + e) * v_n / (1/mA + 1/mB)
#
# Where:
#   e  = restitution
#   j  = impulse magnitude
#
# This ensures:
#   - Momentum conservation
#   - Energy loss based on restitution
#
# ----------------------------------------------------------------------
#
# 8. Applying Impulse
#    - Impulse is applied in opposite directions
#    - Velocity change depends on mass
#
# Whiteboard:
#   vA -= (j * n) / mA
#   vB += (j * n) / mB
#
# ----------------------------------------------------------------------
#
# =========================
# WHY IMPULSE-BASED METHOD
# =========================
#
# - Stable for real-time simulations
# - Easy to tune using restitution
# - Commonly used in physics engines
# - Scales well when ported to C++
#
# ======================================================================
#                       IMPROVEMENT SECTION
# ======================================================================
#
# 1. Friction Support
#    - Add tangential impulse for surface friction.
#
# 2. Continuous Collision Detection
#    - Prevent tunneling at high velocities.
#
# 3. Angular Momentum
#    - Add rotational impulse and torque.
#
# 4. Collision Layers
#    - Allow selective collision handling.
#
# 5. C++ Optimization
#    - Move collision math to a high-performance backend.
#
# ======================================================================
