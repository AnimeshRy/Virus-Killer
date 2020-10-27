import pygame
from pygame.sprite import Sprite


class Sanitizer(Sprite):
    
    def __init__(self, st_settings, screen):
        """Initialize the ship and it's starting position"""

        self.screen = screen
        self.st_settings = st_settings
        super().__init__()

        # load image and get it's rect
        self.image = pygame.image.load("./media/sanitizer_image.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # movement flag for right side and left side
        self.moving_right = False
        self.moving_left = False

        # aligning the image rect with the screen rect using the x attribute
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store the decimal value of the new speed factor
        self.center = float(self.rect.centerx)

    def update_movement(self):
        """update obj movement when flag activates
        - flag goes on and self.rect.right gives the x attribute of the sanit's rect and it should be less than than screen's rect and then it moves right
        - we could replace self.screen_rect.right with 1200
        """

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.st_settings.sanit_speed_factor

        # flag goes on and self.rect.left gives the x attribute of sanit's rect and is should be more than 0 as the box starts from 0x0 and to go less than 0 would be going out of the screen
        # we could replace self.screen_rect.left with 0

        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.st_settings.sanit_speed_factor

        # update the screen rect too
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at the current location specified by the rect"""
        self.screen.blit(self.image, self.rect)

    def center_bottle(self):
        self.center = self.screen_rect.centerx
