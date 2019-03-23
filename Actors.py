import pygame
from pygame.locals import *

class Actor:
    def __init__(self,filename, tag):
        self.tag = tag
        if filename:
            self.img = pygame.image.load(filename)
            self.rect = self.img.get_rect()
            self.pos = [0.0, 0.0]
        pass

    def act(self,delta):
        self.pos[0] = self.pos[0] + delta*30/1000
        self.rect.x = self.pos[0]

    def draw(self,location):
        location.blit(self.img,self.rect)

    def get_tag(self):
        return self.tag

    def collide_with(self,other_col):
        print(other_col)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Basic Pygame program')
        background = pygame.Surface(self.screen.get_size())
        self.background = background.convert()
        self.background.fill((250, 250, 250))

    def set_actors(self,actors):
        self.actors = actors

        self.col_lists = {}
        for actor in actors:
            if actor.get_tag() in self.col_lists:
                self.col_lists[actor.get_tag()].append(actor)
            else:
                self.col_lists[actor.get_tag()] = [actor]

    def run(self):
        print(self.col_lists)
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            self.update()

    def update(self):
        self.screen.blit(self.background, (0, 0))
        delta = self.clock.tick(60)

        for actor in self.actors:
            actor.act(delta)

        for actor in self.actors:
            actor.draw(self.screen)

        pygame.display.flip()


game = Game()
ball = Actor('intro_ball.gif', 'project')
player = Actor('intro_ball.gif', 'player')
game.set_actors([ball, player])
game.run()