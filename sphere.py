import pygame
import math

pygame.init()

size = (500, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("3D Sphere with Gradient")


def draw_sphere(center, radius, num_circles):
    for i in range(num_circles):
        color = (255 * i // num_circles, 255 * i // num_circles, 255 * i // num_circles)
        pygame.draw.circle(screen, color, center, int(radius * (num_circles - i) / num_circles))


def rotate_2d(pos, rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)
    return x * c - y * s, y * c + x * s


def project(pos, z):
    x, y = pos
    f = 200 / (200 + z)
    return x * f + size[0] / 2, y * f + size[1] / 2


def get_xyz(theta, phi, radius):
    x = math.sin(theta) * math.cos(phi) * radius
    y = math.sin(theta) * math.sin(phi) * radius
    z = math.cos(theta) * radius
    return x, y, z


def rotate_xyz(x, y, z, ax, ay, az):
    # rotate x axis
    y, z = rotate_2d((y, z), ax)
    # rotate y axis
    x, z = rotate_2d((x, z), ay)
    # rotate z axis
    x, y = rotate_2d((x, y), az)
    return x, y, z


running = True

theta, phi, radius = 0, 0, 100
num_circles = 50
ax, ay, az = 0, 0, 0

rotate_sphere = False  # flag to track mouse button state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                rotate_sphere = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # left mouse button
                rotate_sphere = False

    if rotate_sphere:
        # get relative mouse position
        x, y = pygame.mouse.get_rel()
        # calculate rotation angles based on mouse position
        rot_x = x / 100
        rot_y = y / 100
        ax += rot_x
        ay += rot_y

    screen.fill((0, 0, 0))

    center = (250, 250)

    for i in range(num_circles):
        theta = i / num_circles * math.pi
        for j in range(num_circles):
            phi = j / num_circles * math.pi * 2
            x, y, z = get_xyz(theta, phi, radius)
            x, y, z = rotate_xyz(x, y, z, ax, ay, az)
            x, z = rotate_2d((x, z), math.pi / 4)
            x, y = rotate_2d((x, y), math.pi / 4)
            x, y = project((x, y), z)
            color = (255 * i // num_circles, 255 * i // num_circles, 255 * i // num_circles)
            pygame.draw.circle(screen, color, (int(x), int(y)), int(radius * z / radius))

    pygame.display.flip()

pygame.quit()
