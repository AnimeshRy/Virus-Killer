class Settings():
    """A class to store all settings for battleship"""

    def __init__(self):
        """initializing the game setting"""
        
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.bottle_limit = 3

        # bullet settings
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (0, 255, 0)

        # keeping a bullet limit to keep the game fast
        self.bullet_allowed = 5

        # virus settings
        self.fleet_drop_speed = 10
        # fleet direction right = 1 and left = -1

        # game settings
        self.speedup_scale = 1.1
        
        # how quickly the virus point value changes
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """dynamic settings that will change throughout the game"""

        # initial settings when the game starts
        self.sanit_speed_factor = 2
        self.bullet_speed_factor = 2.5
        self.virus_speed_factor = 1.5

        # fleet direction right = 1 and left = -1
        self.fleet_direction = 1

        # virus hit points
        self.virus_hitpoint = 10

    def increase_speed(self):
        """increase speed of variables in this method and virus point values"""

        self.sanit_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.virus_speed_factor *= self.speedup_scale
        self.virus_hitpoint = int(self.virus_hitpoint * self.score_scale)
