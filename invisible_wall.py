import cocos
import cocos.euclid as eu


class InvisibleWall():
    def __init__(self, rect, name):
        vec_center = eu.Vector2(rect.x + rect.width/2, rect.y + rect.height/2)
        self.cshape = cocos.collision_model.AARectShape(vec_center,  half_width=rect.width / 2,
                                                        half_height=rect.height / 2
                                                        )
        self.name = name
        self.rect = rect

