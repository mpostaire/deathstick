import os

import pytmx
import cocos
import sys

from cocos.scene import Scene
from cocos.director import director
from bullettime import BulletTime
from cocos.sprite import Sprite
from pyglet.window import key
from cocos.actions import *
from cursor import Cursor
from helpers import draw_rect
from projectile import Projectile
from invisible_wall import InvisibleWall
from turret import Turret
from adstop import AdStop

import cocos.collision_model as cm

CURRENT_TMX = None  # Holds the tmx that loads the map
CURRENT_WALL_ARRAY = None  # Holds only the objects representing the deadly walls
THE_ELDER_SCROLLS_MANAGER = None  # funny name for the scrolling manager
DELAYED_ARRAY = None  # holds the objects that need a layer and cursor instance to be fully operational
BACKGROUND_RECT = None  # background dimensions
COL_MGR = None  # collision manager
SPAWN = [0, 0]  # default spawn position

# helper function
def get_path(file):
    return os.path.join(
        os.path.dirname(__file__),
        file)

# loads tmx from file and replace current_tmx
def load_tmx(map_string):
    global CURRENT_TMX
    CURRENT_TMX = pytmx.TiledMap(map_string)

# gets the background path from the tmx's data
def get_background_path():
    global CURRENT_TMX
    print(CURRENT_TMX.get_tile_image_by_gid(1)[0])
    return CURRENT_TMX.get_tile_image_by_gid(1)[0]

# extract the deadly invisible walls from the tmx
# and loads a lot of the other entities on the map
def load_wall_array():
    global CURRENT_WALL_ARRAY
    global CURRENT_TMX
    global BACKGROUND_RECT
    global SPAWN
    global DELAYED_ARRAY

    CURRENT_WALL_ARRAY = list()
    DELAYED_ARRAY = list()
    for object in CURRENT_TMX.objects:
        top_left_y = object.y
        bottom_left_y = BACKGROUND_RECT.height - object.height - top_left_y
        bottom_left_x = object.x

        rect = cocos.rect.Rect(object.x, bottom_left_y, object.width, object.height)
        wall = InvisibleWall(rect, object.name)#?
        # guessing the type of the parsed game entity
        split = wall.name.split(":")
        if split[0] == "spawn":
            # it's a spawn point
            SPAWN = [bottom_left_x, bottom_left_y, float(split[1])]
        elif split[0] == "turret":
            print(split)  # pos, delay, dist, speed, ammo
            DELAYED_ARRAY.append(
                Turret(
                        (bottom_left_x, bottom_left_y),
                        float(split[2]),
                        float(split[3]),
                        float(split[4]),
                        split[1],
                        float(split[5]),
                        int(split[6])
                    )
            )
        CURRENT_WALL_ARRAY.append(wall)


def spawn_delayed(layer, player):
    global DELAYED_ARRAY
    for delayed in DELAYED_ARRAY:
        delayed.activate(layer, player)


class Game(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self, name):
        super(Game, self).__init__()

        self.name = name

        self.keys_pressed = set()

        self.projectiles = list()

        self.background = Sprite(
            image=get_background_path()
        )
        # à cacher
        global BACKGROUND_RECT
        BACKGROUND_RECT = self.background.get_rect()
        offset = BACKGROUND_RECT.width/2, BACKGROUND_RECT.height/2
        load_wall_array()

        global SPAWN
        self.cursor = Cursor(SPAWN)
        ##

        self.background.position = offset

        spawn_delayed([self], [self.cursor])
        self.add(self.background)

        self.adstop = AdStop(self.cursor)
        self.add(self.adstop)

        self.bullettime = BulletTime(self.cursor)
        self.add(self.bullettime)

        self.add(self.cursor)


        # adding stuff to the collision world
        global COL_MGR
        COL_MGR = cocos.collision_model.CollisionManagerGrid(
            BACKGROUND_RECT.x + BACKGROUND_RECT.width/2,
            BACKGROUND_RECT.x + 3*BACKGROUND_RECT.width/2,
            BACKGROUND_RECT.y + BACKGROUND_RECT.height/2,
            BACKGROUND_RECT.y + 3*BACKGROUND_RECT.height / 2,
            16,
            16
        )

        # self.debug()
        self.schedule(self.update)
    # used to draw collisions boxes etc
    def debug(self):
        global CURRENT_WALL_ARRAY
        for rect in CURRENT_WALL_ARRAY:
            draw_rect(rect.rect, self)

        draw_rect(self.cursor.get_rect(), self)
    # holds logic
    def update(self, delta):
        if self.cursor.bullettime:
            delta *= 0.5
        # reacting to keypresses
        for k in self.keys_pressed:
            if k == key.LEFT:
                self.cursor.do(RotateBy(-self.cursor.angular_speed * delta, 0))
            if k == key.RIGHT:
                self.cursor.do(RotateBy(self.cursor.angular_speed * delta, 0))
            if k == key.SPACE:
                self.adstop.activate()
            if k == key.B:
                self.bullettime.activate()

        self.cursor.update(delta)

        self.adstop.act(delta)
        self.bullettime.act(delta)

        global COL_MGR
        global CURRENT_WALL_ARRAY
        global DELAYED_ARRAY

        COL_MGR.clear()  # fast, no leaks even if changed cshapes
        COL_MGR.add(self.cursor)  # it's the way internet says it has to be done
        for delayed in DELAYED_ARRAY:
            delayed.update(delta)
            if type(delayed) == Turret:
                for proj in delayed.projectiles:
                    COL_MGR.add(proj)
        for wall in CURRENT_WALL_ARRAY:
            COL_MGR.add(wall)

        for p in self.projectiles:
            p.update(delta)
            COL_MGR.add(p)

            for other in COL_MGR.iter_colliding(p):
                if type(other) == InvisibleWall:
                    self.remove(p)
                    self.projectiles.remove(p)

        for other in COL_MGR.iter_colliding(self.cursor):
            if type(other) == Projectile:
                if self.cursor.shielded:
                    self.adstop.reset()
                    other.remove()
                    continue
                else:
                    print("you lost")
                    run_level(self.name)
                    break
            split = other.name.split(":")
            if split[0] == "win":
                print("you win")
                if split[1] == "end":
                    print("Java c'est plus meilleur.")
                    sys.exit(0)
                else:
                    run_level(split[1])
                    break
            elif split[0] == "lose":
                print("you lost")
                run_level(self.name)
                break

        global THE_ELDER_SCROLLS_MANAGER
        THE_ELDER_SCROLLS_MANAGER.set_focus(self.cursor.position[0], self.cursor.position[1])

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        try:
            self.keys_pressed.remove(key)
        except:
            print('tried to remove a key during level change !')


def run_level(name):
    print(name)
    load_tmx("res/"+name+"/map.tmx")
    global THE_ELDER_SCROLLS_MANAGER
    THE_ELDER_SCROLLS_MANAGER = cocos.layer.ScrollingManager()
    THE_ELDER_SCROLLS_MANAGER.add(Game(name))
    main_scene = Scene(THE_ELDER_SCROLLS_MANAGER)
    director.run(main_scene)


if __name__ == '__main__':
    director.init(
        caption="PyCon",
        width=800,
        height=600,
        resizable=True,
        autoscale=True
    )
    #setting up the map
    run_level("level01")
