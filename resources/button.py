import pygame.font

class Button():
    """Class to create buttons for the game"""
    
    def __init__(self, st_settings, screen, msg):

        """ initialize the button attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set the dimension and properties of the button
        self.width = 300
        self.height = 50
        self.button_color = (2, 142, 86)
        self.text_color = (255, 255, 255)

        # none tells to use the default font
        self.font = pygame.font.SysFont(None, 48)

        # building the button's rect object in the center of the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # button needs to be activated only once
        self.activ_button(msg)

    def activ_button(self, msg):
        """Creates image when we render text and then align it in the center"""

        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """print the button onto the screen"""

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
