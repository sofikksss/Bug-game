import pygame
from pygame.locals import *
from random import randint
import os

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

width, height = 64 * 10, 64 * 8
screen = pygame.display.set_mode((width, height))


class Player:
    def __init__(self, image_file_name, start_x, start_y, speed):
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), image_file_name))
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.keys = [False, False, False, False]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collide(self, wall):
        if (self.y >= wall.y and self.y <= wall.y + 64) and \
                ((self.x > 0 and self.x <= wall.wall_hole_ix * 64) or (
                        self.x > (wall.wall_hole_ix + 1) * 64 and self.x < width + 64)):
            return True
        else:
            return False

    def move(self, width, height):
        if self.keys[0]:
            if self.y > 0:
                self.y -= 0.5
        elif self.keys[2]:
            if self.y < height - 64:
                self.y += 0.5
        if self.keys[1]:
            if self.x > 0:
                self.x -= 0.5
        elif self.keys[3]:
            if self.x < width - 64:
                self.x += 0.5

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.keys[0] = True
            elif event.key == K_LEFT:
                self.keys[1] = True
            elif event.key == K_DOWN:
                self.keys[2] = True
            elif event.key == K_RIGHT:
                self.keys[3] = True

        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                self.keys[0] = False
            elif event.key == K_LEFT:
                self.keys[1] = False
            elif event.key == K_DOWN:
                self.keys[2] = False
            elif event.key == K_RIGHT:
                self.keys[3] = False


class Wall:
    def __init__(self, image_file_name, screen_width, screen_height):
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), image_file_name))
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.y = -64
        self.wall_hole_ix = randint(0, 8)
        self.nmbr_of_walls = 0
        self.speed = 0.1

    def draw(self, screen):
        for i in range(0, 10):
            if not (i == self.wall_hole_ix or i == self.wall_hole_ix + 1):
                screen.blit(self.image, (i * 64, self.y))

    def move(self):
        self.y += self.speed
        if self.y > self.screen_height:
            self.y = -64
            self.wall_hole_ix = randint(0, 8)
            self.nmbr_of_walls += 1
            self.speed += 0.01


is_game = False

while True:
    if not is_game:
        screen.fill((255, 255, 255))
        textsurface = myfont.render("Press enter to start", False, (0, 0, 0))
        screen.blit(textsurface, (180, 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    player = Player("bug.png", 256, 440, 0.5)
                    wall = Wall("wall.png", width, height)
                    is_game = True

    else:
        screen.fill((255, 255, 255))

        wall.move()
        if player.collide(wall):
            is_game = False

        player.draw(screen)
        wall.draw(screen)

        textsurface = myfont.render(str(wall.nmbr_of_walls), False, (0, 0, 0))
        screen.blit(textsurface, (10, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            player.handle_event(event)

        player.move(width, height)
