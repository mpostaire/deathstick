import cocos
import cocos.euclid as eu


class Cursor(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y, radius):
        super(Cursor, self).__init__(image)
        self.position = 350, 350
        self.speed = 200
        self.angular_speed = 150
        self.rotation = 90
        self.velocity = 0, 0
        self.position = (center_x, center_y)
        vec_center = eu.Vector2(self.x , self.y )
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.width / 4,
                                                        half_height=self.height / 4)

    def update_cshape(self, delta):
        vec_center = eu.Vector2(self.x ,
                                self.y ,
                                )
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.width / 4,

                                                        half_height=self.height / 4)
    def get_rect(self):
        return cocos.rect.Rect(self.x - self.width/2, self.y - self.width/2, self.width, self.height)
