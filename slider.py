import pygame
from classes.q_piece import qPiece

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Define the Slider class
class Slider:
    def __init__(self, screen, x, y, width, height, min_value, max_value, default_value):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_rect = pygame.Rect(x, y - 10, 20, height + 20)
        self.min_value = min_value
        self.max_value = max_value
        self.value = default_value
        self.dragging = False
        self._font = pygame.font.SysFont('Calibri', 26)

    def get_value(self):
        return self.value

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, [self.x - 30, self.y - 30, self.width + 60, self.height + 60])
        # Draw the slider
        pygame.draw.rect(self.screen, GRAY, self.rect)
        pygame.draw.rect(self.screen, BLACK, self.knob_rect)

        # Draw the value text
        self.draw_value_text()

    def update_knob(self):
        # Update the knob position
        self.knob_rect.x = self.rect.x + int(
            (self.value - self.min_value) * self.rect.width / (self.max_value - self.min_value)) - 10

        # Draw the value text
        self.draw_value_text()

    def draw_value_text(self):
        # Render the value text
        value_text = self._font.render(str((self.value//0.01)/100), True, (0, 0, 0))

        # Position the value text
        # value_text_rect = pygame.draw.rect
        value_text_rect = value_text.get_rect()
        value_text_rect.center = (self.knob_rect.centerx, self.knob_rect.centery - 25)

        # Draw the value text
        self.screen.blit(value_text, value_text_rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse clicked on the knob
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # Stop dragging the knob when the mouse button is released
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            # If the knob is being dragged, update its position and value
            if self.dragging:
                self.knob_rect.x = event.pos[0]
                if self.knob_rect.x < self.rect.x:
                    self.knob_rect.x = self.rect.x
                elif self.knob_rect.x > self.rect.x + self.rect.width:
                    self.knob_rect.x = self.rect.x + self.rect.width
                self.value = self.min_value + (self.knob_rect.x - self.rect.x) * (
                        self.max_value - self.min_value) / self.rect.width
                # self.value = (self.value // 0.1) * 10
                self.draw_value_text()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Define the sliders
    theta_slider = Slider(screen, 50, 50, 300, 20, 0, 360, 0)
    phi_slider = Slider(screen, 50, 100, 300, 20, 0, 360, 0)

    # Define the main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Handle events for each slider
                theta_slider.handle_event(event)
                phi_slider.handle_event(event)

        # Fill the screen with white

        # Draw the sliders and knobs
        theta_slider.draw()
        phi_slider.draw()

        # Update the knob positions
        theta_slider.update_knob()
        phi_slider.update_knob()

        # Update the screen
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
