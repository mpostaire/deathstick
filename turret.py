import string
import random
import time
import cocos
from cocos.text import Label
import cocos.euclid as eu
import cocos.collision_model
from projectile import Projectile
import cocos.euclid as eu

class Turret():

    def __init__(self, pos, delay, dist, speed,  ammo_type):
        self.pos = eu.Vector2(pos[0], pos[1])
        self.delay = delay
        self.dist = dist
        self.speed = speed
        self.timer = delay
        self.ammo_type = ammo_type
        self.projectiles = []
        self.vec_player = None

    def activate(self, layer, player):
        self.player = player[0]
        self.layer = layer[0]

    def update(self, delta):
        #print("turret update, player pos x:{} y{}".format(self.player.x, self.player.y))
        self.vec_player = eu.Vector2(self.player.x, self.player.y)
        diff = eu.Vector2(self.vec_player.x - self.pos.x, self.vec_player.y - self.pos.y)

        self.timer -= delta
        print(self.timer)
        if self.timer <= 0 and diff.magnitude() < self.dist:
            self.shoot(diff)
            self.timer = self.delay
        for proj in self.projectiles:
            proj.update(delta)

    def shoot(self, diff):
        print("turret shot")
        proj = Projectile(
            [self.pos.x, self.pos.y],
            self.vec_player.angle(eu.Vector2(1, 0)),
            [self.layer],
            diff
        )
        proj.turret = self
        self.projectiles.append(proj)
        self.layer.add(proj)
