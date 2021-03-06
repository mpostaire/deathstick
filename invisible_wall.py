import cocos
import cocos.euclid as eu

"""
This class is used to instantiate invisible wall on the maps that kills the player 
on contact. It is supposed to be only used parsed from the Tiled Level Editor.
"""
class InvisibleWall():
    def __init__(self, rect, name):
        vec_center = eu.Vector2(rect.x + rect.width/2, rect.y + rect.height/2)
        self.cshape = cocos.collision_model.AARectShape(vec_center,  half_width=rect.width / 2,
                                                        half_height=rect.height / 2
                                                        )
        if name is None:
            self.name = "lose"
        else:
            self.name = name
        self.rect = rect

