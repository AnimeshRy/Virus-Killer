class GameStats():
    def __init__(self, st_settings):
        """class for recording the game stats for the game"""
        self.st_settings = st_settings
        # resets the game stats
        self.reset_stats()
        # start the game using the button
        self.game_active = False
        # high scores should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that change during the game"""
        self.bottle_left = self.st_settings.bottle_limit
        self.score = 0
        self.level = 1
