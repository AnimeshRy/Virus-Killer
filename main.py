import pygame
from settings import Settings
from sanitizer import Sanitizer
import game_functions as gf
from pygame.sprite import Group
from virus import Virus
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    # initialize background setting needed for pygame and make the first surface called screen and set the window size
    pygame.init()
    # creating instance of the screen settings
    st_settings = Settings()

    screen = pygame.display.set_mode(
        (st_settings.screen_width, st_settings.screen_height))
    pygame.display.set_caption("Go Corona")

    # adding the sanitizer bottle starting at the bottom center
    sanit = Sanitizer(st_settings, screen)
    # make a group to store bullets in
    bullets = Group()
    # make a group of virus
    viruses = Group()
    # create fleet of aliens
    gf.create_fleet(st_settings, screen, sanit, viruses)
    # create instance to store game stats
    stats = GameStats(st_settings)
    # make a instance to save the score of the game
    sb = ScoreBoard(st_settings, screen, stats)
    # make the play button
    play_button = Button(st_settings, screen, "Play / Q:Quit")
    # main loop for the game
    while True:
        # watch for keyboard and mouse movements
        gf.check_events(st_settings, screen, stats,
                        play_button, sb, sanit, viruses, bullets)
        if stats.game_active:
            # update bottle's movement
            sanit.update_movement()
            # update all the sprites in the Group 'bullets'
            gf.bullet_update(st_settings, screen, sanit,
                             sb, stats, viruses, bullets)
            # update screen for all the screens
            gf.update_virus(st_settings, stats, screen, sb,
                            sanit, viruses, bullets)
        gf.update_screen(st_settings, screen, stats, sb, sanit,
                         viruses, bullets, play_button)


run_game()
