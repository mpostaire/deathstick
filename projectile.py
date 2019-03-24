import string
import random
import time
import cocos
from cocos.text import Label
import cocos.euclid as eu
import cocos.collision_model


class Projectile(Label):
    def __init__(self, position, rotation):
        self.size = 16
        super(Label, self).__init__(
            random.choice(string.ascii_lowercase),
            font_name='Times New Roman',
            color=(0, 0, 255, 255),
            font_size=self.size,
            anchor_x='center', anchor_y='center'
        )
        self.creation_time = time.time()
        self.lifetime = 0.0
        self.max_lifetime = 5.0
        self.speed = 250
        self.angular_speed = 100
        self.position = position
        self.rotation = rotation
        vec_center = eu.Vector2(self.x, self.y)
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.size / 2,
                                                        half_height=self.size / 2)

    def update_cshape(self):
        vec_center = eu.Vector2(self.x,
                                self.y,
                                )
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.size / 2,
                                                        half_height=self.size / 2)
