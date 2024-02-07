import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 800, 600
BLUE = (0, 0, 139)  # Dark blue color for night sky
YELLOW = (255, 215, 0)  # Yellow color for construction lights
GRAY = (169, 169, 169)  # Gray color for construction elements
GAME_OVER_COLOR = (255, 0, 0)

# Player properties
player_width = 60
player_height = 100
player_stand_height = 100  # Height when standing
player_crouch_height = 50  # Height when crouching
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_stand_height
player_speed = 8
player_jump_power = 20
player_gravity = 1.5  # Increased gravity for faster falling
player_jump = False
player_jump_count = player_jump_power
double_jump = True
player_lives = 5

# Object properties
object_width = 50
object_height = 50
object_speed = 5

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer Game")

clock = pygame.time.Clock()

# Define a function to create objects
def create_object():
    type = random.choice(["spike", "rock", "pit"])
    x = WIDTH
    y = random.randint(HEIGHT // 2 + player_stand_height, HEIGHT - object_height - 50)  # Ensure objects are below player's head level
    return {"type": type, "x": x, "y": y}

objects = []

# Main game loop
running = True
while running:
    screen.fill(BLUE)  # Background color for night sky

    # Draw construction site elements
    pygame.draw.rect(screen, GRAY, (0, 400, 200, 200))  # Building structure 1
    pygame.draw.rect(screen, GRAY, (600, 350, 200, 250))  # Building structure 2
    for i in range(0, 200, 50):  # Windows for building 1
        pygame.draw.rect(screen, (255, 255, 255), (i, 400, 50, 50))
    pygame.draw.rect(screen, GRAY, (200, 450, 50, 150))  # Construction equipment 1
    pygame.draw.rect(screen, GRAY, (550, 450, 50, 150))  # Construction equipment 2
    pygame.draw.rect(screen, GRAY, (400, 480, 100, 120))  # Construction equipment 3
    pygame.draw.circle(screen, YELLOW, (150, 100), 20)  # Construction light

    # Check if player has lost all lives
    if player_lives <= 0:
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER!", True, GAME_OVER_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_x += player_speed
            elif event.key == pygame.K_UP and not player_jump:
                player_jump = True
            elif event.key == pygame.K_DOWN:
                player_height = player_crouch_height
            elif event.key == pygame.K_SPACE and not player_jump and player_height == player_stand_height:
                if double_jump:
                    player_jump = True
                    double_jump = False

        # Handle key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_height = player_stand_height

    # Apply gravity
    if player_jump:
        player_y -= player_jump_count
        player_jump_count -= 1
        if player_jump_count < -player_jump_power:
            player_jump = False
            player_jump_count = player_jump_power
            double_jump = True
    else:
        if player_y < HEIGHT - player_height:
            player_y += player_gravity

    # Move the objects
    for obj in objects:
        obj["x"] -= object_speed

    # Create new objects
    if len(objects) < 5:
        objects.append(create_object())

    # Remove objects that are off-screen
    objects = [obj for obj in objects if obj["x"] > -object_width]

    # Check collision between player and objects
    for obj in objects:
        if obj["x"] < player_x + player_width and \
           obj["x"] + object_width > player_x and \
           obj["y"] < player_y + player_height and \
           obj["y"] + object_height > player_y:
            player_lives -= 1
            objects.remove(obj)

    # Draw the objects
    for obj in objects:
        if obj["type"] == "spike":
            pygame.draw.polygon(screen, (255, 0, 0), [(obj["x"], obj["y"] + object_height),
                                                      (obj["x"] + object_width, obj["y"] + object_height),
                                                      (obj["x"] + object_width // 2, obj["y"])])
        elif obj["type"] == "rock":
            pygame.draw.circle(screen, (128, 128, 128), (obj["x"] + object_width // 2, obj["y"] + object_height // 2), object_width // 2)
        elif obj["type"] == "pit":
            pygame.draw.rect(screen, (0, 0, 0), (obj["x"], obj["y"] + object_height // 2, object_width, object_height // 2))

    # Draw the player (human figure)
    pygame.draw.rect(screen, (255, 206, 158), (player_x, player_y, player_width, player_height))  # Body
    pygame.draw.ellipse(screen, (0, 0, 0), (player_x, player_y - player_height // 4, player_width, player_height // 2))  # Head
    pygame.draw.line(screen, (0, 0, 0), (player_x + player_width // 2, player_y + player_height // 2), (player_x + player_width // 2, player_y + player_height * 3 // 4), 3)  # Torso
    pygame.draw.line(screen, (0, 0, 0), (player_x + player_width // 2, player_y + player_height // 2), (player_x + player_width // 4, player_y + player_height * 3 // 4), 3)  # Left arm
    pygame.draw.line(screen, (0, 0, 0), (player_x + player_width // 2, player_y + player_height // 2), (player_x + player_width * 3 // 4, player_y + player_height * 3 // 4), 3)  # Right arm
    pygame.draw.line(screen, (0, 0, 0), (player_x + player_width // 2, player_y + player_height * 3 // 4), (player_x + player_width // 4, player_y + player_height * 7 // 8), 3)  # Left leg
    pygame.draw.line(screen, (0, 0, 0), (player_x + player_width // 2, player_y + player_height * 3 // 4), (player_x + player_width * 3 // 4, player_y + player_height * 7 // 8), 3)  # Right leg

    # Draw player lives as hearts
    heart_spacing = 40
    for i in range(player_lives):
        pygame.draw.polygon(screen, (255, 0, 0), [(10 + i * heart_spacing, 10),
                                                  (20 + i * heart_spacing, 20),
                                                  (10 + i * heart_spacing, 30),
                                                  (5 + i * heart_spacing, 20)])

    pygame.display.update()
    clock.tick(30)
