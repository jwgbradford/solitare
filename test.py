import pygame
import math

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Parametric Heart")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Heart function parameters
a = 50  # Adjust for size
b = 50  # Adjust for shape
scale = 10  # Adjust for overall size

# Function to calculate heart coordinates
def heart_coordinates(t, a, b):
    x = 16 * math.sin(t)**3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, y

# Main loop
running = True
t = 0
points = []
print('start calc')
while t < 2 * math.pi:
    # Calculate the next point on the heart curve
    t += 0.001  # Adjust for speed of drawing

    x, y = heart_coordinates(t, a, b)

    # Scale and center the coordinates
    scaled_x = int(screen_width / 2 + x * scale)
    scaled_y = int(screen_height / 2 - y * scale)  # Subtract y to flip vertically

    # Add the point to the list
    points.append((scaled_x, scaled_y))

    # Draw the heart by connecting the points
#print(points)
#main loop
while running:
    for each_event in pygame.event.get():
        if each_event.type == pygame.QUIT:
            running = False
    # Clear the screen
    screen.fill(black)
    
    #pygame.draw.lines(screen, red, False, points, 2)
    pygame.draw.polygon(screen, red, points, 0)
    
    #pygame.draw.circle(screen, red, (screen_width // 2, screen_height // 2), 100, 0)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(50)  # Adjust for speed of drawing

# Quit Pygame
pygame.quit()