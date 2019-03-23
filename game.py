import os

import pytmx
import cocos

from cocos.scene import Scene
from cocos.director import director
from pyglet.window import key
from cocos.actions import *
import math


CURRENT_TMX = None
CURRENT_WALL_ARRAY = None
THE_ELDER_SCROLLS_MANAGER = None


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
    CURRENT_WALL_ARRAY = list()
    for object in CURRENT_TMX.objects:
        rect = cocos.Rect(object.x, object.y, object.width, object.height)
        CURRENT_WALL_ARRAY.append(rect)


class HelloWorld(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()
        self.keys_pressed = set()

        self.cursor = cocos.sprite.Sprite(
            image="cursor.png"
        )
        self.cursor.position = 350, 350
        self.cursor.speed = 200
        self.cursor.angular_speed = 150
        self.cursor.rotation = 90
        self.background = cocos.sprite.Sprite(
            image=get_background_path()
        )
        self.cursor.position = 10, director.get_window_size()[1] - 10
        self.cursor.velocity = 0, 0

        self.label = cocos.text.Label(
            'x: y:',
            font_name='Times New Roman',
            font_size=12,
            anchor_x='center', anchor_y='center'
        )
        self.add(self.background)
        self.add(self.cursor)
        self.add(self.label)

        self.schedule(self.update)

    def update(self, delta):
        global THE_ELDER_SCROLLS_MANAGER
        THE_ELDER_SCROLLS_MANAGER.set_focus(self.cursor.position[0], self.cursor.position[1])
        self.label.element.text = "x: {}, y: {}".format(int(self.cursor.position[0]), int(self.cursor.position[1]))
        self.label.position = self.cursor.position[0], self.cursor.position[1] - 10

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


if __name__ == '__main__':
    director.init(width=800, height=600)
    load_tmx("ressources/testmap/map.tmx")
    THE_ELDER_SCROLLS_MANAGER = cocos.layer.ScrollingManager()

    THE_ELDER_SCROLLS_MANAGER.add(HelloWorld())
    THE_ELDER_SCROLLS_MANAGER.set_focus(10, director.get_window_size()[1] - 10)
    main_scene = Scene(THE_ELDER_SCROLLS_MANAGER)
    director.run(main_scene)
