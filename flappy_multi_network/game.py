import pygame
from flappy import *
from obstacles import *
from random import randint

class Game:

    def __init__(self, affichage_pygame, nmbre_flappy):
        self.w = 600
        self.h = 600
        if affichage_pygame:
            self.screen = pygame.display.set_mode((self.w, self.h))
        self.list_flappy = [Flappy(150, 300 + randint(-50, 50)) for _ in range(nmbre_flappy)]
        self.list_obstacles = []
        self.frame = 0
        self.next_obstacle = 3000
        self.time_between_obstacle = 5000
        self.width_wall = 30
        self.width_center = 100
        self.affichage_pygame = affichage_pygame
    
    def make_flappy_move(self):
        for flappy in self.list_flappy:
            if flappy.alive:
                if self.decision_network(flappy) == 1:
                    flappy.make_jump()

    def decision_network(self, flappy):
        tenser_entree = torch.tensor(self.get_info_network(flappy), dtype=torch.float32)
        output = flappy.network(tenser_entree)
        return output.argmax().item()
    
    def get_info_network(self, flappy):
        
        dist_next_obstacle = self.w
        diff_tuyau_top = self.h
        diff_tuyau_down = self.h
        for obstacle in self.list_obstacles:
            # Calcul distance jusqu'au prochain tuyau
            distance = obstacle.x - flappy.x

            if distance > 0 and distance < dist_next_obstacle:
                dist_next_obstacle = distance
                # Calcul différence avec les tuyaux
                diff_tuyau_top = flappy.y - obstacle.y + obstacle.width_center
                diff_tuyau_down = obstacle.y + obstacle.width_center - flappy.y

        # Vitesse de flappy
        flappy_speed = flappy.speed

        # Hauteur flappy
        flappy_position = flappy.y

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
        for flappy in self.list_flappy:
            #Si le flappy est vivant
            if flappy.alive:
                # Détection si le flappy touche le sol ou le haut
                if flappy.y <= 0 or flappy.y >= self.h - flappy.width:
                    # On tue le flappy
                    flappy.alive = False
                    flappy.score = self.frame
                
                # Détection de colision entre floppy et les obstacles
                for obstacle in self.list_obstacles:
                    if pygame.Rect.colliderect(flappy.get_rect(), obstacle.get_rect_top()) == True or pygame.Rect.colliderect(flappy.get_rect(), obstacle.get_rect_down()) == True:
                        # On tue le flappy
                        flappy.alive = False
                        flappy.score = self.frame
                        break

    def affichage_elements(self):

        # On affiche les flappy qui sont en vie
        for flappy in self.list_flappy:
            if flappy.alive:
                pygame.draw.rect(self.screen, (200, 0, 0), flappy.get_rect())

        # On affiche les obstacles
        for obstacle in self.list_obstacles:
            pygame.draw.rect(self.screen, (0, 200, 0), obstacle.get_rect_top())
            pygame.draw.rect(self.screen, (0, 200, 0), obstacle.get_rect_down())

    def actualise_elements(self):

        # On fait bouger les flappy qui sont en vie
        for flappy in self.list_flappy:
            if flappy.alive:
                flappy.decrease_speed()
                flappy.actualise_position()

        for obstacle in self.list_obstacles:
            obstacle.actualise_position()

        if self.frame > self.next_obstacle:
            self.add_obstacle()

    def calcul_score(self):
        score = [flappy.score for flappy in self.list_flappy]
        return score

    def end_game(self):
        for flappy in self.list_flappy:
            if flappy.alive:
                return False
        return True

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
            
                self.screen.fill((50, 0, 0))

            #self.get_info_network()
            self.make_flappy_move()
            self.actualise_elements()
            self.delete_obstacle()
            self.colision_elements()

            if self.end_game():
                running = False

            if self.affichage_pygame:
                self.affichage_elements()

                pygame.display.flip()
            self.frame += 1
        
        score = self.calcul_score()
        return score