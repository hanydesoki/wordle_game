import pygame
import math

class Board:

    OFFSET = 10

    def __init__(self, number_letters=5):
        self.screen = pygame.display.get_surface()
        self.number_letters = number_letters
        self.x_min = self.screen.get_width() // 2 - (Tile.TILE_SIZE + self.OFFSET) * self.number_letters // 2
        self.y_min = 150

        self.max_try = 6

        self.init()

    def init(self):
        self.board = []
        for i in range(self.max_try):
            self.board.append([Tile((self.x_min + j * (Tile.TILE_SIZE + self.OFFSET),
                                     self.y_min + i * (Tile.TILE_SIZE + self.OFFSET))) for j in range(self.number_letters)])

        #self.board[0][0].set_target_color(Tile.GREEN)

        self.current_try = 0
        self.letter_indice = 0

    def input(self, all_events):
        for event in all_events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    pass

                else:
                    key_pressed = event.unicode


    def update_tiles(self):
        for row in self.board:
            for tile in row:
                tile.update()

    def update(self, all_events):
        self.input(all_events)
        self.update_tiles()



class Tile:
    GREY = (150, 150, 150)
    GREEN = (150, 254, 150)
    ORANGE = (200, 200, 100)

    TILE_SIZE = 50

    def __init__(self, pos, letter=""):
        self.screen = pygame.display.get_surface()
        self.pos = pos
        self.letter = letter
        self.color = self.GREY
        self.target_color = self.color
        self.font = pygame.font.SysFont('comicsans', size=30)
        self.surf = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE))
        self.surf.fill(self.color)

    def draw(self):
        self.screen.blit(self.surf, self.pos)
        self.text_surface = self.font.render(self.letter, True, "white")
        text_pos = (self.pos[0] + self.surf.get_width()//2 - self.text_surface.get_width()//2,
                    self.pos[1] + self.surf.get_height()//2 - self.text_surface.get_height()//2)

        self.screen.blit(self.text_surface, text_pos)

    def set_target_color(self, color):
        self.target_color = color


    def update_color(self):
        if self.color != self.target_color:
            c = list(self.color)
            for i in range(3):
                diff = c[i] - self.target_color[i]
                if diff:
                    c[i] -= 4 * math.copysign(1, diff)

            self.color = tuple(c)
            self.surf.fill(self.color)

    def update(self):
        self.update_color()
        self.draw()