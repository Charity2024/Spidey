

import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Spiders Chasing Glow")

# Clock for controlling frame rate
clock = pygame.time.Clock()


# Vector utility function
def normalize_vector(dx, dy):
    #\"\"\"Normalize a vector (dx, dy) to have a magnitude of 1.\"\"\"
    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    return (dx / magnitude, dy / magnitude) if magnitude != 0 else (0, 0)


class Glow:
   # \"\"\"Class representing the moving light glow.\"\"\"
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2.5

    def move(self):
      #  \"\"\"Move the glow in a random yet smooth direction.\"\"\"
        self.x += random.uniform(-self.speed, self.speed)
        self.y += random.uniform(-self.speed, self.speed)

        # Ensure the glow stays on the screen
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))

    def draw(self):
        #Draw the glow on the screen.\"\"\"
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 10)


class Spider:
  #  \"\"\"Class representing a spider.\"\"\"
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = random.uniform(1.5, 3.5)  # Random base speed for each spider
        self.friction = 0.85
        self.vx = 0
        self.vy = 0
        self.state = "wandering"  # Possible states: wandering, chasing, pouncing
        self.target_x = random.randint(0, WIDTH)
        self.target_y = random.randint(0, HEIGHT)

    def wander(self):
        #\"\"\"Random wandering behavior for the spider.\"\"\"
        if random.random() < 0.02:  # Occasionally pick a new random target
            self.target_x = random.randint(0, WIDTH)
            self.target_y = random.randint(0, HEIGHT)

        self.move_towards(self.target_x, self.target_y)

        # Switch to chasing if close to the glow
        distance = math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)
        if distance < 100:
            self.state = "chasing"

    def chase(self, glow_x, glow_y):
       # \"\"\"Chase the glow.\"\"\"
        self.move_towards(glow_x, glow_y)

        # Pounce if close to the glow
        distance = math.sqrt((glow_x - self.x) ** 2 + (glow_y - self.y) ** 2)
        if distance < 30:
            self.state = "pouncing"

    def pounce(self, glow_x, glow_y):
       # \"\"\"Pounce at the glow with a burst of speed.\"\"\"
        self.move_towards(glow_x, glow_y, speed_multiplier=2.5)
        self.state = "chasing"  # Return to chasing after pouncing

    def move_towards(self, target_x, target_y, speed_multiplier=1.0):
       # \"\"\"Move the spider towards the target position.\"\"\"
        # Calculate direction vector
        dx, dy = target_x - self.x, target_y - self.y
        direction_x, direction_y = normalize_vector(dx, dy)

        # Adjust velocity toward the target with some inertia
        self.vx += direction_x * self.speed * speed_multiplier
        self.vy += direction_y * self.speed * speed_multiplier

        # Apply friction to slow down the spider
        self.vx *= self.friction
        self.vy *= self.friction

        # Update position
        self.x += self.vx
        self.y += self.vy

    def avoid_others(self, other_spiders):
       # \"\"\"Avoid colliding with other spiders.\"\"\"
        for other in other_spiders:
            if other is not self:
                dx, dy = self.x - other.x, self.y - other.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < 30:  # Minimum distance to maintain
                    direction_x, direction_y = normalize_vector(dx, dy)
                    self.x += direction_x * 2  # Push away slightly
                    self.y += direction_y * 2

    def draw(self):
       # \"\"\"Draw the spider on the screen.\"\"\"
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 8)


# Initialize objects
glow = Glow(WIDTH // 2, HEIGHT // 2)
spiders = [Spider(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.choice([RED, BLUE]))
           for _ in range(2)]

# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Clear screen

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update glow position
    glow.move()

    # Update spiders' positions
    for spider in spiders:
        if spider.state == "wandering":
            spider.wander()
        elif spider.state == "chasing":
            spider.chase(glow.x, glow.y)
        elif spider.state == "pouncing":
            spider.pounce(glow.x, glow.y)

        spider.avoid_others(spiders)  # Avoid other spiders
        spider.draw()

    # Draw glow
    glow.draw()

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()



