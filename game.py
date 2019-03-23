import cocos
from cocos.actions import *
from cocos.text import Label
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.director import director
from pyglet.window import key
import math


class HelloWorld(Layer):
    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()
        self.keys_pressed = set()

        self.cursor = cocos.sprite.Sprite(
            image="cursor.png"
        )
        self.cursor.position = 350, 350
        self.cursor.speed = 50
        self.cursor.angular_speed = 150
        self.cursor.rotation = 90
        self.add(self.cursor)

        self.schedule(self.update)

    def update(self, delta):
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
    hello_layer = HelloWorld()
    main_scene = Scene(hello_layer)
    director.run(main_scene)
