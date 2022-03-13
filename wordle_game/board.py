import pygame

import math
import random
import string

from .tools import Button, display_text
from .utils import load_words, get_carac_count, init_carac_count

all_letters = list(string.ascii_lowercase + string.ascii_uppercase)

ALL_WORDS = load_words()

class Board:

    OFFSET = 10

    def __init__(self, number_letters=5):
        self.screen = pygame.display.get_surface()
        self.max_try = 6
        self.restart_button = Button(100, 50, "Restart", size=20)

        self.len_word_buttons = []

        for i in range(4, 12):
            number = str(i)
            if len(number) == 1:
                number = " " + number
            self.len_word_buttons.append(Button(130 + i * 50, 50, number, size=15))

        self.give_up_button = Button(800, 50, "Give up", size=20)

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

        self.words = ALL_WORDS[number_letters]['all_words']
        self.common_words = ALL_WORDS[number_letters]['common_words']
        self.word_to_guess = random.choice(self.common_words)

        #print(self.word_to_guess)

        self.check_animating = False
        self.animation_indice = 0
        self.animation_frame = 0
        self.max_animation_frame = 10
        self.carac_counts = init_carac_count()

        self.playing = True
        self.win = False

        self.subtiles = {l: SubTile(pos=(20 + i*37, 550), letter=l) for i, l in enumerate(list(string.ascii_uppercase))}


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
                                self.win = True
                                self.playing = False

                            if self.current_try >= self.max_try:
                                if word == self.word_to_guess:
                                    self.win = True
                                    self.playing = False
                                else:
                                    #print(f"You lose: {self.word_to_guess}")
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
                if self.animation_indice == 0:
                    word = "".join(tile.letter for tile in self.board[self.current_try - 1])
                    self.carac_counts = get_carac_count(word, self.word_to_guess)
                tile = self.board[self.current_try - 1][self.animation_indice]
                if tile.letter == self.word_to_guess[self.animation_indice]:
                    tile.set_target_color(Tile.GREEN)
                    self.subtiles[tile.letter].set_target_color(Tile.GREEN)

                elif self.carac_counts[tile.letter]:
                    tile.set_target_color(Tile.ORANGE)
                    self.carac_counts[tile.letter] -= 1
                    if self.subtiles[tile.letter].target_color != Tile.GREEN:
                        self.subtiles[tile.letter].set_target_color(Tile.ORANGE)

                pygame.draw.rect(self.screen, color="yellow", rect=tile.surf.get_rect(topleft=tile.pos), width=3)

            self.animation_frame += 1
            if self.animation_frame > self.max_animation_frame:
                self.animation_frame = 0
                self.animation_indice += 1
                if self.animation_indice == self.number_letters:
                    self.animation_indice = 0
                    self.check_animating = False
                    self.carac_counts = init_carac_count()


    def display_infos(self):
        if not self.playing:
            if self.win:
                message = f"You win: {self.word_to_guess}"
            else:
                message = f"You lose: {self.word_to_guess}"
            display_text(self.screen, message, 20, 500, size=30)

    def get_word_current_try(self):
        word = ""
        for tile in self.board[self.current_try]:
            word += tile.letter

        return word

    def update_tiles(self):
        for row in self.board:
            for tile in row:
                tile.update()

        for subtile in self.subtiles.values():
            subtile.update()

    def update_buttons(self):
        self.restart_button.update()

        for b in self.len_word_buttons:
            b.update()

        self.give_up_button.update()

    def check_buttons(self):
        if self.restart_button.check_released():
            self.init(number_letters=self.number_letters)

        for b in self.len_word_buttons:
            if b.check_released():
                number = int(b.text.strip())
                if number != self.number_letters or not self.playing:
                    self.init(number_letters=number)

        if not self.playing:
            self.give_up_button.active = False
        else:
            self.give_up_button.active = True

        if self.give_up_button.check_released():
            self.playing = False
            message = f"You lose: {self.word_to_guess}"
            display_text(self.screen, message, 20, 500, size=30)

    def update(self, all_events):
        self.check_buttons()
        self.update_buttons()
        self.input(all_events)
        self.update_tiles()
        self.word_check_animation()
        self.display_infos()

class Tile:
    GREY = (150, 150, 150)
    GREEN = (150, 250, 150)
    ORANGE = (200, 200, 100)

    TILE_SIZE = 50
    CARAC_SIZE = 30

    def __init__(self, pos, letter=""):
        self.screen = pygame.display.get_surface()
        self.pos = pos
        self.letter = letter
        self.color = self.GREY
        self.target_color = self.color
        self.font = pygame.font.SysFont('comicsans', size=self.CARAC_SIZE)
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

class SubTile(Tile):
    TILE_SIZE = 30
    CARAC_SIZE = 20
