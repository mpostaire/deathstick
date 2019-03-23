import cocos
from cocos.actions import *
from cocos.text import Label
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.director import director
from pyglet.window import key


class HelloWorld(Layer):
    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()
        self.keys_pressed = set()

        self.cursor = cocos.sprite.Sprite(
            image="cursor.png"
        )
        self.cursor.position = 10, director.get_window_size()[1] - 10
        self.cursor.velocity = 0, 0
        self.add(self.cursor)

        self.schedule(self.update)

    def update(self, delta):
        for k in self.keys_pressed:
            if k == key.LEFT:
                self.cursor.position = self.cursor.position[0] - 50 * delta, self.cursor.position[1]
            if k == key.RIGHT:
                self.cursor.position = self.cursor.position[0] + 50 * delta, self.cursor.position[1]
            if k == key.UP:
                self.cursor.position = self.cursor.position[0], self.cursor.position[1] + 50 * delta
            if k == key.DOWN:
                self.cursor.position = self.cursor.position[0], self.cursor.position[1] - 50 * delta

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
