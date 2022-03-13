import pygame

def display_text(screen, text, x, y, size=10, color=(255, 255, 255)):
    text_base_font = pygame.font.SysFont('comicsansms', size)
    text_surface = text_base_font.render(str(text), True, color)

    screen.blit(text_surface, (x, y))

class Button:

    BACKGROUND_COLOR = (100, 255, 100)
    PUSHED_BACKGROUND_COLOR = (100, 200, 100)
    EDGE_COLOR = (50, 200, 50)
    TEXT_COLOR = (100, 100, 0)
    INACTIVE_TEXT_COLOR = (200, 200, 200)

    def __init__(self, x, y, text, size=20):
        self.screen = pygame.display.get_surface()

        self.x = x
        self.y = y
        self.text = text

        base_font = pygame.font.SysFont('arialblack', int(size))
        self.text_surface = base_font.render(str(text), True, self.TEXT_COLOR)
        self.width = self.text_surface.get_width() * 1.4
        self.height = self.text_surface.get_height() * 1.4
        self.bg_surface = pygame.Surface((self.width, self.height))
        self.bg_surface2 = pygame.Surface((self.width, self.height + 3))
        self.rect = self.bg_surface.get_rect(topleft=(self.x, self.y))

        self.clicked = False

        self.history = []

        self.active = True

    def draw(self):

        if self.clicked:
            self.bg_surface.fill(self.EDGE_COLOR)
        else:
            if self.active: color = self.BACKGROUND_COLOR
            else: color = self.INACTIVE_TEXT_COLOR
            self.bg_surface.fill(color)
            self.bg_surface2.fill(self.PUSHED_BACKGROUND_COLOR)

        if not self.clicked:
            self.screen.blit(self.bg_surface2, self.rect)

        self.screen.blit(self.bg_surface, self.rect)
        self.screen.blit(self.text_surface, (self.rect[0] + self.width/2 - self.text_surface.get_width()/2,
                                             self.rect[1] + self.height/2 - self.text_surface.get_height()/2))


    def interact(self):

        if self.active:

            mouse_pos = pygame.mouse.get_pos()

            pressed = pygame.mouse.get_pressed()[0]

            self.rect.x = self.x
            self.rect.y = self.y

            self.clicked = False

            if pressed:
                if self.rect.collidepoint(*mouse_pos):
                    self.clicked = True
                    self.rect.y += 3


    def check_released(self, must_be_in=True):
        if not self.active:
            return False
        if must_be_in:
            return self.history == [True, False] and self.rect.collidepoint(*pygame.mouse.get_pos())
        else:
            return self.history == [True, False]


    def update(self):
        self.interact()
        self.draw()

        self.history.append(self.clicked)

        if len(self.history) >= 2:
            self.history = self.history[-2:]

