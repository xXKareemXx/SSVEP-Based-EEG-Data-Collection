import math
import numpy as np
import pygame
import socket

# Initialize socket for sending triggers to the Unicorn_Recorder
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
endPoint = ("127.0.0.1", 1000)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)

# Define screen dimensions
WIDTH = 1980
HEIGHT = 1080

# Define character dimensions
CHAR_SIZE = 80

# Define spacing between targets
SPACING = 40

# Define frequencies and phases for flickering values
freq = [14, 14.2, 14.4, 14.6, 14.8, 15, 15.2, 15.4, 15.6, 13.8,
        11.8, 13, 9.4, 12, 12.4, 13.4, 12.6, 10.2, 11.4, 11.6,
        8.6, 12.2, 9.2, 9.6, 9.8, 10, 10.4, 10.6, 10.8,
        13.6, 13.2, 9, 12.8, 8.8, 11.2, 11,
        15.8, 8.4, 8, 8.2]

ph = [180, 270, 0, 90, 180, 270, 0, 90, 180, 270,
      0, 90, 180, 270, 0, 90, 180, 270, 0, 90,
      180, 270, 0, 90, 180, 270, 0, 90, 180,
      270, 0, 90, 180, 270, 0, 90,
      180, 270, 0, 90]

# Counter to switch every character's color to Red color in its turn
counter = 0

# Define key labels
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
alphabets = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p",
             "a", "s", "d", "f", "g", "h", "j", "k", "l",
             "z", "x", "c", "v", "b", "n", "m"]
non_alphanumeric = ["YES", "NO", "_", "VOICE"]

# Initialize Pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("QWERT Keyboard Interface")
font = pygame.font.SysFont(None, 32)

# Define result rectangle
Result_Rect = pygame.Rect(480, 200, 1000, 80)
pygame.draw.rect(screen, WHITE, Result_Rect)

# Draw text centered on a rectangle
def draw_centered_text(text, rect):
  text_surface = font.render(text, True, BLACK)
  text_rect = text_surface.get_rect(center=rect.center)
  screen.blit(text_surface, text_rect)

# Draw a target rectangle
def draw_target(rect, color):
  pygame.draw.rect(screen, color, rect)

def create_characters(f40_shades_of_grey):
    global EXIT_x, EXIT_y

    # Calculate target positions
    target_x = x = 400
    target_y = SPACING + Result_Rect.height + Result_Rect.top

    # Draw targets and labels
    for i, key in enumerate(numbers):
        rect = pygame.Rect(target_x, target_y, CHAR_SIZE, CHAR_SIZE)
        color = f40_shades_of_grey[i]
        draw_target(rect, color)
        draw_centered_text(key, rect)
        target_x += CHAR_SIZE + SPACING

    target_x = x
    target_y += CHAR_SIZE + SPACING

    for i, key in enumerate(alphabets):
        rect = pygame.Rect(target_x, target_y, CHAR_SIZE, CHAR_SIZE)
        color = f40_shades_of_grey[i + 10]
        draw_target(rect, color)
        draw_centered_text(key, rect)
        target_x += (CHAR_SIZE + SPACING)
        if key == 'p':
            target_x = (x + CHAR_SIZE / 2)
            target_y += CHAR_SIZE + SPACING
        elif key == 'l':
            target_x = (x + CHAR_SIZE / 2) + (CHAR_SIZE + SPACING)
            target_y += CHAR_SIZE + SPACING
        elif key == 'm':
            target_x = (x + CHAR_SIZE / 2) + (CHAR_SIZE + SPACING) * 2
            target_y += CHAR_SIZE + SPACING

    # Draw space rectangle and labels
    Space_Rect_Width = (CHAR_SIZE + SPACING) * 4 + CHAR_SIZE
    space_rect = pygame.Rect(target_x, target_y, Space_Rect_Width, CHAR_SIZE)
    color = f40_shades_of_grey[38]
    draw_target(space_rect, color)
    draw_centered_text(non_alphanumeric[2], space_rect)

    # Draw YES target
    YES_x = target_x + (CHAR_SIZE + SPACING) * 6
    YES_y = target_y - CHAR_SIZE - SPACING
    yes_rect = pygame.Rect(YES_x, YES_y, CHAR_SIZE, CHAR_SIZE)
    color = f40_shades_of_grey[36]
    draw_target(yes_rect, color)
    draw_centered_text(non_alphanumeric[0], yes_rect)

    # Draw NO target
    NO_x = target_x - (CHAR_SIZE + SPACING) * 2
    NO_y = YES_y
    no_rect = pygame.Rect(NO_x, NO_y, CHAR_SIZE, CHAR_SIZE)
    color = f40_shades_of_grey[37]
    draw_target(no_rect, color)
    draw_centered_text(non_alphanumeric[1], no_rect)

    # Draw VOICE target
    VOICE_x = YES_x + 120
    VOICE_y = target_y - (CHAR_SIZE + SPACING) * 2
    voice_rect = pygame.Rect(VOICE_x, VOICE_y, CHAR_SIZE, CHAR_SIZE)
    color = f40_shades_of_grey[39]
    draw_target(voice_rect, color)
    draw_centered_text(non_alphanumeric[3], voice_rect)

    # Draw VOICE target
    EXIT_x = NO_x - 120
    EXIT_y = VOICE_y
    exit_rect = pygame.Rect(EXIT_x, EXIT_y, CHAR_SIZE, CHAR_SIZE)
    draw_target(exit_rect, WHITE)
    draw_centered_text('Exit', exit_rect)

