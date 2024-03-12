import pygame

class Obstacle:

    def __init__(self, x, y, y_max, width_wall, width_center):
        self.x = x
        self.y = y
        self.y_max = y_max
        self.width = width_wall
        self.width_center = width_center
        self.speed = 0.1
    
    def get_rect_top(self):
        return pygame.Rect(self.x - self.width, 0, self.width, self.y - self.width_center)
    
    def get_rect_down(self):
        return pygame.Rect(self.x - self.width, self.y + self.width_center, self.width, self.y_max - self.y - self.width_center)

    def actualise_position(self):
        self.x -= self.speed