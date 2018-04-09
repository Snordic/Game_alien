# alien_invasion.py

import sys
import pygame
from setting import Settings
from ship import Player1
import game_function as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bullet import Bullet


def run_game():
    pygame.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode((
        ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Alien Invasion")
    player1 = Player1(ai_setting, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_setting, screen, player1, aliens)
    stats = GameStats(ai_setting)
    gf.load_high_score(ai_setting, stats)
    sb = Scoreboard(ai_setting, screen, stats)
    play_button = Button(ai_setting, screen, 'Play')

    # Запуск основного цикла
    while True:
        gf.check_events(ai_setting, screen, stats, sb, player1, aliens, bullets, play_button)
        gf.update_screen(ai_setting, screen, sb, stats, player1, aliens, bullets, play_button)
        if stats.game_active:
            player1.update()
            gf.update_bullets(ai_setting, screen, stats, sb, player1, aliens, bullets)
            gf.update_aliens(ai_setting, stats, sb, screen, player1, aliens, bullets)


run_game()

