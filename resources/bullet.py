import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class to manage the bullets from the sanitizer"""

    def __init__(self, st_settings, screen, sanit):
        """Create a bullet object at the sanitizer's current position."""
        super().__init__()
        self.screen = screen

        # create a bullet rect at position (0,0) and then correct it's position
        self.rect = pygame.Rect(0, 0, st_settings.bullet_width, st_settings.bullet_height)
        self.rect.centerx = sanit.rect.centerx
        self.rect.top = sanit.rect.top

        # store bullet position as a decimal value
        self.y = float(self.rect.y)
        self.color = st_settings.bullet_color
        self.speed_factor = st_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        # update the rect positon
        self.rect.y = self.y

    def draw_bullet(self):
        """draw bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
