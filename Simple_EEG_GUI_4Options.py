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
BLUE = (16, 52, 166)

# Define screen dimensions
WIDTH = 750
HEIGHT = 870

# Define character dimensions
CHAR_SIZE_WIDTH = 400
CHAR_SIZE_HEIGHT = 150

# Define spacing between targets
SPACING = 100

# Define frequencies and phases for flickering values
freq = [12, 20, 15, 16]
ph = [180, 270, 0, 90]

# Counter to switch every character's color to Red color in its turn
counter = 0

# Define key labels
sentences = ["Turn lights On/Off", "Open/Close Door", "Turn TV On/Off", "Contact my emergency number"]

# Initialize Pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("QWERT Keyboard Interface")
font = pygame.font.SysFont(None, 27)
screen_background_color = (11,102,35)
screen.fill(screen_background_color)

# Define result rectangle
Result_Rect = pygame.Rect(170, 100, 1200, 100) # variable from device to another
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
    target_x = Result_Rect.left
    target_y = SPACING + Result_Rect.height + Result_Rect.top

    for i, key in enumerate(sentences):
        rect = pygame.Rect(target_x, target_y, CHAR_SIZE_WIDTH , CHAR_SIZE_HEIGHT)
        color = f40_shades_of_grey[i]
        draw_target(rect, color)
        draw_centered_text(key, rect)
        target_x += CHAR_SIZE_WIDTH + SPACING * 4
        if i % 2 == 1:
            target_x = Result_Rect.left
            target_y += CHAR_SIZE_HEIGHT + SPACING * 2

    # Draw Exit target
    EXIT_x = EXIT_y = 50
    CHAR_SIZE_exit = 50
    exit_rect = pygame.Rect(EXIT_x, EXIT_y, CHAR_SIZE_exit, CHAR_SIZE_exit)
    draw_target(exit_rect, WHITE)
    draw_centered_text('Exit', exit_rect)

# Event loop for the user interaction
running = True
sessionCount = 0
while running:
    global EXIT_x, EXIT_y, seconds, counterFlag, trigFlag, start_ticks
    if counter == 4:
        sessionCount += 1
        counter = 0
    if sessionCount == 8:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (EXIT_x <= mouse_x <= (EXIT_x + CHAR_SIZE_HEIGHT) and
                    EXIT_y <= mouse_y <= (EXIT_y + CHAR_SIZE_HEIGHT)):
                running = False

    time = pygame.time.get_ticks() / 240

    if pygame.time.get_ticks()/1000 < 5:
        f40_shades_of_grey = [WHITE] * 4
        create_characters(f40_shades_of_grey)
        start_ticks = pygame.time.get_ticks()
        # print(pygame.time.get_ticks()/1000)
        counterFlag = trigFlag = 1

    elif seconds <= 3:
        # The target we want the user to focus on will turn to RED, and the rest is WHITE for 0.5s
        print(counter)
        f40_shades_of_grey = [WHITE] * 4
        f40_shades_of_grey[counter] = BLUE
        create_characters(f40_shades_of_grey)
        if trigFlag:
            trigString = str(counter + 1)
            sendTrigger = trigString.encode()
            print("sendTrig=", sendTrigger)
            socket.sendto(sendTrigger, endPoint)
            counterFlag = 1
            trigFlag = 0

    elif seconds <= 8:
        print(counter)
        f40_shades_of_grey = []
        # Use the equation to output the shade we want (0 - black, 255 - white, in between - grey)
        # All characters are flickering for 5s
        for f, p in zip(freq, ph):
            shade = int((0.5 * (1 + math.sin(2 * np.pi * f * time + p))) * 255)
            f40_shades_of_grey.append((shade, shade, shade))
        create_characters(f40_shades_of_grey)

    elif seconds <= 8.1:
        f40_shades_of_grey = [WHITE] * 4
        create_characters(f40_shades_of_grey)
        if counterFlag:
            # trigString = str(0)
            # sendTrigger = trigString.encode()
            # socket.sendto(sendTrigger, endPoint)
            counterFlag = 0
            counter += 1
            trigFlag = 1

    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Time in seconds
    seconds = seconds % 8.1  # Duration of each character (10s)
    # print("sec % 10 =", seconds)

    # Update display
    pygame.display.flip()

pygame.quit()