import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from rock import Rock
import ship

class Asteroids:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Asteroids")

        # Initialize font for UI text
        self.font = pygame.font.Font(None, 36)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        
        # Rock spawning timer
        self.rock_spawn_timer = 0
        
        # Game time and difficulty tracking
        self.game_time = 0  # Total game time in frames
        self.current_difficulty_level = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_rocks()
            self._update_game_time()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.rotating_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.rotating_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_forward = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_backward = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.rotating_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.rotating_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_forward = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_backward = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared from any edge of the screen.
        for bullet in self.bullets.copy():
            if (bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_height or 
                bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width):
                self.bullets.remove(bullet)

    def _update_rocks(self):
        """Update rocks and spawn new ones."""
        # Update rock positions
        self.rocks.update()
        
        # Remove rocks that have moved off screen
        for rock in self.rocks.copy():
            if rock.is_off_screen():
                self.rocks.remove(rock)
        
        # Spawn new rocks periodically
        self.rock_spawn_timer += 1
        if (self.rock_spawn_timer >= self.settings.rock_spawn_rate and 
            len(self.rocks) < self.settings.max_rocks):
            new_rock = Rock(self)
            self.rocks.add(new_rock)
            self.rock_spawn_timer = 0

    def _update_game_time(self):
        """Update game time and difficulty level."""
        self.game_time += 1
        
        # Calculate current difficulty level
        new_difficulty_level = min(
            self.game_time // self.settings.difficulty_increase_time,
            self.settings.max_difficulty_level
        )
        
        # Check if difficulty level increased
        if new_difficulty_level > self.current_difficulty_level:
            self.current_difficulty_level = new_difficulty_level
            print(f"Nivel de dificultad aumentado a: {self.current_difficulty_level + 1}")
    
    def get_current_rock_speed_range(self):
        """Calculate current rock speed range based on difficulty level."""
        speed_multiplier = 1 + (self.current_difficulty_level * self.settings.speed_multiplier_per_level)
        min_speed = self.settings.base_rock_speed_min * speed_multiplier
        max_speed = self.settings.base_rock_speed_max * speed_multiplier
        return min_speed, max_speed
    
    def get_game_time_seconds(self):
        """Get current game time in seconds."""
        return self.game_time // 60

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.rocks.draw(self.screen)
        self.ship.blitme()
        
        # Draw UI information
        self._draw_ui()

        pygame.display.flip()
    
    def _draw_ui(self):
        """Draw UI elements like timer and difficulty level."""
        # Game time
        time_seconds = self.get_game_time_seconds()
        time_text = self.font.render(f"Tiempo: {time_seconds}s", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 10))
        
        # Difficulty level
        difficulty_text = self.font.render(f"Nivel: {self.current_difficulty_level + 1}", True, (255, 255, 255))
        self.screen.blit(difficulty_text, (10, 50))
        
        # Current rock speed info
        min_speed, max_speed = self.get_current_rock_speed_range()
        speed_text = self.font.render(f"Velocidad rocas: {min_speed:.1f}-{max_speed:.1f}", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 90))

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = Asteroids()
    ai.run_game()