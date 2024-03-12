

class Obstacle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.width_center = 100
        self.speed = 0.1
    
    def actualise_position(self):
        self.x -= self.speed