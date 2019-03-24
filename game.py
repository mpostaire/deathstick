import os

import pytmx
import cocos

from cocos.scene import Scene
from cocos.director import director
from cocos.text import Label
from cocos.sprite import Sprite
from pyglet.window import key
from cocos.actions import *
import cocos.collision_model as cm
import cocos.euclid as eu
import math

CURRENT_TMX = None
CURRENT_WALL_ARRAY = None
THE_ELDER_SCROLLS_MANAGER = None
BACKGROUND_RECT = None
COL_MGR = None


def get_path(file):
    return os.path.join(
        os.path.dirname(__file__),
        file)


def load_tmx(map_string):
    global CURRENT_TMX
    CURRENT_TMX = pytmx.TiledMap(map_string)


def get_background_path():
    global CURRENT_TMX
    print(CURRENT_TMX.get_tile_image_by_gid(1)[0])
    return CURRENT_TMX.get_tile_image_by_gid(1)[0]


def load_wall_array():
    global CURRENT_WALL_ARRAY
    global CURRENT_TMX
    global BACKGROUND_RECT
    CURRENT_WALL_ARRAY = list()
    for object in CURRENT_TMX.objects:
        top_left_y = object.y
        bottom_left_y = BACKGROUND_RECT.height - object.height - top_left_y

        rect = cocos.rect.Rect(object.x, bottom_left_y, object.width, object.height)
        CURRENT_WALL_ARRAY.append(rect)

#the background is offset in regard with the collision boxes

class Cursor(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y, radius):
        super(Cursor, self).__init__(image)
        self.position = 350, 350
        self.speed = 200
        self.angular_speed = 150
        self.rotation = 90
        self.velocity = 0, 0
        self.position = (center_x, center_y)
        vec_center= eu.Vector2(self.x + self.width/2, self.y + self.height/2)
        self.cshape = cocos.collision_model.AARectShape(vec_center, half_width=self.width/2, half_height=self.height/2)

class InvisibleWall():
    def __init__(self, rect):
        vec_center = eu.Vector2(rect.x + rect.width/2, rect.y + rect.height/2)
        self.cshape = cocos.collision_model.AARectShape(vec_center,  half_width=rect.width / 2,
                                                        half_height=rect.height / 2
                                                        )


class HelloWorld(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()
        self.keys_pressed = set()

        self.cursor = Cursor(
            "res/cursor.png",
            10, director.get_window_size()[1] - 10,
            0,
        )

        self.background = Sprite(
            image=get_background_path()
        )
        #à cacher
        global BACKGROUND_RECT
        BACKGROUND_RECT = self.background.get_rect()
        offset = BACKGROUND_RECT.width/2, BACKGROUND_RECT.height/2
        load_wall_array()
        ##

        self.background.position = offset

        self.label = Label(
            'x: y:',
            font_name='Times New Roman',
            color=(255, 0, 0, 255),
            font_size=64,
            anchor_x='center', anchor_y='center'
        )

        self.add(self.background)
        self.add(self.cursor)
        self.add(self.label)
        #adding stuff to the collision world
        COL_MGR = cocos.collision_model.CollisionManagerGrid(
            BACKGROUND_RECT.x + BACKGROUND_RECT.width/2,
            BACKGROUND_RECT.x + 3*BACKGROUND_RECT.width/2,
            BACKGROUND_RECT.y + BACKGROUND_RECT.height/2,
            BACKGROUND_RECT.y + 3*BACKGROUND_RECT.height / 2,
            16,
            16
        )

        for rect in CURRENT_WALL_ARRAY:
            COL_MGR.add(InvisibleWall(rect))
        COL_MGR.add(self.cursor)

        self.debug()

        self.schedule(self.update)

    def debug(self):
        global CURRENT_WALL_ARRAY
        for rect in CURRENT_WALL_ARRAY:
            draw_rect(rect, self)
        draw_rect(self.background.get_rect(), self)

    def update(self, delta):
        global THE_ELDER_SCROLLS_MANAGER
        THE_ELDER_SCROLLS_MANAGER.set_focus(self.cursor.position[0], self.cursor.position[1])
        self.label.element.text = "x: {}, y: {}".format(int(self.cursor.position[0]), int(self.cursor.position[1]))
        self.label.position = self.cursor.position[0] - 50, self.cursor.position[1] - +20

        for k in self.keys_pressed:
            if k == key.LEFT:
                self.cursor.do(RotateBy(-self.cursor.angular_speed * delta, 0))
            if k == key.RIGHT:
                self.cursor.do(RotateBy(self.cursor.angular_speed * delta, 0))

        x = (self.cursor.speed * delta) * math.sin(math.radians(self.cursor.rotation))
        y = (self.cursor.speed * delta) * math.cos(math.radians(self.cursor.rotation))
        self.cursor.position = self.cursor.position[0] + x, self.cursor.position[1] + y


    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        """This function is called when a key is released.

        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """

        self.keys_pressed.remove(key)

def draw_rect(rect, layer):
    # bottom line
    line = cocos.draw.Line(rect.get_origin(),
                           (rect.x + rect.width, rect.y),
                           (255, 0, 0, 255), 5)
    layer.add(line)

    # top line
    line = cocos.draw.Line((rect.x + rect.width, rect.y + rect.height),
                           (rect.x, rect.y + rect.height),
                           (255, 0, 0, 255), 5)
    layer.add(line)

    # left line
    line = cocos.draw.Line(rect.get_origin(),
                           (rect.x, rect.y + rect.height),
                           (255, 0, 0, 255), 5)
    layer.add(line)

    # right line
    line = cocos.draw.Line((rect.x + rect.width, rect.y),
                           (rect.x + rect.width, rect.y + rect.height),
                           (255, 0, 0, 255), 5)
    layer.add(line)

if __name__ == '__main__':
    director.init(width=800, height=600)
    #setting up the map
    load_tmx("res/testmap/map.tmx")
    THE_ELDER_SCROLLS_MANAGER = cocos.layer.ScrollingManager()
    THE_ELDER_SCROLLS_MANAGER.scale = 0.25

    THE_ELDER_SCROLLS_MANAGER.add(HelloWorld())
    THE_ELDER_SCROLLS_MANAGER.set_focus(10, director.get_window_size()[1] - 10)
    main_scene = Scene(THE_ELDER_SCROLLS_MANAGER)
    director.run(main_scene)
