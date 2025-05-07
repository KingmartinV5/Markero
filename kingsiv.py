import pygame
import random
import sys

pygame.init()

# Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KingsIV")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20)

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARKGRAY = (30, 30, 30)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game variables
graphics_levels = ["Low", "Medium", "High", "High-Ultra", "Ultra"]
graphics_index = 2  # Default: High
cheats_enabled = False
current_weapon = 0
weapons = ["Square Blaster", "Circle Cannon"]

# Player
player = pygame.Rect(WIDTH//2, HEIGHT//2, 30, 30)
player_speed = 3

# NPCs
npcs = [pygame.Rect(random.randint(100, 700), random.randint(100, 500), 30, 30) for _ in range(5)]
npc_dialogues = ["How's your day?", "Nice weather huh?", "Seen any ghosts?", "Pizza or burgers?"]

# Buildings
buildings = [pygame.Rect(random.randint(0, WIDTH-60), random.randint(0, HEIGHT-60), 60, 60) for _ in range(8)]

# Bullets
bullets = []

# Blood effects
blood_splats = []

# States
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_SETTINGS = "settings"
STATE_CREDITS = "credits"
state = STATE_MENU

menu_options = ["Play", "Settings", "Credits"]
menu_index = 0

def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

def handle_bullets():
    global npcs
    for bullet in bullets[:]:
        bullet['rect'].x += bullet['dir'][0]
        bullet['rect'].y += bullet['dir'][1]
        if not screen.get_rect().colliderect(bullet['rect']):
            bullets.remove(bullet)
            continue
        for npc in npcs[:]:
            if bullet['rect'].colliderect(npc):
                blood_splats.append((npc.centerx, npc.centery))
                npcs.remove(npc)
                if bullet in bullets:
                    bullets.remove(bullet)

def draw_game():
    screen.fill((30, 80, 30) if graphics_index < 2 else (60, 160, 60))  # grass color by graphics level

    for building in buildings:
        pygame.draw.rect(screen, GRAY, building)

    pygame.draw.rect(screen, BLUE, player)

    for npc in npcs:
        pygame.draw.rect(screen, YELLOW, npc)

    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet['rect'])

    for blood in blood_splats:
        pygame.draw.circle(screen, RED, blood, 10)

def draw_menu():
    screen.fill(BLACK)
    draw_text("KingsIV - Main Menu", 300, 50, WHITE)
    for i, option in enumerate(menu_options):
        color = GREEN if i == menu_index else WHITE
        draw_text(option, 360, 150 + i * 40, color)
    draw_text("Press C to activate cheats", 280, 400, RED if cheats_enabled else WHITE)

def draw_settings():
    screen.fill(DARKGRAY)
    draw_text("Graphics Settings", 330, 50)
    draw_text(f"Graphics: {graphics_levels[graphics_index]}", 300, 150, WHITE)
    draw_text("Use LEFT/RIGHT to change, ESC to return", 220, 300, GRAY)

def draw_credits():
    screen.fill(BLACK)
    draw_text("KingsIV - Credits", 320, 50)
    draw_text("Owner: KingMartin", 300, 130)
    draw_text("Game Associate Developer: ChatGPT", 230, 160)
    draw_text("Director 1: Kuko145", 300, 210)
    draw_text("Director 2: Inatable", 300, 240)
    draw_text("Director 3: Mathias Krundek", 260, 270)
    draw_text("Press ESC to return", 300, 400, GRAY)

def save_game():
    """Save the player's position and other relevant data to a file."""
    with open('save_game.txt', 'w') as file:
        file.write(f'{player.x},{player.y}\n')
        file.write(f'{graphics_index}\n')
        file.write(f'{cheats_enabled}\n')

def load_game():
    """Load the player's position and other saved data from a file."""
    global player, graphics_index, cheats_enabled
    try:
        with open('save_game.txt', 'r') as file:
            x, y = map(int, file.readline().strip().split(','))
            player.x, player.y = x, y
            graphics_index = int(file.readline().strip())
            cheats_enabled = file.readline().strip() == 'True'
    except FileNotFoundError:
        pass

def check_collisions():
    """Prevent the player from walking through buildings."""
    for building in buildings:
        if player.colliderect(building):
            return True
    return False

# Game loop
running = True
load_game()  # Try to load the game when the program starts

while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[menu_index] == "Play":
                        state = STATE_GAME
                    elif menu_options[menu_index] == "Settings":
                        state = STATE_SETTINGS
                    elif menu_options[menu_index] == "Credits":
                        state = STATE_CREDITS
                elif event.key == pygame.K_c:
                    cheats_enabled = not cheats_enabled

        elif state == STATE_SETTINGS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    graphics_index = max(0, graphics_index - 1)
                elif event.key == pygame.K_RIGHT:
                    graphics_index = min(len(graphics_levels) - 1, graphics_index + 1)
                elif event.key == pygame.K_ESCAPE:
                    state = STATE_MENU

        elif state == STATE_CREDITS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = STATE_MENU

        elif state == STATE_GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB and cheats_enabled:
                    current_weapon = (current_weapon + 1) % len(weapons)
            if event.type == pygame.MOUSEBUTTONDOWN and cheats_enabled:
                mx, my = pygame.mouse.get_pos()
                dx = mx - player.centerx
                dy = my - player.centery
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist == 0: dist = 1
                direction = (dx / dist * 6, dy / dist * 6)
                bullets.append({
                    'rect': pygame.Rect(player.centerx, player.centery, 8, 8),
                    'dir': direction
                })

    if state == STATE_GAME:
        if keys[pygame.K_w]: player.y -= player_speed
        if keys[pygame.K_s]: player.y += player_speed
        if keys[pygame.K_a]: player.x -= player_speed
        if keys[pygame.K_d]: player.x += player_speed

        # Prevent the player from moving through buildings
        if check_collisions():
            if keys[pygame.K_w]: player.y += player_speed
            if keys[pygame.K_s]: player.y -= player_speed
            if keys[pygame.K_a]: player.x += player_speed
            if keys[pygame.K_d]: player.x -= player_speed

        handle_bullets()
        draw_game()

    elif state == STATE_MENU:
        draw_menu()

    elif state == STATE_SETTINGS:
        draw_settings()

    elif state == STATE_CREDITS:
        draw_credits()

    pygame.display.flip()
    clock.tick(60)

# Save the game state on exit
save_game()

pygame.quit()
sys.exit()
