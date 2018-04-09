# game_function.py

import sys
import pygame
import json
from bullet import Bullet
from alien import Alien
from time import sleep


def check_aliens_bottom(ai_setting, stats, sb, screen, player1, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, sb, screen, player1, aliens, bullets)
            break


def ship_hit(ai_setting, stats, sb, screen, player1, aliens, bullets):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, player1, aliens)
        player1.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_events(ai_setting, screen, stats, sb, player1, aliens, bullets, play_button):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(ai_setting, stats)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(
                    event, ai_setting, screen, player1, bullets)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    save_high_score(ai_setting, stats)
                    sys.exit()
                check_keyup_events(event, player1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_setting, screen, stats, sb, player1, aliens, bullets, play_button, mouse_x, mouse_y)


def save_high_score(ai_setting, stats):
    with open(ai_setting.record, 'w') as f_obj:
        json.dump(stats.high_score, f_obj)


def load_high_score(ai_setting, stats):
    try:
        with open(ai_setting.record) as f_obj:
            stats.high_score = json.load(f_obj)
    except FileNotFoundError:
        with open(ai_setting.record, 'w') as f_obj:
            json.dump(stats.high_score, f_obj)


def check_play_button(ai_setting, screen, stats, sb, player1, aliens, bullets, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        ai_setting.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, player1, aliens)
        player1.center_ship()


def update_screen(ai_setting, screen, sb, stats, player1, alien, bullets, play_button):
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    player1.blitme()
    sb.show_score()
    alien.draw(screen)
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def check_keyup_events(event, player1):
    if event.key == pygame.K_RIGHT:
        player1.moving_right = False
        player1.rect.centerx += 1
    elif event.key == pygame.K_LEFT:
        player1.moving_left = False
        player1.rect.centerx -= 1
    elif event.key == pygame.K_UP:
        player1.moving_up = False
        player1.rect.bottom += 1
    elif event.key == pygame.K_DOWN:
        player1.moving_down = False
        player1.rect.bottom -= 1


def check_keydown_events(event, ai_setting, screen, player1, bullets):
    if event.key == pygame.K_RIGHT:
        player1.moving_right = True
    elif event.key == pygame.K_LEFT:
        player1.moving_left = True
    elif event.key == pygame.K_UP:
        player1.moving_up = True
    elif event.key == pygame.K_DOWN:
        player1.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, player1, bullets)


def update_bullets(ai_setting, screen, stats, sb, player1, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen, stats, sb, player1, aliens, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_setting, screen, stats, sb, player1, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    start_new_level(ai_setting, screen, stats, sb, player1, aliens, bullets)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)


def start_new_level(ai_setting, screen, stats, sb, player1, aliens, bullets):
    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_setting, screen, player1, aliens)


def fire_bullet(ai_setting, screen, player1, bullets):
    if len(bullets) < ai_setting.bullets_allowed:
        new_bullet = Bullet(ai_setting, screen, player1)
        bullets.add(new_bullet)


def create_fleet(ai_setting, screen, player1, aliens):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_setting, alien_width)
    number_rows = get_number_rows(ai_setting, player1.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_setting, alien_width):
    avaible_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(avaible_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_setting, screen, aliens, alien_number, number_rows):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * number_rows
    aliens.add(alien)


def get_number_rows(ai_setting, player1_height, alien_height):
    avaible_space_y = (ai_setting.screen_height - (3 * alien_height) - player1_height)
    number_rows = int(avaible_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_setting, stats, sb, screen, player1, aliens, bullets):
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(player1, aliens):
        ship_hit(ai_setting, stats, sb, screen, player1, aliens, bullets)
    check_aliens_bottom(ai_setting, stats, sb, screen, player1, aliens, bullets)


def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


def change_fleet_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1
