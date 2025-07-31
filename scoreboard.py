"""
Scoreboard class to display game statistics and UI elements.
This module handles all visual display of scores, stats, and game info.
"""

import pygame

class Scoreboard:
    """A class to report scoring information."""
    
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Font settings for displaying scoring information.
        self.text_color = (255, 255, 255)  # White text
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load ship image for lives display
        self.ship_image = pygame.image.load('images/fighter.png')
        self.ship_image = pygame.transform.scale(self.ship_image, (30, 30))  # Small size for lives display
        
        # Prepare the initial score images.
        self.prep_score()
        self.prep_level()
        self.prep_time()
        self.prep_rocks_destroyed()
        self.prep_rocks_escaped()
        self.prep_accuracy()
        self.prep_rock_speed()
        self.prep_ships()
    
    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Puntuación: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        
        # Display the score at the top left of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = 10
        self.score_rect.top = 90
    
    def prep_level(self):
        """Turn the level into a rendered image."""
        level = self.stats.current_difficulty_level + 1
        level_str = f"Nivel: {level}"
        self.level_image = self.font.render(level_str, True, self.text_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = 10
        self.level_rect.top = 50
    
    def prep_time(self):
        """Turn the game time into a rendered image."""
        time_seconds = self.stats.get_game_time_seconds()
        time_str = f"Tiempo: {time_seconds}s"
        self.time_image = self.font.render(time_str, True, self.text_color)
        
        # Position the time at the top.
        self.time_rect = self.time_image.get_rect()
        self.time_rect.left = 10
        self.time_rect.top = 10
    
    def prep_rocks_destroyed(self):
        """Turn the rocks destroyed count into a rendered image."""
        rocks_str = f"Rocas destruidas: {self.stats.rocks_destroyed}"
        self.rocks_image = self.font.render(rocks_str, True, self.text_color)
        
        # Position below the score.
        self.rocks_rect = self.rocks_image.get_rect()
        self.rocks_rect.left = 10
        self.rocks_rect.top = 130
    
    def prep_rocks_escaped(self):
        """Turn the rocks escaped count into a rendered image."""
        rocks_escaped_str = f"Rocas escapadas: {self.stats.rocks_escaped}"
        self.rocks_escaped_image = self.font.render(rocks_escaped_str, True, (255, 100, 100))  # Light red color
        
        # Position below rocks destroyed.
        self.rocks_escaped_rect = self.rocks_escaped_image.get_rect()
        self.rocks_escaped_rect.left = 10
        self.rocks_escaped_rect.top = 170
    
    def prep_accuracy(self):
        """Turn the accuracy percentage into a rendered image."""
        accuracy_str = f"Precisión: {self.stats.accuracy:.1f}%"
        self.accuracy_image = self.small_font.render(accuracy_str, True, self.text_color)
        
        # Position below rocks escaped.
        self.accuracy_rect = self.accuracy_image.get_rect()
        self.accuracy_rect.left = 10
        self.accuracy_rect.top = 210
    
    def prep_rock_speed(self):
        """Turn the current rock speed range into a rendered image."""
        min_speed, max_speed = self.stats.get_current_rock_speed_range()
        speed_str = f"Velocidad rocas: {min_speed:.1f}-{max_speed:.1f}"
        self.speed_image = self.small_font.render(speed_str, True, self.text_color)
        
        # Position below accuracy.
        self.speed_rect = self.speed_image.get_rect()
        self.speed_rect.left = 10
        self.speed_rect.top = 235
    
    def prep_bullets_info(self):
        """Turn bullets information into a rendered image."""
        bullets_fired = self.stats.total_bullets_fired
        bullets_str = f"Balas disparadas: {bullets_fired}"
        self.bullets_image = self.small_font.render(bullets_str, True, self.text_color)
        
        # Position at the top right.
        self.bullets_rect = self.bullets_image.get_rect()
        self.bullets_rect.right = self.screen_rect.right - 10
        self.bullets_rect.top = 10
    
    def prep_current_bullets(self):
        """Show current bullets available."""
        current_bullets = len(self.ai_game.bullets)
        max_bullets = self.settings.bullets_allowed
        bullets_str = f"Balas: {current_bullets}/{max_bullets}"
        self.current_bullets_image = self.small_font.render(bullets_str, True, self.text_color)
        
        # Position at the top right, below bullets fired.
        self.current_bullets_rect = self.current_bullets_image.get_rect()
        self.current_bullets_rect.right = self.screen_rect.right - 10
        self.current_bullets_rect.top = 35
    
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = pygame.sprite.Group()
        for ship_number in range(self.stats.ships_left):
            ship = pygame.sprite.Sprite()
            ship.image = self.ship_image.copy()
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * 40  # Space ships 40 pixels apart
            ship.rect.y = 260  # Position below other stats
            self.ships.add(ship)
    
    def show_score(self):
        """Draw all score information to the screen."""
        # Update all score elements
        self.prep_score()
        self.prep_level()
        self.prep_time()
        self.prep_rocks_destroyed()
        self.prep_rocks_escaped()
        self.prep_accuracy()
        self.prep_rock_speed()
        self.prep_bullets_info()
        self.prep_current_bullets()
        self.prep_ships()
        
        # Draw all score information
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.time_image, self.time_rect)
        self.screen.blit(self.rocks_image, self.rocks_rect)
        self.screen.blit(self.rocks_escaped_image, self.rocks_escaped_rect)
        self.screen.blit(self.accuracy_image, self.accuracy_rect)
        self.screen.blit(self.speed_image, self.speed_rect)
        self.screen.blit(self.bullets_image, self.bullets_rect)
        self.screen.blit(self.current_bullets_image, self.current_bullets_rect)
        
        # Draw the ships (lives)
        self.ships.draw(self.screen)
    
    def show_game_over_screen(self):
        """Display game over statistics."""
        # Create game over title
        game_over_str = "GAME OVER"
        game_over_image = pygame.font.Font(None, 72).render(
            game_over_str, True, (255, 0, 0)
        )
        game_over_rect = game_over_image.get_rect()
        game_over_rect.center = self.screen_rect.center
        game_over_rect.y -= 100
        
        # Get final stats
        stats_summary = self.stats.get_stats_summary()
        
        # Create final statistics display
        final_stats = [
            f"Puntuación Final: {stats_summary['score']:,}",
            f"Rocas Destruidas: {stats_summary['rocks_destroyed']}",
            f"Rocas Escapadas: {stats_summary['rocks_escaped']}",
            f"Tiempo Total: {stats_summary['time_seconds']}s",
            f"Nivel Alcanzado: {stats_summary['difficulty_level']}",
            f"Precisión: {stats_summary['accuracy']:.1f}%",
            f"Balas Disparadas: {stats_summary['total_bullets_fired']}",
            f"Vidas Restantes: {stats_summary['ships_left']}"
        ]
        
        # Draw game over screen
        self.screen.blit(game_over_image, game_over_rect)
        
        y_offset = game_over_rect.bottom + 50
        for stat in final_stats:
            stat_image = self.font.render(stat, True, self.text_color)
            stat_rect = stat_image.get_rect()
            stat_rect.centerx = self.screen_rect.centerx
            stat_rect.y = y_offset
            self.screen.blit(stat_image, stat_rect)
            y_offset += 40