# Event loop for the user interaction
running = True
sessionCount = 0
while running:
    global EXIT_x, EXIT_y, seconds, counterFlag, trigFlag, start_ticks
    if counter == 40:
        sessionCount += 1
        counter = 0
    if sessionCount == 2:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (EXIT_x <= mouse_x <= (EXIT_x + CHAR_SIZE) and
                    EXIT_y <= mouse_y <= (EXIT_y + CHAR_SIZE)):
                running = False

    time = pygame.time.get_ticks() / 144

    if pygame.time.get_ticks()/1000 < 5:
        f40_shades_of_grey = [WHITE] * 40
        create_characters(f40_shades_of_grey)
        start_ticks = pygame.time.get_ticks()
        # print(pygame.time.get_ticks()/1000)
        counterFlag = trigFlag = 1

    elif seconds <= 0.5:
        # The target we want the user to focus on will turn to RED, and the rest is WHITE for 0.5s
        f40_shades_of_grey = [WHITE] * 40
        f40_shades_of_grey[counter] = RED
        create_characters(f40_shades_of_grey)
        if trigFlag:
            trigString = str(counter + 1)
            sendTrigger = trigString.encode()
            print("sendTrig=", sendTrigger)
            socket.sendto(sendTrigger, endPoint)
            counterFlag = 1
            trigFlag = 0

    elif seconds <= 5.5:
        f40_shades_of_grey = []
        # Use the equation to output the shade we want (0 - black, 255 - white, in between - grey)
        # All characters are flickering for 5s
        for f, p in zip(freq, ph):
            shade = int((0.5 * (1 + math.sin(2 * np.pi * f * time + p))) * 255)
            f40_shades_of_grey.append((shade, shade, shade))
        create_characters(f40_shades_of_grey)

    elif seconds <= 9:
        # Rest for 3s
        f40_shades_of_grey = [WHITE] * 40
        create_characters(f40_shades_of_grey)
        if counterFlag:
            trigString = str(0)
            sendTrigger = trigString.encode()
            socket.sendto(sendTrigger, endPoint)
            counterFlag = 0
            counter += 1
            trigFlag = 1

    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Time in seconds
    seconds = seconds % 9  # Duration of each character (9s)
    # print("sec % 9 =", seconds)

    # Update display
    pygame.display.flip()

pygame.quit()