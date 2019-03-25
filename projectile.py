import time
import cocos
import math
from cocos.text import Label
import cocos.euclid as eu
import cocos.collision_model

"""
This class represents laters that are shot at the players
They have a reference to their parent turret which are the only objects 
supposed to spawn those
"""
class Projectile(Label):
    def __init__(self, position, rotation, layer, speed_wagon, speed, bullet_len, char):
        self.size = 16
        super(Label, self).__init__(
            char,
            font_name='Times New Roman',
            color=(255, 0, 0, 255),
            font_size=self.size,
            anchor_x='center', anchor_y='center',
            bold=True
        )
        self.creation_time = time.time()
        self.lifetime = 0.0
        self.max_lifetime = bullet_len
        self.speed = speed
        self.speed_vec = speed_wagon.normalize() #direction of movement
        self.angular_speed = 100 #useless but no time to explain
        self.position = position
        self.rotation = rotation #direction of movement in degree
        self.layer = layer[0] #refernce to the layer it spawns in needed so we can remove the instances of projectile
        #from within this file, without needing to bloat the main file.
        self.turret = None #the turret variable needs to be set after this instance creation
        vec_center = eu.Vector2(self.x, self.y)
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.size / 2,
                                                        half_height=self.size / 2) #for collision purposes

    def update_cshape(self):
        #update collision shape of the projectile
        vec_center = eu.Vector2(self.x,
                                self.y,
                                )
        self.cshape = cocos.collision_model.AARectShape(
                        vec_center,
                        half_width=self.size / 2,
                        half_height=self.size / 2
                    )


    def update(self, delta):
        #defines the behavior of this object each delta time
        self.lifetime += delta
        if self.lifetime >= self.max_lifetime:
            self.remove()
            return

        x = (self.speed * delta) * self.speed_vec.x
        y = (self.speed * delta) * self.speed_vec.y
        self.position = self.position[0] + x, self.position[1] + y
        self.update_cshape()


    def spawn(self):
        self.layer.add(self)

    def remove(self):
        self.layer.remove(self)
        if self.turret is not None:
            #the turret holds an array of all the projectile it shots.
            #it is needed to remove this instance from it.
            self.turret.projectiles.remove(self)
            self.turret = None
