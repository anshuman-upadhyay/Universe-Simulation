# GRAVITY SIMULATOR — COMPLETE INTERNAL TECHNICAL DOCUMENTATION

This document explains the Gravity Simulator project **from first principles to execution**, covering:
- Why the project exists
- How the architecture is designed
- How files communicate
- What every class, function, and variable does
- Where each piece of state originates
- How data flows through the system
- How user input affects physics
- How physics affects rendering
- How navigation works across screens

If you read this document fully, you should be able to:
- Explain the project end-to-end
- Modify any part confidently
- Teach the codebase to someone else
- Defend design decisions in an interview
- Resume development months later without confusion

There are **no assumed details**. Everything is explicitly documented.

---

## 1. PROJECT PHILOSOPHY & GOALS

The Gravity Simulator is designed as a **mini physics engine**, not just a demo.

Primary goals:
- Simulate Newtonian gravity between bodies
- Allow real-time interaction with physics objects
- Maintain numerical stability
- Keep code modular and readable
- Avoid monolithic “god files”
- Support future migration of physics to C++

Secondary goals:
- Teach engine architecture
- Be interview-presentable
- Be easy to debug and extend

---

## 2. HIGH-LEVEL ARCHITECTURE OVERVIEW

The project is divided into **layers**, each with strict responsibility boundaries.

### Layer 1: Application Layer
- Controls application lifecycle
- Switches between screens
- Knows nothing about physics

### Layer 2: Screen Layer
- Manages UI screens (Home, Simulation)
- Handles navigation (Start, End, Exit)
- Does NOT run physics

### Layer 3: Core Engine Layer
- Runs the simulation loop
- Applies physics
- Integrates motion
- Coordinates rendering
- Reads input state

### Layer 4: Subsystems
- Physics (gravity, collision)
- Rendering
- Input handling
- Constants/configuration

Each layer depends only **downward**, never upward.

---

## 3. COMPLETE FILE STRUCTURE & PURPOSE

```
gravity-simulator/
├── LICENSE
├── README.md                ← public-facing summary
├── cpp/                     ← future physics backend (planned)
└── python/
    ├── main.py              ← application entry & screen router
    ├── core/
    │   ├── input.py         ← input handling + simulation state
    │   └── simulation_loop.py ← physics + rendering loop
    ├── screens/
    │   ├── home.py          ← home/start screen
    │   └── simulation.py    ← simulation UI wrapper
    ├── physics/
    │   ├── body.py          ← body definition
    │   ├── gravity.py       ← gravity force logic
    │   └── collision.py     ← collision resolution
    ├── renderer/
    │   ├── window.py        ← window creation
    │   └── draw.py          ← drawing utilities
    ├── simulation/
    │   └── preset1.py       ← predefined systems
    └── utils/
        ├── constants.py     ← global constants & materials
        └── time.py
```

---

## 4. main.py — APPLICATION ENTRY POINT

### Role of main.py

`main.py` is **NOT** the simulation.
It is **NOT** physics.
It is **NOT** input handling.

It is the **application controller**.

Its responsibilities:
- Initialize pygame
- Create the window
- Decide which screen is currently active
- Transition between screens
- Shut down cleanly

### Why main.py must stay small

If main.py knows physics details, the project becomes:
- Hard to refactor
- Hard to test
- Hard to migrate to C++

By keeping main.py thin, we gain flexibility.

---

### Function: `app()`

**Defined in:** `main.py`

**Purpose:**
Runs the application loop and manages screen transitions.

**Inputs:**
- None (entry function)

**Returns:**
- None

**Execution flow:**
1. Initialize pygame
2. Create window and clock
3. Set initial state to `"HOME"`
4. Loop until state becomes `"EXIT"`
5. Delegate control to the current screen
6. Quit pygame

**Important note:**
`app()` does not know what happens inside screens — it only trusts their return values.

---

## 5. screens/home.py — HOME / START SCREEN

### Role of home.py

This file defines the **first screen the user sees**.

Responsibilities:
- Display project title
- Display START button
- Display EXIT button
- Capture mouse input for navigation
- Decide the next application state

It does **not**:
- Create bodies
- Run physics
- Handle simulation state

---

### Function: `home_screen(screen, clock)`

**Defined in:** `screens/home.py`

**Inputs:**
- `screen` (pygame.Surface): rendering target
- `clock` (pygame.time.Clock): frame timing

**Returns:**
- `"SIMULATION"` → start simulation
- `"EXIT"` → quit application

**Internal logic:**
- Draws title text
- Draws rectangular buttons using pygame.Rect
- Renders text surfaces for button labels
- Detects mouse clicks
- Checks collision between mouse position and button rectangles
- Returns state string based on user action

**Why this function returns strings:**
This keeps navigation decoupled from implementation.
`main.py` doesn’t care *how* the decision was made — only *what* the decision is.

---

## 6. screens/simulation.py — SIMULATION SCREEN WRAPPER

### Role of simulation.py

This file **wraps the simulation loop with UI controls**.

Responsibilities:
- Call the core simulation engine
- Draw the END button
- Detect when the user wants to leave simulation
- Decide whether to return to HOME or EXIT

It does **not**:
- Apply gravity
- Handle collisions
- Update body positions

---

### Function: `simulation_screen(screen, clock)`

**Defined in:** `screens/simulation.py`

**Inputs:**
- `screen`
- `clock`

**Returns:**
- `"HOME"` → go back to home screen
- `"EXIT"` → quit app

**Execution logic:**
- Calls `run_simulation()` from `core/simulation_loop.py`
- Draws END button overlay
- Handles mouse clicks on END
- Returns appropriate state

