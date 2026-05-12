import pygame
import math
import random

# --- Settings ---
WIDTH, HEIGHT = 800, 600
FPS = 60
PARTICLE_COUNT = 500
CUBE_SIZE = 150  # Half-length of the cube side

class Particle:
    def __init__(self):
        # 3D coordinates inside the cube (-CUBE_SIZE to CUBE_SIZE)
        self.pos = [random.uniform(-CUBE_SIZE, CUBE_SIZE) for _ in range(3)]
        self.vel = [random.uniform(-2, 2) for _ in range(3)]
        self.color = (255, 100, 50)

    def update(self, gravity_vec):
        # Apply "gravity" based on cube rotation
        for i in range(3):
            self.vel[i] += gravity_vec[i] * 0.1
            self.pos[i] += self.vel[i]
            
            # Simple bounce logic inside the 3D box
            if abs(self.pos[i]) > CUBE_SIZE:
                self.vel[i] *= -0.5 # Damping
                self.pos[i] = math.copysign(CUBE_SIZE, self.pos[i])

def rotate_3d(x, y, z, angle_x, angle_y):
    # Rotate around Y axis
    ny = y
    nx = x * math.cos(angle_y) + z * math.sin(angle_y)
    nz = -x * math.sin(angle_y) + z * math.cos(angle_y)
    # Rotate around X axis
    y, z = ny, nz
    ny = y * math.cos(angle_x) - z * math.sin(angle_x)
    nz = y * math.sin(angle_x) + z * math.cos(angle_x)
    return nx, ny, nz

def project(x, y, z):
    # Simple perspective projection
    factor = 400 / (400 + z)
    px = x * factor + WIDTH // 2
    py = y * factor + HEIGHT // 2
    return int(px), int(py)

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
particles = [Particle() for _ in range(PARTICLE_COUNT)]

angle_x = angle_y = 0
dragging = False
last_mouse_pos = (0, 0)

# Cube edges for drawing the wireframe
edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
vertices = [
    [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1],
    [-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1]
]

running = True
while running:
    screen.fill((10, 10, 15))
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN: dragging = True
        if event.type == pygame.MOUSEBUTTONUP: dragging = False

    # Interaction: Rotate cube with mouse
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle_y += (mouse_x - last_mouse_pos[0]) * 0.01
        angle_x -= (mouse_y - last_mouse_pos[1]) * 0.01
    last_mouse_pos = pygame.mouse.get_pos()

    # Calculate Gravity Vector based on rotation
    # This makes particles "fall" toward the current bottom of the cube
    grav = [math.sin(angle_y), math.sin(angle_x), math.cos(angle_x)]

    # Draw Cube Edges
    projected_verts = []
    for v in vertices:
        rx, ry, rz = rotate_3d(v[0]*CUBE_SIZE, v[1]*CUBE_SIZE, v[2]*CUBE_SIZE, angle_x, angle_y)
        projected_verts.append(project(rx, ry, rz))

    for edge in edges:
        pygame.draw.line(screen, (100, 100, 100), projected_verts[edge[0]], projected_verts[edge[1]], 1)

    # Update and Draw Particles
    for p in particles:
        p.update(grav)
        rx, ry, rz = rotate_3d(p.pos[0], p.pos[1], p.pos[2], angle_x, angle_y)
        pos_2d = project(rx, ry, rz)
        
        # Draw particle (size varies by depth for 3D effect)
        size = max(1, int(5 * (400 / (400 + rz))))
        pygame.draw.circle(screen, p.color, pos_2d, size)

    pygame.display.flip()

pygame.quit()