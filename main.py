import pygame
import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Zombie Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Physics and State
        self.gravity = 0
        self.movement = 0
        self.facing_right = True
        self.last_shot_time = 0  # Changed from self.shooting for clarity

        # --- Assets ---
        # Player Idle
        self.player_right = pygame.image.load(resource_path("Graphics/Player Right Gun.png")).convert_alpha()
        self.player_right = pygame.transform.scale(self.player_right, (200, 150))
        
        self.player_left = pygame.image.load(resource_path("Graphics/Player Left Gun.png")).convert_alpha()
        self.player_left = pygame.transform.scale(self.player_left, (200, 150))

        # Player Walking
        self.walk_right = pygame.image.load(resource_path("Graphics/Player Walking Right.png")).convert_alpha()
        self.walk_right = pygame.transform.scale(self.walk_right, (200, 150))
        
        self.walk_left = pygame.image.load(resource_path("Graphics/Player Walking Left.png")).convert_alpha()
        self.walk_left = pygame.transform.scale(self.walk_left, (200, 150))

        # Bullets
        self.bullet_img_right = pygame.image.load(resource_path("Graphics/Bullet.png")).convert_alpha()
        self.bullet_img_right = pygame.transform.scale(self.bullet_img_right, (25, 25))
        
        self.bullet_img_left = pygame.image.load(resource_path("Graphics/Bullet Left.png")).convert_alpha()
        self.bullet_img_left = pygame.transform.scale(self.bullet_img_left, (25, 25))

        # Player Rect
        self.player_rect = self.player_right.get_rect(center=(100, 500))

        # Bullet Lists (Store dictionaries or objects to keep track of rect + direction)
        self.active_bullets = [] # List of [pygame.Rect, direction_multiplier]

        # Background
        self.gameBackground = pygame.image.load(resource_path("Graphics/game Background.png")).convert_alpha()
        self.gameBackground = pygame.transform.scale(self.gameBackground, (1280, 720))

        # Controls
        self.right_pressed = False
        self.left_pressed = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.right_pressed = True
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.left_pressed = True
                
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    # Cooldown check: 500ms (0.5 seconds)
                    if current_time - self.last_shot_time > 500:
                        self.shoot()
                        self.last_shot_time = current_time

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.right_pressed = False
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.left_pressed = False

    def shoot(self):
        if self.facing_right:
            # Create a NEW rect instance for this specific bullet
            new_rect = self.bullet_img_right.get_rect(midleft=self.player_rect.midright)
            self.active_bullets.append({"rect": new_rect, "speed": 10, "img": self.bullet_img_right})
        else:
            new_rect = self.bullet_img_left.get_rect(midright=self.player_rect.midleft)
            self.active_bullets.append({"rect": new_rect, "speed": -10, "img": self.bullet_img_left})

    def update(self):
        # Handle Movement Logic
        if self.right_pressed and not self.left_pressed:
            self.movement = 5
            self.facing_right = True
        elif self.left_pressed and not self.right_pressed:
            self.movement = -5
            self.facing_right = False
        else:
            self.movement = 0

        # Apply Movement & Gravity
        self.player_rect.x += self.movement
        self.player_rect.y += self.gravity
        self.gravity += 1

        # Floor Collision
        if self.player_rect.bottom >= 600:
            self.player_rect.bottom = 600
            self.gravity = 0

        # Update Bullets and Remove if off-screen
        for b in self.active_bullets:
            b["rect"].x += b["speed"]
        
        # This list comprehension safely removes bullets out of bounds
        self.active_bullets = [b for b in self.active_bullets if -50 < b["rect"].x < 1330]

    def render(self):
        self.screen.blit(self.gameBackground, (0, 0))

        # Draw Player
        if self.facing_right:
            img = self.walk_right if self.movement != 0 else self.player_right
        else:
            img = self.walk_left if self.movement != 0 else self.player_left
        
        self.screen.blit(img, self.player_rect)

        # Draw Bullets
        for b in self.active_bullets:
            self.screen.blit(b["img"], b["rect"])

        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()