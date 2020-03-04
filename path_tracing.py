import pygame
import math
import random
from shapely.geometry import LineString
pygame.init()


class Wall:
    def __init__(self, vec1: pygame.Vector2, vec2: pygame.Vector2, colour: tuple):
        self.vec1, self.vec2 = vec1, vec2
        self.vec1.x, self.vec2.x = random.randint(100, 1000), random.randint(100, 1000)
        self.vec1.y, self.vec2.y = random.randint(100, 700), random.randint(100, 700)
        self.colour = colour


class Player(pygame.Rect):
    def __init__(self, dims: tuple, colour: tuple):
        super().__init__(*dims)
        self.colour = colour


class Path:
    def __init__(self, vec: pygame.Vector2, colour: tuple):
        self.vec = vec
        self.colour = colour


width, height = 1024, 720
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
player_width = 20

player = Player((width // 2, height // 2, player_width, player_width), (255, 255, 255))
paths = [Path(pygame.Vector2(), (255, 0, 0)) for _ in range(50)]
walls = [Wall(pygame.Vector2(), pygame.Vector2(), (255, 255, 255)) for _ in range(10)]
angles = len(paths) / 360
ray_distance = 1000
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    mouse_pos = pygame.mouse.get_pos()
    player.x, player.y = mouse_pos
    for pos, path in enumerate(paths):
        path.vec.x = player.x + (ray_distance * math.cos(math.radians(pos / angles)))
        path.vec.y = player.y + (ray_distance * math.sin(math.radians(pos / angles)))

    for wall in walls:
        for path in paths:
            path_line = LineString([(player.x, player.y), (path.vec.x, path.vec.y)])
            wall_line = LineString([(wall.vec1.x, wall.vec1.y), (wall.vec2.x, wall.vec2.y)])
            intersection = path_line.intersection(wall_line)
            if intersection:
                path.vec.x, path.vec.y = intersection.x, intersection.y

    display.fill((0, 0, 0))

    for path in paths:
        pygame.draw.line(display, path.colour, (player.x + (player_width //2), player.y + (player_width //2)), (path.vec.x + (player_width //2), path.vec.y + (player_width //2)))

    for wall in walls:
        pygame.draw.line(display, wall.colour, (wall.vec1.x, wall.vec1.y), (wall.vec2.x, wall.vec2.y), 10)

    pygame.draw.rect(display, player.colour, player)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
