import pygame
import random

# --- Konfiguration ---
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 40
GRAVITY = 0.8
JUMP_STRENGTH = -16
SPEED = 7

# Farben
DARK_GREY = (38, 36, 60)
BLUE = (50, 150, 255)
GREEN = (46, 204, 113)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, PLAYER_SIZE, PLAYER_SIZE)
        self.vel_y = 0
        self.on_ground = False
        self.old_x = self.rect.x
        self.old_y = self.rect.y

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        # Horizontale Bewegung
        self.old_x = self.rect.x
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
        self.rect.x += dx
        self.check_collision(platforms, 'horizontal')

        # Vertikale Bewegung
        self.old_y = self.rect.y
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
        
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collision(platforms, 'vertical')

    def check_collision(self, platforms, direction):
        for p in platforms:
            if self.rect.colliderect(p):
                if direction == 'horizontal':
                    if self.rect.right > p.left and self.old_x + PLAYER_SIZE <= p.left:
                        self.rect.right = p.left
                    elif self.rect.left < p.right and self.old_x >= p.right:
                        self.rect.left = p.right
                if direction == 'vertical':
                    if self.vel_y > 0:
                        self.rect.bottom = p.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.top = p.bottom
                        self.vel_y = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Infinite Procedural Jump & Run")
    clock = pygame.time.Clock()

    player = Player()
    
    # Start-Plattformen
    platforms = [pygame.Rect(0, 500, 1000, 100)]
    last_platform_x = 1000

    def spawn_platform(last_x):
        # Zufälliger Abstand und Höhe für die nächste Plattform
        gap = random.randint(150, 300)
        width = random.randint(150, 400)
        height = 20
        y = random.randint(300, 500)
        new_x = last_x + gap
        return pygame.Rect(new_x, y, width, height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Plattformen generieren (wenn der Spieler sich dem Ende nähert)
        if player.rect.x + WIDTH > last_platform_x:
            new_p = spawn_platform(last_platform_x)
            platforms.append(new_p)
            last_platform_x = new_p.right

        # 2. Alte Plattformen löschen (Performance-Optimierung)
        platforms = [p for p in platforms if p.right > player.rect.x - WIDTH]

        # 3. Logik Update
        player.update(platforms)

        # 4. Kamera & Zeichnen
        offset_x = WIDTH // 2 - player.rect.centerx
        screen.fill(DARK_GREY)
        
        for p in platforms:
            pygame.draw.rect(screen, GREEN, p.move(offset_x, 0))
        
        pygame.draw.rect(screen, BLUE, player.rect.move(offset_x, 0))

        # 5. Game Over Reset (falls man runterfällt)
        if player.rect.y > HEIGHT + 500:
            player.__init__()
            platforms = [pygame.Rect(0, 500, 1000, 100)]
            last_platform_x = 1000

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()