from random import randint

import pygame

from classes.board import Board
from classes.q_piece import qPiece
from classes.game_myattempt import GameUI

# Define some colors
#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Quantum Gate Game")

# Set up the font
font = pygame.font.Font(None, 36)

# Define the buttons
gate_buttons = {
    'H': pygame.Rect(50, 50, 100, 50),
    'X': pygame.Rect(50, 120, 100, 50),
    'Y': pygame.Rect(50, 190, 100, 50),
    'Z': pygame.Rect(50, 260, 100, 50),
    'R': pygame.Rect(50, 330, 100, 50)
}

# Set up the quantum program
qp = qPiece(0, 0, 0, 0, 0)

# Game loop
end_game = False
end_gate_input = False
while not end_game:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a button was clicked
            for button in gate_buttons:
                if gate_buttons[button].collidepoint(event.pos):
                    if button == 'R':
                        theta = float(input('What theta value:'))
                        phi = float(input('What phi value:'))
                        qp.apply_gate('r', theta, phi)
                    else:
                        qp.apply_gate(button.lower())

                    # Print the probabilities
                    probs = qp.calculate_probs()
                    print(f"Probability for Q1 is {probs[0]} and probability for Q2 is {probs[1]}")

                    # Check if the user is done applying gates
                    done_gates = input("Are you done applying gates? (y or n)")
                    if done_gates == 'y':
                        end_gate_input = True

    # Draw the screen
    screen.fill(WHITE)

    # Draw the buttons
    for button in gate_buttons:
        pygame.draw.rect(screen, GRAY, gate_buttons[button])
        text = font.render(button, True, WHITE)
        text_rect = text.get_rect(center=gate_buttons[button].center)
        screen.blit(text, text_rect)

    # Update the screen
    pygame.display.update()

pygame.quit()
