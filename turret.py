import string
import random
import time
import cocos
from cocos.text import Label
import cocos.euclid as eu
import cocos.collision_model
from projectile import Projectile
import cocos.euclid as eu


def predict_pos(vec_orig, speed_mag, vec_pos, vec_dir, delta, epsilon):
    diff_old, diff = None, None
    delta = delta/2
    old_pos = vec_pos
    while diff is None or diff_old is None or ((diff - diff_old) > epsilon):
        diff_old = diff
        #print(vec_pos.magnitude())
        delta = delta + 1
        #compute next target's pos
        old_pos = vec_pos
        vec_pos = vec_pos + delta * vec_dir
        #compute vector of aim
        orig_dir = (vec_pos - vec_orig).normalize() * speed_mag
        #compute next proj pos
        vec_orig = vec_orig + delta * orig_dir
        diff = (vec_orig - vec_pos).magnitude()
        if diff_old is not None and diff > diff_old:
            return old_pos

    return vec_pos
MAX_LEVEL = 10

class Turret():

    def __init__(self, pos, delay, dist, speed, ammo_type, bullet_len, level):
        self.pos = eu.Vector2(pos[0], pos[1])
        self.delay = delay
        self.dist = dist
        self.bullet_len = bullet_len
        self.speed = speed
        self.timer = delay
        self.level = level
        self.ammo_type = ammo_type# shape (characters) of the ammunitions
        self.projectiles = [] #all the bullets it shot that are still alive
        self.vec_player = None #a temporary variable used for inner computation
        self.bullet_count = 0

    def activate(self, layer, player):
        #the zero indexing is used to pass raw reference wrapped inside an array
        #dirty and hacky but it works just fine :)
        self.player = player[0]
        self.layer = layer[0]

    def update(self, delta):
        #update the logic of the turrets according to the delta time ellapsed
        self.vec_player = eu.Vector2(self.player.x, self.player.y)
        #diff is the vector between the player and the turret
        diff = next_ppos = predict_pos(
            self.pos,
            self.speed,
            self.vec_player,
            self.player.vec_speed,
            delta,
            5.0
        ) - self.pos

        self.timer -= delta#used to implement firing speed
        #check if the player is close enough
        if self.timer <= 0 and diff.magnitude() < self.dist:
            if self.bullet_count < self.level:
                self.shoot(diff, delta) #needs to be passed because we need the direction 
            else:
                self.shoot(self.vec_player - self.pos, delta) #needs to be passed because we need the direction
            global MAX_LEVEL
            self.bullet_count = (self.bullet_count + 1) % MAX_LEVEL
            self.timer = self.delay
        for proj in self.projectiles:
            proj.update(delta)

    def shoot(self, diff, delta):
        

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
