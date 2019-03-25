import cocos
import math
import cocos.euclid as eu


class Cursor(cocos.sprite.Sprite):
    def __init__(self, spawn_coords):
        super(Cursor, self).__init__("res/cursor.png")
        self.speed = 200
        self.angular_speed = 150
        self.rotation = spawn_coords[2]
        self.position = (spawn_coords[0], spawn_coords[1])
        self.shielded = False
        self.bullettime = False
        self.update_cshape()
        self.update_vec_speed()

    def update_vec_speed(self):
        self.vec_speed = eu.Vector2(
            math.sin(math.radians(self.rotation)) * self.speed,
            math.cos(math.radians(self.rotation)) * self.speed,
        )

    def update_cshape(self):
        vec_center = eu.Vector2(
                        self.x,
                        self.y,
                    )
        self.cshape = cocos.collision_model.AARectShape(
            vec_center, half_width=self.width / 4,
            half_height=self.height / 4
        )

    def update(self, delta):
        self.update_vec_speed()
        self.x = self.x + delta * self.vec_speed.x
        self.y = self.y + delta * self.vec_speed.y
        self.update_cshape()

    def get_rect(self):
        return cocos.rect.Rect(self.x - self.width/2, self.y - self.width/2, self.width, self.height)
