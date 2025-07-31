"""
Button class for creating interactive buttons in the game.
This module handles button rendering, interaction, and click detection.
"""

import pygame.font

class Button:
    """A class to build buttons for the game."""
    
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)  # Dark green
        self.text_color = (255, 255, 255)  # White
        self.font = pygame.font.Font(None, 48)
        
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # The button message needs to be prepped only once.
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                         self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        """Draw blank button and then draw message."""
        # Draw button background
        self.screen.fill(self.button_color, self.rect)
        
        # Draw button border for better visibility
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 2)
        
        # Draw button text
        self.screen.blit(self.msg_image, self.msg_image_rect)
    
    def update_msg(self, msg):
        """Update the button message."""
        self._prep_msg(msg)

class PlayButton(Button):
    """A specialized button for play/restart functionality."""
    
    def __init__(self, ai_game):
        """Initialize the play button."""
        super().__init__(ai_game, "PLAY")
        
        # Make the play button slightly larger
        self.width, self.height = 250, 60
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # Update the message with new dimensions
        self._prep_msg("PLAY")
    
    def update_for_game_over(self):
        """Update button for game over state."""
        self.button_color = (135, 0, 0)  # Dark red
        self._prep_msg("PLAY AGAIN")

class GameOverScreen:
    """A class to display game over information and play button."""
    
    def __init__(self, ai_game):
        """Initialize game over screen attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        
        # Font settings
        self.title_font = pygame.font.Font(None, 72)
        self.text_font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)
        
        # Create play button (position will be set dynamically)
        self.play_button = PlayButton(ai_game)
    
    def show_game_over(self):
        """Display the game over screen with statistics."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over title
        title_image = self.title_font.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_image.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.y = self.screen_rect.centery - 180
        self.screen.blit(title_image, title_rect)
        
        # Final statistics
        stats_summary = self.stats.get_stats_summary()
        final_stats = [
            f"Final Score: {stats_summary['score']:,}",
            f"Rocks Destroyed: {stats_summary['rocks_destroyed']}",
            f"Time Survived: {stats_summary['time_seconds']}s",
            f"Level Reached: {stats_summary['difficulty_level']}",
            f"Accuracy: {stats_summary['accuracy']:.1f}%"
        ]
        
        # Draw statistics
        y_offset = title_rect.bottom + 30
        for stat in final_stats:
            stat_image = self.text_font.render(stat, True, self.text_color)
            stat_rect = stat_image.get_rect()
            stat_rect.centerx = self.screen_rect.centerx
            stat_rect.y = y_offset
            self.screen.blit(stat_image, stat_rect)
            y_offset += 35
        
        # Position play again button below statistics
        self.play_button.rect.centerx = self.screen_rect.centerx
        self.play_button.rect.y = y_offset + 30
        self.play_button._prep_msg("PLAY AGAIN")
        
        # Draw play again button
        self.play_button.draw_button()

class StartScreen:
    """A class to display the start screen."""
    
    def __init__(self, ai_game):
        """Initialize start screen attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Font settings
        self.title_font = pygame.font.Font(None, 96)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        self.text_color = (255, 255, 255)
        
        # Create play button (position will be set dynamically)
        self.play_button = PlayButton(ai_game)
    
    def show_start_screen(self):
        """Display the start screen."""
        # Fill background
        self.screen.fill((0, 0, 20))  # Darker blue background
        
        # Game title
        title_image = self.title_font.render("ASTEROIDS", True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.y = self.screen_rect.centery - 200
        self.screen.blit(title_image, title_rect)
        
        # Instructions
        instructions = [
            "Arrow Keys: Mueve y Rota la Nave",
            "Spacebar: Disparar",
            "Q: Salir del Juego",
            "",
            "Destruye los asteroides para ganar puntos!",
            "La dificultad aumenta con el tiempo."
        ]
        
        y_offset = title_rect.bottom + 30
        for instruction in instructions:
            if instruction:  # Skip empty strings
                inst_image = self.text_font.render(instruction, True, self.text_color)
                inst_rect = inst_image.get_rect()
                inst_rect.centerx = self.screen_rect.centerx
                inst_rect.y = y_offset
                self.screen.blit(inst_image, inst_rect)
            y_offset += 30
        
        # Position play button below instructions
        self.play_button.rect.centerx = self.screen_rect.centerx
        self.play_button.rect.y = y_offset + 30
        self.play_button._prep_msg("PLAY")
        
        # Draw play button
        self.play_button.draw_button()
