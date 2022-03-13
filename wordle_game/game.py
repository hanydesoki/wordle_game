import pygame
import sys

from .board import Board

class Game:

    BACKGROUND_COLOR = (50, 50, 50)

    def __init__(self):
        pygame.init()

        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption('Wordle')
        self.clock = pygame.time.Clock()

        self.background = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill(self.BACKGROUND_COLOR)

        self.board = Board(5)


    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def run(self):
        while True:
            all_events = pygame.event.get()
            for event in all_events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw_background()
            self.board.update(all_events)

            pygame.display.update()
            self.clock.tick(60)