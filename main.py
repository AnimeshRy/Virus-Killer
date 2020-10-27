import pygame
from resources.settings import Settings
from resources.sanitizer import Sanitizer
from resources import game_functions as gf
from pygame.sprite import Group
from resources.virus import Virus
from resources.game_stats import GameStats
from resources.button import Button
from resources.scoreboard import ScoreBoard


def run_game():
    pygame.init()
    st_settings = Settings()
    screen = pygame.display.set_mode(
        (st_settings.screen_width, st_settings.screen_height))
    
    # FOR Full Screen - 
    # screen = pygame.display.set_mode((st_settings.screen_width, st_settings.screen_height, pygame.FULLSCREEN)
    pygame.display.set_caption("Virus Killer")

    
    sanit = Sanitizer(st_settings, screen)
    bullets = Group()
    viruses = Group()
    gf.create_fleet(st_settings, screen, sanit, viruses)
    stats = GameStats(st_settings)
    sb = ScoreBoard(st_settings, screen, stats)
    play_button = Button(st_settings, screen, "Play / Q:Quit")

    # main loop 
    while True:
        
        gf.check_events(st_settings, screen, stats,
                        play_button, sb, sanit, viruses, bullets)

        if stats.game_active:
            sanit.update_movement()
            gf.bullet_update(st_settings, screen, sanit,sb, stats, viruses, bullets)
            gf.update_virus(st_settings, stats, screen, sb, sanit, viruses, bullets)

        gf.update_screen(st_settings, screen, stats, sb, sanit, viruses, bullets, play_button)


if __name__ == "__main__":
    run_game()
