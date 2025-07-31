import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from rock import Rock
from game_stats import GameStats
from scoreboard import Scoreboard
from button import StartScreen, GameOverScreen
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

        # Create an instance to store game statistics and create a scoreboard.
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self)
        
        # Create start and game over screens
        self.start_screen = StartScreen(self)
        self.game_over_screen = GameOverScreen(self)

        # Initialize font for UI text (kept for backwards compatibility)
        self.font = pygame.font.Font(None, 36)
        
        # Preload rock images for better performance
        Rock.load_images()

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        
        # Rock spawning timer
        self.rock_spawn_timer = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_rocks()
                self._check_bullet_rock_collisions()
                self._check_ship_rock_collisions()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
            if self.stats.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_p:
            # Allow 'P' key to start/restart game
            if not self.stats.game_active:
                self._start_game()
    
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

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if not self.stats.game_active:
            # Check start screen button
            if not self.stats.game_over:
                button_clicked = self.start_screen.play_button.rect.collidepoint(mouse_pos)
            else:
                button_clicked = self.game_over_screen.play_button.rect.collidepoint(mouse_pos)
            
            if button_clicked:
                self._start_game()
    
    def _start_game(self):
        """Start a new game."""
        # Reset the game statistics and start the game
        self.stats.start_game()
        
        # Reset the scoreboard
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        
        # Empty the list of aliens and bullets
        self.rocks.empty()
        self.bullets.empty()
        
        # Create a new fleet and center the ship
        self.ship.rect.center = self.ship.screen_rect.center
        self.ship.x = float(self.ship.rect.centerx)
        self.ship.y = float(self.ship.rect.centery)
        
        # Reset ship movement flags
        self.ship.moving_forward = False
        self.ship.moving_backward = False
        self.ship.rotating_left = False
        self.ship.rotating_right = False
        
        # Reset rock spawning timer
        self.rock_spawn_timer = 0
        
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            # Track bullet fired for statistics
            self.stats.add_bullet_fired()

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
        # Only update rocks if game is active
        if not self.stats.game_active:
            return
            
        # Update rock positions
        self.rocks.update()
        
        # Remove rocks that have moved off screen and apply penalty only if they truly escaped
        for rock in self.rocks.copy():
            if rock.is_off_screen():
                # Only apply penalty if the rock was actually visible on screen before escaping
                if rock.has_been_visible:
                    self.stats.add_rock_escaped()
                self.rocks.remove(rock)
        
        # Spawn new rocks periodically
        self.rock_spawn_timer += 1
        if (self.rock_spawn_timer >= self.settings.rock_spawn_rate and 
            len(self.rocks) < self.settings.max_rocks):
            new_rock = Rock(self)
            self.rocks.add(new_rock)
            self.rock_spawn_timer = 0

    def _check_bullet_rock_collisions(self):
        """Check for collisions between bullets and rocks using precise collision detection."""
        for bullet in self.bullets.copy():
            for rock in self.rocks.copy():
                # Use the rock's collision_rect for more precise collision detection
                if bullet.rect.colliderect(rock.collision_rect):
                    # Remove both bullet and rock
                    self.bullets.remove(bullet)
                    self.rocks.remove(rock)
                    
                    # Update score and statistics
                    points = self.stats.add_rock_destroyed()
                    break  # Exit inner loop since bullet is gone

    def _check_ship_rock_collisions(self):
        """Check for collisions between ship and rocks using precise collision detection."""
        for rock in self.rocks:
            if self.ship.collision_rect.colliderect(rock.collision_rect):
                self._ship_hit()
                break  # Exit after first collision
    
    def _ship_hit(self):
        """Respond to the ship being hit by a rock."""
        print("¡La nave fue golpeada!")
        
        # Use the lives system from stats
        can_continue = self.stats.ship_hit()
        
        if can_continue:
            # Remove all rocks and bullets to give player a fresh start
            self.rocks.empty()
            self.bullets.empty()
            
            # Reset ship position
            self.ship.rect.center = self.ship.screen_rect.center
            self.ship.x = float(self.ship.rect.centerx)
            self.ship.y = float(self.ship.rect.centery)
            
            # Reset ship movement flags
            self.ship.moving_forward = False
            self.ship.moving_backward = False
            self.ship.rotating_left = False
            self.ship.rotating_right = False
            
            # Pause briefly to give player time to react
            pygame.time.wait(1000)  # 1 second pause
        else:
            # Game over - show the mouse cursor
            pygame.mouse.set_visible(True)

    def _update_game_time(self):
        """Update game time and difficulty level."""
        level_increased = self.stats.update_game_time()
        # You can add special effects here when level increases
        if level_increased:
            # Could add visual/audio feedback for level up
            pass
    
    def get_current_rock_speed_range(self):
        """Calculate current rock speed range based on difficulty level."""
        return self.stats.get_current_rock_speed_range()
    
    def get_game_time_seconds(self):
        """Get current game time in seconds."""
        return self.stats.get_game_time_seconds()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        
        if self.stats.game_active:
            # Draw game elements
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.rocks.draw(self.screen)
            self.ship.blitme()
            
            # Optional: Draw collision rectangles for debugging (comment out for normal play)
            # self._draw_collision_rects()
            
            # Draw the score information.
            self.sb.show_score()
        
        elif not self.stats.game_active and not self.stats.game_over:
            # Show start screen
            self.start_screen.show_start_screen()
        
        elif self.stats.game_over:
            # Show game over screen
            self.game_over_screen.show_game_over()

        pygame.display.flip()
    
    def _draw_collision_rects(self):
        """Draw collision rectangles for debugging purposes."""
        # Draw ship collision rect in green
        pygame.draw.rect(self.screen, (0, 255, 0), self.ship.collision_rect, 2)
        
        # Draw rock collision rects in red
        for rock in self.rocks:
            pygame.draw.rect(self.screen, (255, 0, 0), rock.collision_rect, 2)

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = Asteroids()
    ai.run_game()