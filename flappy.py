

class Flappy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.speed = 0
        self.speed_decrease = 0.001
        self.speed_jump = 0.5
    
    def actualise_position(self):
        self.y -= self.speed

    def decrease_speed(self):
        self.speed -= self.speed_decrease
    
    def make_jump(self):
        self.speed = self.speed_jump
    
    