**Key design decision:**
The simulation engine does not know about UI navigation.
The screen wrapper owns that responsibility.

---

## 7. core/input.py — INPUT HANDLING & SIMULATION STATE

### Role of input.py

This file is the **single source of truth for user input and simulation state**.

All mutable simulation state lives here.

This includes:
- Pause status
- Gravity toggle
- Active body
- Dragging state
- Input strength parameters

---

### Module-level State Variables

These variables persist across frames.

#### `paused`
- Type: bool
- Purpose: Freezes physics updates when True
- Modified by: SPACE key in `handle_events`
- Read by: `core/simulation_loop.py`

#### `gravity_enabled`
- Type: bool
- Purpose: Enables/disables gravity force
- Modified by: G key
- Read by: simulation loop

#### `active_body`
- Type: Body or None
- Purpose: Tracks the currently selected body
- Modified by: mouse click / drag
- Used by:
  - keyboard force application
  - rendering highlight

#### `is_dragging`
- Type: bool
- Purpose: Tracks whether a body is being dragged
- Controls:
  - whether mouse motion applies velocity
  - whether keyboard forces apply

#### `drag_offset`
- Type: list[float, float]
- Purpose: Maintains relative grab position during dragging

#### `body_counter`
- Type: int
- Purpose: Assigns unique IDs to bodies

#### `THROW_STRENGTH`
- Type: float
- Purpose: Scales mouse release velocity

#### `BAT_FORCE`
- Type: float
- Purpose: Scales keyboard force input

#### `DAMPING_COEFF`
- Type: float
- Purpose: Reduces velocity each frame to simulate energy loss

---

### Function: `handle_events(bodies, dt)`

**Defined in:** `core/input.py`

**Inputs:**
- `bodies`: list of Body objects
- `dt`: delta time in seconds

**Returns:**
- True → continue simulation
- False → quit simulation

**What this function does (step by step):**
1. Reads pygame events
2. Handles quit event
3. Spawns new bodies (N key)
4. Toggles pause (SPACE)
5. Toggles gravity (G)
6. Spawns preset systems (Z)
7. Handles mouse grabbing and dragging
8. Applies keyboard forces to active body
9. Updates input state variables

**Why input state lives here:**
Keeping input and state together prevents circular dependencies and simplifies future refactors.

---

## 8. core/simulation_loop.py — CORE ENGINE LOOP

### Role of simulation_loop.py

This file is the **engine heart**.

It:
- Runs every simulation frame
- Applies physics
- Integrates motion
- Handles collisions
- Coordinates rendering
- Reads input state

It does **not**:
- Create windows
- Handle UI navigation
- Quit the application

---

### Function: `run_simulation(screen, clock)`

**Defined in:** `core/simulation_loop.py`

**Inputs:**
- `screen`
- `clock`

**Returns:**
- `"EXIT"` when simulation ends

**Frame execution order:**
1. Compute delta time
2. Call `handle_events`
3. Check paused state
4. Apply gravity if enabled
5. Integrate motion
6. Resolve collisions
7. Handle boundary collisions
8. Apply damping
9. Render all bodies
10. Render state indicators
11. Flip display buffer

**Why input state is imported as a module:**
To ensure live access to mutable state, not stale copies.

---

## 9. physics/body.py — BODY DEFINITION

### Role of Body class

Represents a physical object in the simulation.

---

### Class: `Body`

**Attributes:**
- `position`: [x, y]
- `velocity`: [vx, vy]
- `mass`: float
- `radius`: int
- `color`: (R, G, B)
- `id`: int

---

### Method: `update(dt)`
Integrates velocity into position using:
```
position += velocity * dt
```

---

### Method: `handle_boundary_collision(width, height, restitution)`
Detects collision with screen edges and reflects velocity.

---

## 10. physics/gravity.py — GRAVITY SYSTEM

### Function: `apply_gravity(body_a, body_b, G, dt)`

**Purpose:**
Applies Newtonian gravitational force between two bodies.

**Formula used:**
```
F = G * (m1 * m2) / r²
```

**Important details:**
- Softening applied to prevent instability
- Force applied symmetrically
- Acceleration derived from force and mass

---

## 11. physics/collision.py — COLLISION SYSTEM

### Function: `resolve_body_collision(body_a, body_b, restitution)`

**Purpose:**
Resolves elastic collision between two circular bodies.

**Steps:**
1. Detect overlap
2. Compute collision normal
3. Correct positions based on mass
4. Compute relative velocity
5. Apply impulse response

---

## 12. renderer/window.py — WINDOW CREATION

### Function: `create_window()`

Creates:
- pygame display surface
- pygame clock

Returns both for reuse across screens.

---

## 13. renderer/draw.py — RENDERING UTILITIES

### Functions:
- `clear_screen`
- `draw_body`
- `draw_active_shadow`

These functions **only draw** — they never modify simulation state.

---

## 14. utils/constants.py — GLOBAL CONFIGURATION

Contains:
- Screen dimensions
- FPS
- Color definitions
- Gravitational constant
- Material definitions

Materials define:
- Density
- Radius range
- Color

Used when spawning bodies.

---

## 15. DATA FLOW SUMMARY

1. User inputs → `core/input.py`
2. Input modifies state
3. Simulation loop reads state
4. Physics updates bodies
5. Renderer draws bodies
6. Screen wrapper handles navigation
7. Main app switches screens

---

## FINAL NOTE

This project is intentionally designed as a **learning-first engine**.

It is not optimized prematurely.
It is optimized for clarity, correctness, and extensibility.

If you understand this document, you understand the entire project.

---

END OF INTERNAL DOCUMENTATION
