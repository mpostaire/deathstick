import cocos


class AdStop(cocos.sprite.Sprite):
    def __init__(self, cursor):
        super(AdStop, self).__init__("res/adstop.png", opacity=100)
        self.charging_time = 2.0  # time this power needs to recharge (in seconds)
        self.elapsed_time = 0.0  # time since last power deactivation (in seconds)
        self.cursor = cursor
        self.set_hud_position()

    def act(self, delta):
        if self.cursor.bullettime:
            self.elapsed_time += delta * 2  # counteract bullet time if activated
        else:
            self.elapsed_time += delta
        if self.elapsed_time >= self.charging_time:  # if this power available, highlight it
            self.opacity = 255
        if self.cursor.shielded:
            self.set_cursor_position()
            self.rotation = self.cursor.rotation
        else:
            self.set_hud_position()

    def activate(self):
        if self.elapsed_time >= self.charging_time:
            self.cursor.shielded = True
            self.rotation = self.cursor.rotation
            self.set_cursor_position()

    def reset(self):
        self.cursor.shielded = False
        self.opacity = 100
        self.rotation = 0
        self.elapsed_time = 0

    def set_hud_position(self):
        window_size = cocos.director.director.get_window_size()
        self.position = (self.cursor.position[0] - window_size[0] / 2 + 20,
                         self.cursor.position[1] + window_size[1] / 2 - 20)

    def set_cursor_position(self):
        self.position = self.cursor.position
        self.opacity = 100
