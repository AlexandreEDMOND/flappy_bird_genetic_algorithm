import pygame
from flappy import *
from obstacles import *

class Game:

    def __init__(self):
        self.w = 600
        self.h = 600
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.flappy = Flappy(150, 300)
        self.list_obstacles = []
        self.next_obstacle = 1000
        self.time_between_obstacle = 3000
    
    def add_obstacle(self):
        self.list_obstacles.append(Obstacle(self.w, 300))
        self.next_obstacle += self.time_between_obstacle

    def delete_obstacle(self):
        for obstacle in self.list_obstacles:
            if obstacle.x <= 0:
                self.list_obstacles.remove(obstacle)
                print(len(self.list_obstacles))
        

    def colision_elements(self):
        # Détection si le flappy touche le sol ou le haut
        if self.flappy.y <= 0 or self.flappy.y >= self.h - self.flappy.width:
            return 1
        return 0

    def affichage_elements(self):
        pygame.draw.rect(self.screen, (200, 0, 0), pygame.Rect(self.flappy.x, self.flappy.y, self.flappy.width, self.flappy.width))

        for obstacle in self.list_obstacles:
            pygame.draw.rect(self.screen, (0, 200, 0), pygame.Rect(obstacle.x - obstacle.width, 0, obstacle.width, obstacle.y - obstacle.width_center))
            pygame.draw.rect(self.screen, (0, 200, 0), pygame.Rect(obstacle.x - obstacle.width, obstacle.y + obstacle.width_center, obstacle.width, obstacle.y - obstacle.width_center))

    def actualise_elements(self):
        self.flappy.decrease_speed()
        self.flappy.actualise_position()

        for obstacle in self.list_obstacles:
            obstacle.actualise_position()

        if pygame.time.get_ticks() > self.next_obstacle:
            self.add_obstacle()

    def main_loop(self):
        pygame.display.set_caption('Flappy Bird')
        pygame.init()

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN: 
                    # Récupérer les touches enfoncées
                    if event.key == pygame.K_SPACE:
                        self.flappy.make_jump()
            
            self.screen.fill((50, 0, 0))

            self.actualise_elements()
            self.delete_obstacle()
            if self.colision_elements() == 1:
                running = False
            self.affichage_elements()

            pygame.display.flip()