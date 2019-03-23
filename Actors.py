import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import sys

PLAYER = 0
WALL = 1

class Actor:
    def __init__(self,filename, tag):
        self.tag = tag
        if filename:
            self.img = pygame.image.load(filename).convert_alpha()
            self.rect = self.img.get_rect()
            self.pos = [0.0, 0.0]

    def act(self,delta):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def draw(self,location):
        if hasattr(self, 'img'):
            location.blit(self.img,self.rect)

class BasicWall(Actor):
    def __init__(self, x,y):
        super().__init__("brick.jpg", WALL)
        self.pos[0] = x
        self.pos[1] = y

class BasicPlayer(Actor):
    def __init__(self):
        super().__init__("cursor.png", PLAYER)
        self.vel = [0.0, 0.0]
        self.orig_img = self.img
        self.angle = 0
        self.center = self.rect.center
        self.angular_vel = 100

    def act(self,delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.turnLeft(delta)

        if keys[pygame.K_RIGHT]:
            self.turnRight(delta)

        if keys[pygame.K_UP]:
            self.pos[0] += 10 * delta
            self.pos[1] += 10 * delta

        # self.pos[0] += self.vel[0] * delta
        # self.pos[1] += self.vel[1] * delta
        super().act(delta)

    def turnLeft(self, delta):
        self.angle += (self.angular_vel * delta) % 360
        print(self.center)
        self.img = pygame.transform.rotate(self.orig_img, self.angle)
        self.rect = self.img.get_rect()
        self.img.get_rect().center = self.center
        print(self.img.get_rect().center)

    def turnRight(self, delta):
        self.angle -= (self.angular_vel * delta) % 360
        self.img = pygame.transform.rotate(self.orig_img, self.angle)

    def collide(self):
        sys.exit(0)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Basic Pygame program')
        background = pygame.Surface(self.screen.get_size())
        self.background = background.convert()
        self.background.fill((250, 250, 250))
        #code demo
        tmxdata = load_pygame("ressources/testmap/map.tmx")
        self.background.blit(tmxdata.get_tile_image_by_gid(1), (0, 0))

    def set_actors(self,actors, walls):
        self.actors = actors

        self.col_lists = {WALL:[]}
        if walls:
            for wall in walls:
                self.col_lists[WALL].append(wall)

        for actor in actors:
            if actor.tag == PLAYER:
                self.player_actor = actor
            if actor.tag in self.col_lists:
                self.col_lists[actor.tag].append(actor.rect)
            else:
                self.col_lists[actor.tag] = [actor.rect]

    def detect_collisions(self):
        for player in self.col_lists[PLAYER]:
            if player.collidelist(self.col_lists[WALL]) != -1:
                self.player_actor.collide()

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            self.update()

    def update(self):
        self.screen.blit(self.background, (0, 0))
        delta = self.clock.tick(60) / 1000

        for actor in self.actors:
            actor.act(delta)

        self.detect_collisions()

        for actor in self.actors:
            actor.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    player = BasicPlayer()
    wall = BasicWall(150,0)
    game.set_actors([wall, player], None)
    game.run()
