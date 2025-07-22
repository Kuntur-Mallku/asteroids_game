import pygame
import math
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.center = ai_game.ship.rect.center

        # Store the bullet's position as floats.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        
        # Store the ship's angle to calculate bullet direction
        self.angle = ai_game.ship.angle
        
        # Calculate velocity components based on ship's direction
        radians = math.radians(self.angle - 90)
        self.velocity_x = self.settings.bullet_speed * math.cos(radians)
        self.velocity_y = self.settings.bullet_speed * math.sin(radians)

    def update(self):
        """Move the bullet in the direction it was fired."""
        # Update the float position of the bullet using velocity components.
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Update the rect position.
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)