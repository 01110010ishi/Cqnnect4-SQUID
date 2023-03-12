import pygame
from pygame.locals import *
import pygame_gui

# Set up Pygame
pygame.init()
window = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Slider Example")
manager = pygame_gui.UIManager((400, 300))
# Create the sliders
theta_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 50), (300, 20)),
    start_value=0.5,
    value_range=(0.0, 1.0),
    manager=pygame_gui.UIManager((400, 300)),
)
phi_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 100), (300, 20)),
    start_value=0.5,
    value_range=(0.0, 1.0),
    manager=pygame_gui.UIManager((400, 300)),
)

# Main loop
while True:
    for event in pygame.event.get():

        # Update the sliders
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == theta_slider:
                    theta_value = event.value
                elif event.ui_element == phi_slider:
                    phi_value = event.value

        # Update the GUI
        manager.process_events(event)

    # Draw the sliders
    window.fill((255, 255, 255))
    manager.update(1/60.0)
    manager.draw_ui(window)
    pygame.display.update()

    # Print the slider values
    print("Theta: {:.2f}  Phi: {:.2f}".format(theta_slider.get_current_value(), phi_slider.get_current_value()))
