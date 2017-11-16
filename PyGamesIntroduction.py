import sys
import pygame


class GUI():
    def __init__(self, table):
        pygame.init()
        self.table = table
        size = width, height = 720, 720
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(size)

    def render(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.black)
            for y in range(len(self.table)):
                for x in range(len(self.table[0])):
                    if self.table[y][x] is not '.':
                        color = (255, 0, 0)
                        border = 0
                    else:
                        color = (255, 255, 255)
                        border = 1
                    pygame.draw.rect(self.screen, color,
                                     (x * 64, y * 64, 64, 64), border)
            pygame.display.flip()

    def update(self, table):
        self.table = table
