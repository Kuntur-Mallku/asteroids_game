import pygame
import random
import math
from pygame.sprite import Sprite

class Rock(Sprite):
    """A class to represent a single rock in the fleet."""
    
    def __init__(self, ai_game):
        """Initialize the rock and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game  # Reference to game for difficulty calculation

        # Load the rock image and set its rect attribute.
        self.image = pygame.image.load('images/rock1.png')
        self.rect = self.image.get_rect()
        
        # Set random starting position on screen edge and direction
        self._set_random_spawn_position()
        
        # Store the rock's exact position as floats.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Set random speed based on current difficulty level
        min_speed, max_speed = ai_game.get_current_rock_speed_range()
        self.speed = random.uniform(min_speed, max_speed)
    
    def _set_random_spawn_position(self):
        """Set rock to spawn randomly on any screen edge with random direction."""
        screen_width = self.settings.screen_width
        screen_height = self.settings.screen_height
        
        # Choose random edge: 0=top, 1=right, 2=bottom, 3=left
        edge = random.randint(0, 3)
        
        if edge == 0:  # Top edge
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = -self.rect.height
            # Direction towards screen (downward bias)
            angle = random.uniform(45, 135)  # 45° to 135° (pointing down-ish)
            
        elif edge == 1:  # Right edge
            self.rect.x = screen_width
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            # Direction towards screen (leftward bias)
            angle = random.uniform(135, 225)  # 135° to 225° (pointing left-ish)
            
        elif edge == 2:  # Bottom edge
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = screen_height
            # Direction towards screen (upward bias)
            angle = random.uniform(225, 315)  # 225° to 315° (pointing up-ish)
            
        else:  # Left edge
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, screen_height - self.rect.height)
            # Direction towards screen (rightward bias)
            angle = random.uniform(315, 405) % 360  # 315° to 45° (pointing right-ish)
        
        # Convert angle to velocity components
        radians = math.radians(angle)
        self.velocity_x = math.cos(radians)
        self.velocity_y = math.sin(radians)
    
    def update(self):
        """Update the rock's position."""
        # Move the rock based on its velocity and speed
        self.x += self.velocity_x * self.speed
        self.y += self.velocity_y * self.speed
        
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
    
    def is_off_screen(self):
        """Check if the rock has moved completely off screen."""
        return (self.rect.right < 0 or self.rect.left > self.settings.screen_width or
                self.rect.bottom < 0 or self.rect.top > self.settings.screen_height)