import cocos


class BulletTime(cocos.sprite.Sprite):
    def __init__(self, image, cursor):
        super(BulletTime, self).__init__(image, opacity=100)
        self.cursor = cursor
        self.setHudPosition()
        self.charging_time = 3.0
        self.elapsed_time = 0.0
        self.duration = 1.0

    def act(self, delta):
        self.elapsed_time += delta * 2
        if self.cursor.bullettime and self.elapsed_time >= self.duration:
            self.reset()
        elif not self.cursor.bullettime and self.elapsed_time >= self.charging_time:
            self.opacity = 255
        self.setHudPosition()

    def activate(self):
        if self.elapsed_time >= self.charging_time:
            self.cursor.bullettime = True
            self.elapsed_time = 0
            self.opacity = 100

    def reset(self):
        self.cursor.bullettime = False
        self.opacity = 100
        self.elapsed_time = 0

    def setHudPosition(self):
        window_size = cocos.director.director.get_window_size()
        self.position = (self.cursor.position[0] - window_size[0] / 2 + 20,
                         self.cursor.position[1] + window_size[1] / 2 - 60)
