import pygame
import random
import math
from pygame.sprite import Sprite

class Rock(Sprite):
    """A class to represent a single rock in the fleet."""
    
    # Class variable to store preloaded images
    rock_images = []
    
    @classmethod
    def load_images(cls):
        """Load all rock images once at the start of the game."""
        if not cls.rock_images:  # Only load if not already loaded
            image_paths = ['images/rock1.png', 'images/rock2.png']
            for path in image_paths:
                try:
                    image = pygame.image.load(path)
                    cls.rock_images.append(image)
                    print(f"Imagen cargada: {path}")
                except pygame.error as e:
                    print(f"Error cargando imagen {path}: {e}")
            
            if not cls.rock_images:
                print("¡Error! No se pudieron cargar las imágenes de rocas")
    
    def __init__(self, ai_game):
        """Initialize the rock and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game  # Reference to game for difficulty calculation

        # Ensure images are loaded
        Rock.load_images()
        
        # Select a random rock image from preloaded images and determine which one
        if Rock.rock_images:
            # Randomly select an image index
            image_index = random.randint(0, len(Rock.rock_images) - 1)
            original_image = Rock.rock_images[image_index].copy()
            
            # Determine scale range based on which image was selected
            if image_index == 0:  # rock1.png (first image)
                scale_min = self.settings.rock1_scale_min
                scale_max = self.settings.rock1_scale_max
            else:  # rock2.png (second image) - reduce size since it's too big
                scale_min = self.settings.rock2_scale_min
                scale_max = self.settings.rock2_scale_max
        else:
            # Fallback in case images couldn't be loaded
            print("¡Advertencia! Usando imagen por defecto")
            original_image = pygame.Surface((50, 50))  # Create a simple rectangle as fallback
            original_image.fill((128, 128, 128))  # Gray color
            scale_min = 0.6
            scale_max = 1.4
        
        # Apply random scaling based on selected image
        scale_factor = random.uniform(scale_min, scale_max)
        original_width = original_image.get_width()
        original_height = original_image.get_height()
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
        
        # Apply random rotation (0 to 360 degrees)
        initial_rotation = random.uniform(0, 360)
        self.image = pygame.transform.rotate(scaled_image, initial_rotation)
        
        # Store original image and rotation info for continuous rotation
        self.original_image = scaled_image
        self.rotation_angle = initial_rotation
        self.rotation_speed = random.uniform(
            self.settings.rock_rotation_speed_min,
            self.settings.rock_rotation_speed_max
        )  # Random rotation speed from settings
        
        self.rect = self.image.get_rect()
        
        # Create a smaller collision rect for more accurate collision detection
        self.collision_padding = 20  # Pixels to shrink from each side for rocks
        self.collision_rect = pygame.Rect(0, 0, 
                                        self.rect.width - (self.collision_padding * 2),
                                        self.rect.height - (self.collision_padding * 2))
        
        # Set random starting position on screen edge and direction
        self._set_random_spawn_position()
        
        # Store the rock's exact position as floats.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Update collision rect initial position
        self.collision_rect.center = (self.x, self.y)
        
        # Set random speed based on current difficulty level
        min_speed, max_speed = ai_game.get_current_rock_speed_range()
        self.speed = random.uniform(min_speed, max_speed)
        
        # Track if rock has been visible on screen (to prevent counting spawn-escaped rocks)
        self.has_been_visible = False
    
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
        """Update the rock's position and rotation."""
        # Move the rock based on its velocity and speed
        self.x += self.velocity_x * self.speed
        self.y += self.velocity_y * self.speed
        
        # Update rotation
        self.rotation_angle += self.rotation_speed
        self.rotation_angle = self.rotation_angle % 360  # Keep angle in 0-360 range
        
        # Apply rotation to the image
        center = (self.x, self.y)
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=center)
        
        # Update collision rect to stay centered with the rock
        self.collision_rect.center = center
        
        # Update position
        self.x = center[0]
        self.y = center[1]
        
        # Check if rock is now visible on screen
        if not self.has_been_visible:
            self.has_been_visible = self.is_visible_on_screen()
    
    def is_visible_on_screen(self):
        """Check if any part of the rock is visible on screen."""
        return (self.rect.right > 0 and self.rect.left < self.settings.screen_width and
                self.rect.bottom > 0 and self.rect.top < self.settings.screen_height)
    
    def is_off_screen(self):
        """Check if the rock has moved completely off screen."""
        return (self.rect.right < 0 or self.rect.left > self.settings.screen_width or
                self.rect.bottom < 0 or self.rect.top > self.settings.screen_height)
    
    def has_escaped(self):
        """Check if the rock has truly escaped (was visible and now off screen)."""
        return self.has_been_visible and self.is_off_screen()