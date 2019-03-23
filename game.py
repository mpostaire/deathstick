import cocos
from cocos.actions import *


class HelloWorld(cocos.layer.Layer):
    def __init__(self):
        super(HelloWorld, self).__init__()
        cursor = cocos.sprite.Sprite(
            image="cursor.png"
        )
        self.add(cursor)
        cursor.position = 100, 100
        cursor.do(RotateBy(360, 10))
        label = cocos.text.Label(
            'Hello, world',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center'
        )
        label.position = 0, 0
        label.do(RotateBy(360, 10))
        self.add(label)


if __name__ == '__main__':
    cocos.director.director.init()
    hello_layer = HelloWorld()
    main_scene = cocos.scene.Scene(hello_layer)
    cocos.director.director.run(main_scene)
