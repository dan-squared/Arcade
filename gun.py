import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 700
PLAYER_SIZE = 80
ENEMY_SIZE = 50
BULLET_WIDTH, BULLET_HEIGHT = 5, 15
HEART_SIZE = 30
PLAYER_SPEED = 7
ENEMY_SPEED = 3
BULLET_SPEED = 6
SHOOTER_SPEED = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toy Jet Shooter")

try:
    font = pygame.font.Font("Medodica.otf", 24)
except:
    try:
        font = pygame.font.Font("Roboto-Regular.ttf", 24)
    except:
        try:
            font = pygame.font.Font("arial.ttf", 24)
        except:
            font = pygame.font.SysFont("segoeuiemoji", 24)

try:
    heart_img = pygame.image.load("heart.png")
    heart_img = pygame.transform.scale(heart_img, (HEART_SIZE, HEART_SIZE))
    use_heart_image = True
except:
    use_heart_image = False
    heart_img = None

try:
    bullet_img = pygame.image.load("bullet.png")
    bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
    use_bullet_image = True
except:
    use_bullet_image = False
    bullet_img = None

player_img = pygame.image.load("toy_jet.png")
player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))

shooter_img = pygame.image.load("shooter_enemy.png")
shooter_img = pygame.transform.scale(shooter_img, (ENEMY_SIZE, ENEMY_SIZE))
enemy_img = pygame.image.load("target.png")
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))

shoot_sound = pygame.mixer.Sound("shoot.mp3")
explosion_sound = pygame.mixer.Sound("explosion.WAV")
game_over_sound = pygame.mixer.Sound("game_over.mp3")

