import pygame.font
from pygame.sprite import Group
from sanitizer import Sanitizer


class ScoreBoard():
    def __init__(self, st_settings, screen, stats):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.st_settings = st_settings
        self.stats = stats

        # font settings
        self.font_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score and highscore and level
        self.prep_score()
        self.prep_highscore()
        self.prep_level()
        self.prep_bottles()

    def prep_score(self):
        # round the score to the nearest 10s value
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.font_color, self.st_settings.bg_color)

        # display the score on the top right of the screen
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right
        # place the image 20 pixels from the top
        self.score_image_rect.top = 5

    def show_score(self):
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        # draw bottles on the screen - call draw on the group
        self.bottle.draw(self.screen)

    def prep_highscore(self):
        """turn the highscore to an image """
        highscore = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(highscore)
        self.high_score_image = self.font.render(
            high_score_str, True, self.font_color, self.st_settings.bg_color)

        # center the high score at the top of the screen
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = self.screen_rect.top

    def prep_level(self):
        self.level_image = self.font.render(
            str(self.stats.level), True, self.font_color, self.st_settings.bg_color)

        # positions the level rect
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_image_rect.right
        self.level_image_rect.top = self.score_image_rect.bottom + 10

    def prep_bottles(self):
        """Show how many bottles are left"""
        self.bottle = Group()
        for bottle_number in range(self.stats.bottle_left):
            bottle = Sanitizer(self.st_settings, self.screen)
            bottle.rect.x = 10 + bottle_number * bottle.rect.width
            bottle.rect.y = 10
            self.bottle.add(bottle)
