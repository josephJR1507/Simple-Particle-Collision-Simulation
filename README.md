# Simple Particle Collision Simulation

A pair of small Python/Pygame demos that simulate bouncing, colliding particles.

## Contents

### `SPH.py` — 2D Particle Collision Simulator
- Spawns 50 circular particles with random sizes, positions, and velocities in a 1000x1000 window.
- Particles bounce off the walls of the space.
- Detects collisions between particles using distance checks and resolves them with a simple elastic collision (velocity swap) plus overlap correction so particles don't get stuck inside each other.

### `# Simple pygame program.py` — 3D Rotating Cube of Particles
- Renders 500 particles inside a wireframe cube, projected from 3D to 2D with simple perspective projection.
- Drag the mouse to rotate the cube; gravity dynamically points toward the current "down" direction based on the cube's rotation.
- Particles fall under this rotating gravity and bounce (with damping) off the cube's walls.

## Requirements
- Python 3
- [Pygame](https://www.pygame.org/) (`pip install pygame`)

## Running

```bash
python SPH.py
```

or

```bash
python "# Simple pygame program.py"
```