player = pygame.Rect(WIDTH//2, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
enemies = []
bullets = []
shooter_bullets = []
lives = 3

difficulty = "Medium"

running = True
game_over = False
show_instructions = True
clock = pygame.time.Clock()
score = 0
high_score = 0

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (200, 50, 50)
BUTTON_HOVER_COLOR = (255, 70, 70)
START_BUTTON_COLOR = (50, 200, 50)
START_BUTTON_HOVER_COLOR = (70, 255, 70)

def create_enemy(is_shooter):
    x_position = random.randint(0, WIDTH - ENEMY_SIZE)
    enemy = pygame.Rect(x_position, 0, ENEMY_SIZE, ENEMY_SIZE)
    enemies.append({'rect': enemy, 'is_shooter': is_shooter, 'health': 1})

def fire_bullet():
    bullet = pygame.Rect(player.centerx - BULLET_WIDTH//2, player.top, BULLET_WIDTH, BULLET_HEIGHT)
    bullets.append(bullet)
    shoot_sound.play()

def fire_shooter_bullet(enemy):
    bullet = pygame.Rect(enemy['rect'].centerx - BULLET_WIDTH//2, enemy['rect'].bottom, BULLET_WIDTH, BULLET_HEIGHT)
    shooter_bullets.append(bullet)

def reset_game():
    global score, enemies, bullets, shooter_bullets, lives, game_over, player, show_instructions
    score = 0
    enemies.clear()
    bullets.clear()
    shooter_bullets.clear()
    lives = 3
    game_over = False
    show_instructions = False
    player.x = WIDTH//2
    game_over_sound.stop()

def render_hearts(lives):
    if use_heart_image and heart_img:
        heart_surface = pygame.Surface((HEART_SIZE * lives, HEART_SIZE), pygame.SRCALPHA)
        for i in range(lives):
            heart_surface.blit(heart_img, (i * HEART_SIZE, 0))
        return heart_surface
    else:
        heart_emoji = "❤️" * lives
        return font.render(heart_emoji, True, RED)

def create_button(x, y, width, height, text):
    button_rect = pygame.Rect(x, y, width, height)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    return button_rect, text_surface, text_rect

def is_button_clicked(button_rect, mouse_pos):
    return button_rect.collidepoint(mouse_pos)

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                fire_bullet()
            elif event.key == pygame.K_r and game_over:
                reset_game()
            elif event.key == pygame.K_l:
                try:
                    if use_bullet_image:
                        use_bullet_image = False
                    else:
                        bullet_img = pygame.image.load("bullet.png")
                        bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
                        use_bullet_image = True
                except:
                    use_bullet_image = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_instructions:
                if is_button_clicked(start_button_rect, event.pos):
                    show_instructions = False
            elif game_over:
                if is_button_clicked(restart_button_rect, event.pos):
                    reset_game()
    
    if show_instructions:
        title_text = font.render("Toy Jet Shooter", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(title_text, title_rect)
        
        start_button_rect, start_text, start_text_rect = create_button(
            WIDTH//2 - BUTTON_WIDTH//2,
            HEIGHT//2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Start Game"
        )
        
        mouse_pos = pygame.mouse.get_pos()
        button_color = START_BUTTON_HOVER_COLOR if is_button_clicked(start_button_rect, mouse_pos) else START_BUTTON_COLOR
        
        pygame.draw.rect(screen, button_color, start_button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, start_button_rect, 2, border_radius=10)
        screen.blit(start_text, start_text_rect)
        
        instructions_text = font.render("Use LEFT/RIGHT arrows to move, SPACE to shoot", True, WHITE)
        instructions_rect = instructions_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(instructions_text, instructions_rect)
    else:
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.move_ip(-PLAYER_SPEED, 0)
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.move_ip(PLAYER_SPEED, 0)
            
            if difficulty == "Easy":
                spawn_chance = 80
                shooter_chance = 150
            elif difficulty == "Medium":
                spawn_chance = 60
                shooter_chance = 100
            else:
                spawn_chance = 40
                shooter_chance = 80
            
            if random.randint(1, spawn_chance) == 1:
                is_shooter = random.randint(1, 100) <= shooter_chance
                create_enemy(is_shooter)
            
            for enemy_data in enemies[:]:
                enemy = enemy_data['rect']
                enemy_data['rect'].move_ip(0, ENEMY_SPEED)
                if enemy.top > HEIGHT:
                    enemies.remove(enemy_data)
                if enemy.colliderect(player):
                    game_over = True
                    if score > high_score:
                        high_score = score
                    game_over_sound.play()
            
            for shooter in enemies[:]:
                if shooter['is_shooter']:
                    if random.randint(1, 60) == 1:
                        fire_shooter_bullet(shooter)
            
            for bullet in bullets[:]:
                bullet.move_ip(0, -BULLET_SPEED)
                if bullet.bottom < 0:
                    bullets.remove(bullet)
                for enemy_data in enemies[:]:
                    enemy = enemy_data['rect']
                    if bullet.colliderect(enemy):
                        bullets.remove(bullet)
                        enemy_data['health'] -= 1
                        if enemy_data['health'] == 0:
                            enemies.remove(enemy_data)
                            explosion_sound.play()
                            score += 1
                        break
            
            for bullet in shooter_bullets[:]:
                bullet.move_ip(0, BULLET_SPEED)
                if bullet.colliderect(player):
                    shooter_bullets.remove(bullet)
                    lives -= 1
                    if lives == 0:
                        game_over = True
                        if score > high_score:
                            high_score = score
                        game_over_sound.play()
                if bullet.top > HEIGHT:
                    shooter_bullets.remove(bullet)
            
            for enemy_data in enemies:
                enemy = enemy_data['rect']
                if enemy_data['is_shooter']:
                    screen.blit(shooter_img, enemy)
                else:
                    screen.blit(enemy_img, enemy)
            
            for bullet in bullets:
                if use_bullet_image and bullet_img:
                    screen.blit(bullet_img, bullet)
                else:
                    pygame.draw.rect(screen, ORANGE, bullet)
            for bullet in shooter_bullets:
                pygame.draw.rect(screen, RED, bullet)
            
            screen.blit(player_img, player)
            
            lives_text = render_hearts(lives)
            screen.blit(lives_text, (WIDTH - (HEART_SIZE * lives + 20), 10))
        else:
            restart_button_rect, restart_text, restart_text_rect = create_button(
                WIDTH//2 - BUTTON_WIDTH//2,
                HEIGHT//2 + 20,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Restart Game"
            )
            
            mouse_pos = pygame.mouse.get_pos()
            button_color = BUTTON_HOVER_COLOR if is_button_clicked(restart_button_rect, mouse_pos) else BUTTON_COLOR
            
            pygame.draw.rect(screen, button_color, restart_button_rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, restart_button_rect, 2, border_radius=10)
            screen.blit(restart_text, restart_text_rect)
            
            game_over_text = font.render("Game Over!", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
            screen.blit(game_over_text, game_over_rect)
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 35))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
