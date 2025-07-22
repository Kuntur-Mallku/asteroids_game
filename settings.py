class Settings:
    """A class to store all settings for the Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_rotation_speed = 2.5  # Degrees per frame

        # # Bullet settings
        self.bullet_speed = 3.5
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)

        # # Alien settings
        # self.alien_speed = 1.0