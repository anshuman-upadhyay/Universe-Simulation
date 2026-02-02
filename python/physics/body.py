# ============================================================
# Body Class
# ============================================================
# Represents a single physical entity in the simulation.
# Each body has position, velocity, mass, radius, and color.
# ============================================================


class Body:
    def __init__(self, position, velocity, mass, radius, color, body_id):
        # ----------------------------------------------------
        # Core Physical Properties
        # ----------------------------------------------------
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.radius = radius

        # ----------------------------------------------------
        # Visual & Identity Properties
        # ----------------------------------------------------
        self.color = color
        self.id = body_id

    # --------------------------------------------------------
    # Position Update (Motion Integration)
    # --------------------------------------------------------
    def update(self, dt):
        # Update position using velocity and delta time
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    # --------------------------------------------------------
    # Boundary Collision Handling
    # --------------------------------------------------------
    def handle_boundary_collision(self, width, height, restitution=0.9):
        # Left wall
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] *= -restitution

        # Right wall
        if self.position[0] + self.radius > width:
            self.position[0] = width - self.radius
            self.velocity[0] *= -restitution

        # Top wall
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] *= -restitution

        # Bottom wall
        if self.position[1] + self.radius > height:
            self.position[1] = height - self.radius
            self.velocity[1] *= -restitution





# ======================================================================
#                           TEACHING SECTION
# ======================================================================
#
# File: body.py
#
# Role of this file:
# ------------------
# This file defines the Body class, which is the fundamental unit of the
# physics simulation. Every object that participates in gravity,
# collision, and rendering is represented as a Body instance.
#
# The Body class itself is intentionally lightweight:
#   - It stores physical state
#   - It updates its own position
#   - It handles boundary collisions
#
# Higher-level interactions (gravity, body-body collisions, rendering)
# are handled externally to keep responsibilities clean.
#
# ----------------------------------------------------------------------
#
# =========================
# CLASS: Body
# =========================
#
# Represents a circular rigid body in a 2D simulation space.
#
# ----------------------------------------------------------------------
#
# __init__(self, position, velocity, mass, radius, color, body_id)
# ----------------------------------------------------------------
# Inputs:
#   - position : list[float, float]
#   - velocity : list[float, float]
#   - mass     : float
#   - radius   : int / float
#   - color    : tuple[int, int, int]
#   - body_id  : int
# Purpose:
#   - Initializes the physical and visual state of the body
#   - Stores identity for tracking and debugging
#   - Acts as a data container for simulation systems
#
# ----------------------------------------------------------------------
#
# update(self, dt)
# ----------------
# Inputs:
#   - dt : float (delta time in seconds)
# Purpose:
#   - Updates position using velocity
#   - Implements basic kinematic integration
#   - Keeps motion frame-rate independent
#
# Whiteboard view:
#   x = x + vx * dt
#   y = y + vy * dt
#
# ----------------------------------------------------------------------
#
# handle_boundary_collision(self, width, height, restitution=0.9)
# ----------------------------------------------------------------
# Inputs:
#   - width       : int (simulation boundary width)
#   - height      : int (simulation boundary height)
#   - restitution : float (energy retention factor)
# Purpose:
#   - Detects collision with simulation boundaries
#   - Reflects velocity upon impact
#   - Prevents bodies from leaving the visible area
#
# Restitution meaning:
#   restitution < 1.0  → energy loss (damping)
#   restitution = 1.0  → perfectly elastic bounce
#
# ----------------------------------------------------------------------
#
# =========================
# DATA MODEL SUMMARY
# =========================
#
# Body Attributes:
#   position : [x, y]
#   velocity : [vx, vy]
#   mass     : scalar mass value
#   radius   : collision & rendering size
#   color    : RGB tuple for rendering
#   id       : unique identifier
#
# ----------------------------------------------------------------------
#
# =========================
# WHY THIS CLASS IS SIMPLE
# =========================
#
# - Keeps physics modular
# - Allows gravity, collision, and rendering to evolve independently
# - Makes future C++ porting easier
# - Avoids tight coupling between systems
#
# ======================================================================
#                       IMPROVEMENT SECTION
# ======================================================================
#
# 1. Acceleration Support
#    - Store acceleration as a first-class property for force-based design.
#
# 2. Rotational Physics
#    - Extend body with angular velocity and torque.
#
# 3. Shape Generalization
#    - Support non-circular bodies (polygons).
#
# 4. Immutable State Option
#    - Enable immutable updates for deterministic simulations.
#
# 5. C++ Backend Compatibility
#    - Mirror this class layout for seamless Python ↔ C++ integration.
#
# ======================================================================
