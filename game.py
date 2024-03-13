import pygame
from flappy import *
from obstacles import *
from random import randint

class Game:

    def __init__(self, affichage_pygame):
        self.w = 600
        self.h = 600
        if affichage_pygame:
            self.screen = pygame.display.set_mode((self.w, self.h))
        self.flappy = Flappy(150, 300)
        self.list_obstacles = []
        self.frame = 0
        self.next_obstacle = 3000
        self.time_between_obstacle = 5000
        self.width_wall = 30
        self.width_center = 100
        self.affichage_pygame = affichage_pygame
    
    def decision_network(self):
        tenser_entree = torch.tensor(self.get_info_network(), dtype=torch.float32)
        output = self.flappy.network(tenser_entree)
        return output.argmax().item()
    
    def get_info_network(self):
        
        dist_next_obstacle = self.w
        diff_tuyau_top = self.h
        diff_tuyau_down = self.h
        for obstacle in self.list_obstacles:
            # Calcul distance jusqu'au prochain tuyau
            distance = obstacle.x - self.flappy.x

            if distance > 0 and distance < dist_next_obstacle:
                dist_next_obstacle = distance
                # Calcul différence avec les tuyaux
                diff_tuyau_top = self.flappy.y - obstacle.y + obstacle.width_center
                diff_tuyau_down = obstacle.y + obstacle.width_center - self.flappy.y

        # Vitesse de flappy
        flappy_speed = self.flappy.speed

        # Hauteur flappy
        flappy_position = self.flappy.y

        data_network = [dist_next_obstacle, diff_tuyau_top, diff_tuyau_down, flappy_speed, flappy_position]
        #print(data_network)
        return data_network

    def add_obstacle(self):
        self.list_obstacles.append(Obstacle(self.w, randint(self.width_center + 10, self.h - self.width_center + 10), self.h, self.width_wall, self.width_center))
        self.next_obstacle += self.time_between_obstacle

    def delete_obstacle(self):
        for obstacle in self.list_obstacles:
            if obstacle.x <= 0:
                self.list_obstacles.remove(obstacle)
        

    def colision_elements(self):
        # Détection si le flappy touche le sol ou le haut
        if self.flappy.y <= 0 or self.flappy.y >= self.h - self.flappy.width:
            return 1
        
        # Détection de colision entre floppy et les obstacles
        for obstacle in self.list_obstacles:
            if pygame.Rect.colliderect(self.flappy.get_rect(), obstacle.get_rect_top()) == True:
                return 1
            if pygame.Rect.colliderect(self.flappy.get_rect(), obstacle.get_rect_down()) == True:
                return 1
            
        return 0

    def affichage_elements(self):
        pygame.draw.rect(self.screen, (200, 0, 0), self.flappy.get_rect())

        for obstacle in self.list_obstacles:
            pygame.draw.rect(self.screen, (0, 200, 0), obstacle.get_rect_top())
            pygame.draw.rect(self.screen, (0, 200, 0), obstacle.get_rect_down())

    def actualise_elements(self):
        self.flappy.decrease_speed()
        self.flappy.actualise_position()

        for obstacle in self.list_obstacles:
            obstacle.actualise_position()

        if self.frame > self.next_obstacle:
            self.add_obstacle()

    def calcul_score(self):
        return self.frame

    def main_loop(self):

        if self.affichage_pygame:
            pygame.display.set_caption('Flappy Bird')
            pygame.init()

        running = True
        while running:

            if self.affichage_pygame:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN: 
                        # Récupérer les touches enfoncées
                        if event.key == pygame.K_SPACE:
                            self.flappy.make_jump()
            
                self.screen.fill((50, 0, 0))

            #self.get_info_network()
            if self.decision_network() == 1:
                self.flappy.make_jump()
            self.actualise_elements()
            self.delete_obstacle()
            if self.colision_elements() == 1:
                running = False

            if self.affichage_pygame:
                self.affichage_elements()

                pygame.display.flip()
            self.frame += 1
        
        score = self.calcul_score()
        return score