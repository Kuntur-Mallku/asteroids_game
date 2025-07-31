class Settings:
    """A class to store all settings for the Asteroids."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 20)  # Dark space blue

        # Ship settings
        self.ship_speed = 1.5
        self.ship_rotation_speed = 2.5  # Degrees per frame
        self.ship_lives = 3  # Number of lives the player has

        # # Bullet settings
        self.bullet_speed = 4.5
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (255, 255, 0)  # Bright yellow for visibility against dark space
        self.bullets_allowed = 5

        # Rock settings
        self.rock_spawn_rate = 120  # Frames between rock spawns (2 seconds at 60 FPS)
        self.max_rocks = 10  # Maximum number of rocks on screen (increased 25% from 8)
        
        # Scoring settings
        self.rock_escaped_penalty = -5  # Points lost when a rock escapes
        
        # Rock appearance settings
        # Rock1 scaling (normal size range)
        self.rock1_scale_min = 0.5  # Minimum scale factor (60% of original)
        self.rock1_scale_max = 1.3  # Maximum scale factor (140% of original)
        
        # Rock2 scaling (smaller size range since rock2 is too big)
        self.rock2_scale_min = 0.2  # Minimum scale factor (40% of original)
        self.rock2_scale_max = 0.4  # Maximum scale factor (80% of original)
        
        self.rock_rotation_speed_min = -2.0  # Minimum rotation speed (degrees per frame)
        self.rock_rotation_speed_max = 2.0   # Maximum rotation speed (degrees per frame)
        
        # Difficulty progression settings
        self.base_rock_speed_min = 1.0  # Minimum speed at start
        self.base_rock_speed_max = 2.0  # Maximum speed at start
        self.difficulty_increase_time = 1200  # Frames (30 seconds at 60 FPS)
        self.speed_multiplier_per_level = 0.4  # How much faster each level
        self.max_difficulty_level = 15  # Maximum difficulty level