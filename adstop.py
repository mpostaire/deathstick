import cocos


class AdStop(cocos.sprite.Sprite):
    def __init__(self, image, position, cursor):
        super(AdStop, self).__init__(image, opacity=100)
        self.position = position
        self.charging_time = 2.0
        self.elapsed_time = 0.0
        self.cursor = cursor

    def act(self, delta):
        self.elapsed_time += delta
        if self.elapsed_time >= self.charging_time:
            self.opacity = 255
        if self.cursor.shielded:
            self.setCursorPosition()
        else:
            self.setHudPosition()

    def activate(self):
        if self.elapsed_time >= self.charging_time:
            self.cursor.shielded = True
            self.setCursorPosition()

    def reset(self):
        self.cursor.shielded = False
        self.opacity = 100
        self.elapsed_time = 0

    def setHudPosition(self):
        window_size = cocos.director.director.get_window_size()
        self.position = (self.cursor.position[0] - window_size[0] / 2 + 20,
                         self.cursor.position[1] + window_size[1] / 2 - 20)

    def setCursorPosition(self):
        self.position = self.cursor.position
        self.opacity = 100
