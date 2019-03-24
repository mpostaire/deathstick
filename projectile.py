import time
import cocos
import math
from cocos.text import Label
import cocos.euclid as eu
import cocos.collision_model


class Projectile(Label):
    def __init__(self, position, rotation, layer, speed_wagon, speed, bullet_len, char):
        self.size = 16
        super(Label, self).__init__(
            char,
            font_name='Times New Roman',
            color=(0, 0, 255, 255),
            font_size=self.size,
            anchor_x='center', anchor_y='center',
            bold=True
        )
        self.creation_time = time.time()
        self.lifetime = 0.0
        self.max_lifetime = bullet_len
        self.speed = speed
        self.speed_vec = speed_wagon.normalize()
        self.angular_speed = 100
        self.position = position
        self.rotation = rotation
        self.layer = layer[0]
        self.turret = None
        vec_center = eu.Vector2(self.x, self.y)
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.size / 2,
                                                        half_height=self.size / 2)

    def update_cshape(self):
        vec_center = eu.Vector2(self.x,
                                self.y,
                                )
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.size / 2, half_height=self.size / 2)

    def update(self, delta):
        self.lifetime += delta
        if self.lifetime >= self.max_lifetime:
            self.remove()
            self.turret.projectiles.remove(self)
            return

        x = (self.speed * delta) * self.speed_vec.x
        y = (self.speed * delta) * self.speed_vec.y
        self.position = self.position[0] + x, self.position[1] + y
        self.update_cshape()


    def spawn(self):
        self.layer.add(self)

    def remove(self):
        self.layer.remove(self)
