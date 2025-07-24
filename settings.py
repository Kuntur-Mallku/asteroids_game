class Settings:
    """A class to store all settings for the Asteroids."""

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
        self.bullets_allowed = 3

        # Rock settings
        self.rock_spawn_rate = 120  # Frames between rock spawns (2 seconds at 60 FPS)
        self.max_rocks = 8  # Maximum number of rocks on screen
        
        # Difficulty progression settings
        self.base_rock_speed_min = 0.5  # Minimum speed at start
        self.base_rock_speed_max = 2.0  # Maximum speed at start
        self.difficulty_increase_time = 1800  # Frames (30 seconds at 60 FPS)
        self.speed_multiplier_per_level = 0.3  # How much faster each level
        self.max_difficulty_level = 10  # Maximum difficulty level

        # # Alien settings
        # self.alien_speed = 1.0