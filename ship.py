# ship.py

import pygame
from pygame.sprite import Sprite



class Player1(Sprite):
    def __init__(self, ai_setting, screen):
        super(Player1, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting
        self.image = pygame.image.load('player1.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Место появление
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        # Проверка на нажатие клавиш
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.ship_speed_factor = ai_setting.ship_speed_factor

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.bottom -= self.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
