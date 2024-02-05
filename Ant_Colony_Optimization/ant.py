import pygame
import random as rand

class Ant():
    def __init__(self, angle = -90):
        self.image = pygame.image.load("images/ant.png")
        self.surface = pygame.transform.scale(self.image, (25, 25))
        self.surface = pygame.transform.rotate(self.surface, angle)
        self.is_generated = False
        self.position_node = 0
        self.ant_position = (0, 0)
        self.path = None
        self.did_finish = False
        self.did_update_pheromone = False
        self.rect = self.image.get_rect(center = self.ant_position)
        self.pheromone_particles = []

    def __getall__(self):
        return self.surface, self.is_generated, self.position_node, self.ant_position, self.path, self.did_finish, self.did_update_pheromone
    
    def move(self):
        self.rect = self.surface.get_rect(center = self.ant_position)
        for pheromone_particle in self.pheromone_particles:
            pheromone_particle[0][0] -= 2
            pheromone_particle[0][1] += pheromone_particle[1]

        color = pygame.Color(0, rand.randrange(200, 255), 0)
        pheromone_particle = [list(self.rect.midleft), rand.uniform(-1, 1), color]
        self.pheromone_particles.append(pheromone_particle)

        if len(self.pheromone_particles) > 30:
            self.pheromone_particles.pop(0)
        self.rect.centerx += 1
        
    def draw(self, screen):
        self.move()
        for j, pheromone_particle in enumerate(self.pheromone_particles):
            pygame.draw.circle(screen, pheromone_particle[2], pheromone_particle[0], (j // 15))
        screen.blit(self.surface, self.ant_position)

def setAnt(angle = -90):
    ant = Ant(angle)
    return ant

def setAntPopulationSurfaces(population_size):
    ant_surfaces = []
    for i in range(population_size):
        ant_surfaces.append(setAnt())
    return ant_surfaces