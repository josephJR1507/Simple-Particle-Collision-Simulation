import pygame
import random
import math

# --- Configuration ---
SPACE_SIZE = 1000
FPS = 60
PARTICLE_COUNT = 50
BG_COLOR = (10, 10, 20)  # Dark midnight blue

class Particle:
    def __init__(self):
        self.radius = random.randint(8, 15)
        self.x = random.randint(self.radius, SPACE_SIZE - self.radius)
        self.y = random.randint(self.radius, SPACE_SIZE - self.radius)
        self.vx = random.uniform(-150, 150)
        self.vy = random.uniform(-150, 150)
        self.color = (random.randint(50, 255), random.randint(50, 255), 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self, dt):
        # Move
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Wall Bounces
        if self.x < self.radius or self.x > SPACE_SIZE - self.radius:
            self.vx *= -1
            self.x = max(self.radius, min(self.x, SPACE_SIZE - self.radius))
            
        if self.y < self.radius or self.y > SPACE_SIZE - self.radius:
            self.vy *= -1
            self.y = max(self.radius, min(self.y, SPACE_SIZE - self.radius))

def handle_collisions(particles):
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1, p2 = particles[i], particles[j]
            
            # Distance formula: sqrt((x2-x1)^2 + (y2-y1)^2)
            dx = p1.x - p2.x
            dy = p1.y - p2.y
            distance = math.hypot(dx, dy)

            # Check if they are overlapping
            if distance < p1.radius + p2.radius:
                # Simple elastic collision (swap velocities)
                # This makes them look like they're bouncing!
                p1.vx, p2.vx = p2.vx, p1.vx
                p1.vy, p2.vy = p2.vy, p1.vy
                
                # Prevent particles from getting stuck inside each other
                overlap = 0.5 * (p1.radius + p2.radius - distance + 1)
                p1.x += overlap * (dx / distance)
                p1.y += overlap * (dy / distance)
                p2.x -= overlap * (dx / distance)
                p2.y -= overlap * (dy / distance)

# --- Main Setup ---
pygame.init()
screen = pygame.display.set_mode([SPACE_SIZE, SPACE_SIZE])
pygame.display.set_caption("Particle Collision Simulator")
clock = pygame.time.Clock()

particles = [Particle() for _ in range(PARTICLE_COUNT)]

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logic
    for p in particles:
        p.update(dt)
    handle_collisions(particles)

    # Rendering
    screen.fill(BG_COLOR)
    for p in particles:
        p.draw(screen)
    
    pygame.display.flip()

pygame.quit()