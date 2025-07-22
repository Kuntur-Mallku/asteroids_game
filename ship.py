import pygame
import math
# from alien_invasion import AlienInvasion

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.original_image = pygame.image.load('images/fighter.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()

        # Start each new ship at the center of the screen.
        self.rect.center = self.screen_rect.center

        # Store a float for the ship's exact position.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Rotation attributes
        self.angle = 0  # Degrees (0 = pointing right, 90 = pointing down, etc.)

        # Movement flags; start with a ship that's not moving.
        self.moving_forward = False
        self.moving_backward = False
        self.rotating_right = False
        self.rotating_left = False
    
    def update(self):
        """Update the ship's position based on movement flag."""
        # Handle rotation
        if self.rotating_right:
            self.angle += self.settings.ship_rotation_speed
        if self.rotating_left:
            self.angle -= self.settings.ship_rotation_speed

        # Keep angle in 0-360 range
        self.angle = self.angle % 360
        
        # Handle movement
        if self.moving_forward or self.moving_backward:
            # Convert angle to radians for trigonometry
            radians = math.radians(self.angle + 90)  # Adjusting so 0° points right

            # Calculate velocity components
            speed = self.settings.ship_speed
            if self.moving_forward:
                speed = -speed
            
            # Update position using velocity components
            # El ángulo 0° = nave apuntando hacia la derecha
            # El ángulo 90° = nave apuntando hacia abajo
            # Se usa trigonometría para calcular la dirección:
            self.x += speed * math.cos(radians)
            self.y += speed * math.sin(radians)

            # Wrap around screen edges (classic Asteroids behavior)
            if self.x < 0:
                self.x = self.settings.screen_width
            elif self.x > self.settings.screen_width:
                self.x = 0
                
            if self.y < 0:
                self.y = self.settings.screen_height
            elif self.y > self.settings.screen_height:
                self.y = 0
        
        # Update rect position
        self.rect.centerx = self.x
        self.rect.centery = self.y

        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)