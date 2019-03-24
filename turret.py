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

    def __init__(self, pos, delay, dist, speed, ammo_type, bullet_len ):
        self.pos = eu.Vector2(pos[0], pos[1])
        self.delay = delay
        self.dist = dist
        self.bullet_len = bullet_len
        self.speed = speed
        self.timer = delay
        self.ammo_type = ammo_type# shape (characters) of the ammunitions
        self.projectiles = [] #all the bullets it shot that are still alive
        self.vec_player = None #a temporary variable used for inner computation

    def activate(self, layer, player):
        #the zero indexing is used to pass raw reference wrapped inside an array
        #dirty and hacky but it works just fine :)
        self.player = player[0]
        self.layer = layer[0]

    def update(self, delta):
        #update the logic of the turrets according to the delta time ellapsed
        self.vec_player = eu.Vector2(self.player.x, self.player.y)
        #diff is the vector between the player and the turret
        diff = eu.Vector2(self.vec_player.x - self.pos.x, self.vec_player.y - self.pos.y)

        self.timer -= delta#used to implement firing speed
        #check if the player is close enough
        if self.timer <= 0 and diff.magnitude() < self.dist:
            self.shoot(diff) #needs to be passed because we need the direction
            self.timer = self.delay
        for proj in self.projectiles:
            proj.update(delta)

    def shoot(self, diff):
        #spawns a bullet and adds it to the layer
        proj = Projectile(
            [self.pos.x, self.pos.y],
            self.vec_player.angle(eu.Vector2(1, 0)),
            [self.layer],
            diff,
            self.speed,
            self.bullet_len,
            self.ammo_type
        )
        proj.turret = self
        self.projectiles.append(proj)
        self.layer.add(proj)
