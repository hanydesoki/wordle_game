import pygame

import math
import string
import random

from .tools import Button

all_letters = list(string.ascii_lowercase + string.ascii_uppercase)

def check_valid_word(word):
    for caracter in word:
        if caracter not in all_letters:
            return False

    return True

def load_words(number_letters):
    with open('liste_francais.txt', 'r') as f:
        all_words = f.readlines()

    result = []

    for word in all_words:
        w = word.replace('\n', '')
        if check_valid_word(w) and len(w) == number_letters:
            result.append(w.upper())

    return result




class Board:

    OFFSET = 10

    def __init__(self, number_letters=5):
        self.screen = pygame.display.get_surface()
        self.max_try = 6
        self.restart_button = Button(100, 50, "Restart", size=20)

        self.init(number_letters)

    def init(self, number_letters):
        self.number_letters = number_letters
        self.x_min = self.screen.get_width() // 2 - (Tile.TILE_SIZE + self.OFFSET) * self.number_letters // 2
        self.y_min = 150

        self.board = []
        for i in range(self.max_try):
            self.board.append([Tile((self.x_min + j * (Tile.TILE_SIZE + self.OFFSET),
                                     self.y_min + i * (Tile.TILE_SIZE + self.OFFSET))) for j in range(self.number_letters)])
        #self.board[0][0].set_target_color(Tile.GREEN)

        self.current_try = 0
        self.letter_indice = 0

        self.words = load_words(number_letters)
        self.word_to_guess = random.choice(self.words)

        #print(self.word_to_guess)
        self.check_animating = False
        self.animation_indice = 0
        self.animation_frame = 0
        self.max_animation_frame = 10

        self.playing = True


    def input(self, all_events):
        if not self.check_animating and self.playing:
            for event in all_events:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN and self.letter_indice == self.number_letters:
                        word = self.get_word_current_try()
                        if word in self.words:
                            self.check_animating = True
                            self.current_try += 1
                            self.letter_indice = 0
                            if word == self.word_to_guess:
                                print("You win!")
                                self.playing = False

                            if self.current_try >= self.max_try:
                                if word == self.word_to_guess:
                                    print("You win!")
                                    self.playing = False
                                else:
                                    print(f"You lose: {self.word_to_guess}")
                                    self.playing = False

                    elif event.key == pygame.K_BACKSPACE and self.letter_indice != 0:
                        self.board[self.current_try][self.letter_indice - 1].letter = ""
                        self.letter_indice -= 1

                    else:
                        if self.letter_indice < self.number_letters:
                            key_pressed = event.unicode
                            if key_pressed in all_letters:
                                self.board[self.current_try][self.letter_indice].letter = key_pressed.upper()
                                self.letter_indice += 1


    def word_check_animation(self):
        if self.check_animating:
            if self.animation_frame == 0:
                tile = self.board[self.current_try - 1][self.animation_indice]
                if tile.letter == self.word_to_guess[self.animation_indice]:
                    tile.set_target_color(Tile.GREEN)

                elif tile.letter in self.word_to_guess:
                    tile.set_target_color(Tile.ORANGE)

                pygame.draw.rect(self.screen, color="yellow", rect=tile.surf.get_rect(topleft=tile.pos), width=3)

            self.animation_frame += 1
            if self.animation_frame > self.max_animation_frame:
                self.animation_frame = 0
                self.animation_indice += 1
                if self.animation_indice == self.number_letters:
                    self.animation_indice = 0
                    self.check_animating = False




    def get_word_current_try(self):
        word = ""
        for tile in self.board[self.current_try]:
            word += tile.letter

        return word

    def update_tiles(self):
        for row in self.board:
            for tile in row:
                tile.update()

    def update_buttons(self):
        self.restart_button.update()

    def check_buttons(self):
        if self.restart_button.check_released():
            self.init(number_letters=self.number_letters)

    def update(self, all_events):
        self.check_buttons()
        self.update_buttons()
        self.input(all_events)
        self.update_tiles()
        self.word_check_animation()



class Tile:
    GREY = (150, 150, 150)
    GREEN = (150, 250, 150)
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
                    c[i] -= 10 * math.copysign(1, diff)

            self.color = tuple(c)
            self.surf.fill(self.color)

    def update(self):
        self.update_color()
        self.draw()