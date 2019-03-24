import cocos
import cocos.euclid as eu


class Cursor(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y, angle):
        super(Cursor, self).__init__(image)
        self.speed = 200
        self.angular_speed = 150
        self.rotation = angle
        self.position = (center_x, center_y)
        self.shielded = False
        self.bullettime = False
        vec_center = eu.Vector2(self.x , self.y )
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.width / 4,
                                                        half_height=self.height / 4)

    def update_cshape(self):
        vec_center = eu.Vector2(self.x ,
                                self.y ,
                                )
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.width / 4,
                                                        half_height=self.height / 4)

    def get_rect(self):
        return cocos.rect.Rect(self.x - self.width/2, self.y - self.width/2, self.width, self.height)
