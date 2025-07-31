"""
GameStats class to track and manage all game statistics.
This module handles scoring, difficulty progression, game timing, and game states.
"""

class GameStats:
    """Track statistics for the Asteroids game."""
    
    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        
        # Game state
        self.game_active = False
        self.game_over = False
        
        self.reset_stats()
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        # Score tracking
        self.score = 0
        self.rocks_destroyed = 0
        self.rocks_escaped = 0  # Track rocks that escaped
        
        # Lives tracking
        self.ships_left = self.settings.ship_lives
        
        # Game time and difficulty tracking
        self.game_time = 0  # Total game time in frames
        self.current_difficulty_level = 0
        
        # Performance tracking
        self.total_bullets_fired = 0
        self.accuracy = 0.0  # Percentage of bullets that hit rocks
        
        # Reset game state flags
        self.game_over = False
        
    def update_game_time(self):
        """Update game time and check for difficulty level changes."""
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
            return True  # Return True if level increased
        return False
    
    def add_rock_destroyed(self):
        """Update score and statistics when a rock is destroyed."""
        self.rocks_destroyed += 1
        points = 10 * (self.current_difficulty_level + 1)  # More points for higher difficulty
        self.score += points
        
        # Update accuracy
        if self.total_bullets_fired > 0:
            self.accuracy = (self.rocks_destroyed / self.total_bullets_fired) * 100
        
        print(f"¡Roca destruida! +{points} puntos. Score total: {self.score}")
        print(f"Rocas destruidas: {self.rocks_destroyed} | Precisión: {self.accuracy:.1f}%")
        
        return points  # Return points earned
    
    def add_bullet_fired(self):
        """Track when a bullet is fired."""
        self.total_bullets_fired += 1
        
        # Update accuracy
        if self.total_bullets_fired > 0:
            self.accuracy = (self.rocks_destroyed / self.total_bullets_fired) * 100
    
    def add_rock_escaped(self):
        """Update score and statistics when a rock escapes."""
        self.rocks_escaped += 1
        penalty = self.settings.rock_escaped_penalty
        self.score += penalty  # Add negative points
        
        # Ensure score doesn't go below 0
        if self.score < 0:
            self.score = 0
        
        print(f"¡Roca escapó! {penalty} puntos. Score total: {self.score}")
        print(f"Rocas escapadas: {self.rocks_escaped}")
        
        return penalty  # Return penalty applied
    
    def ship_hit(self):
        """Respond to ship being hit by a rock."""
        if self.ships_left > 0:
            # Decrement ships_left
            self.ships_left -= 1
            print(f"¡Nave golpeada! Vidas restantes: {self.ships_left}")
            
            # Check if game should end
            if self.ships_left == 0:
                self.end_game()
                print("¡Sin más vidas! Fin del juego.")
                return False  # Game over
            return True  # Continue playing
        else:
            self.end_game()
            return False
    
    def get_game_time_seconds(self):
        """Get current game time in seconds."""
        return self.game_time // 60
    
    def get_current_rock_speed_range(self):
        """Calculate current rock speed range based on difficulty level."""
        speed_multiplier = 1 + (self.current_difficulty_level * self.settings.speed_multiplier_per_level)
        min_speed = self.settings.base_rock_speed_min * speed_multiplier
        max_speed = self.settings.base_rock_speed_max * speed_multiplier
        return min_speed, max_speed
    
    def get_stats_summary(self):
        """Get a summary of all current statistics."""
        return {
            'score': self.score,
            'rocks_destroyed': self.rocks_destroyed,
            'rocks_escaped': self.rocks_escaped,
            'time_seconds': self.get_game_time_seconds(),
            'difficulty_level': self.current_difficulty_level + 1,
            'total_bullets_fired': self.total_bullets_fired,
            'accuracy': self.accuracy,
            'rock_speed_range': self.get_current_rock_speed_range(),
            'ships_left': self.ships_left
        }
    
    def start_game(self):
        """Start a new game."""
        self.game_active = True
        self.game_over = False
        self.reset_stats()
    
    def end_game(self):
        """End the current game."""
        self.game_active = False
        self.game_over = True
