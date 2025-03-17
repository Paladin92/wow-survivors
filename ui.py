import pygame
import sys
from settings import *
from utils import draw_text, draw_background

def show_menu(screen):
    """Display the main menu screen."""
    draw_background(screen)
    draw_text(screen, "Welcome to WoW Survivor!", 64, (255, 255, 0), WIDTH//2 - 250, HEIGHT//2 - 150)
    draw_text(screen, "Press any key to start...", 36, (255, 255, 255), WIDTH//2 - 150, HEIGHT//2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def class_selection_screen(screen):
    """Display the class selection screen and return the selected class."""
    selecting = True
    selected_class = None
    instructions = [
        "Choose your class:",
        "1: Warrior",
        "2: Mage",
        "3: Hunter",
        "4: Priest",
        "5: Paladin"
    ]
    while selecting:
        draw_background(screen)
        for i, line in enumerate(instructions):
            draw_text(screen, line, 36, (255, 255, 255), WIDTH//2 - 150, 100 + i * 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_class = "Warrior"; selecting = False
                elif event.key == pygame.K_2:
                    selected_class = "Mage"; selecting = False
                elif event.key == pygame.K_3:
                    selected_class = "Hunter"; selecting = False
                elif event.key == pygame.K_4:
                    selected_class = "Priest"; selecting = False
                elif event.key == pygame.K_5:
                    selected_class = "Paladin"; selecting = False
    return selected_class

def show_upgrade_menu(screen, current_upgrades):
    """Display the upgrade selection menu after leveling up."""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    draw_text(screen, "LEVEL UP! Choose an upgrade:", 48, (255, 255, 0), WIDTH//2 - 250, HEIGHT//2 - 150)
    for i, upg in enumerate(current_upgrades, start=1):
        draw_text(screen, f"{i}: {upg['name']}", 36, (255, 255, 255), WIDTH//2 - 150, HEIGHT//2 - 50 + i * 40)
    pygame.display.flip()

def show_game_over(screen, player):
    """Display the game over screen."""
    draw_background(screen)
    draw_text(screen, "GAME OVER", 64, (255, 0, 0), WIDTH//2 - 150, HEIGHT//2 - 150)
    draw_text(screen, f"Final Level: {player.level}", 36, (255, 255, 255), WIDTH//2 - 100, HEIGHT//2 - 50)
    draw_text(screen, f"Coins Collected: {coin_count}", 36, (255, 255, 255), WIDTH//2 - 130, HEIGHT//2)
    draw_text(screen, "Press any key to enter the shop", 36, (255, 255, 255), WIDTH//2 - 200, HEIGHT//2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def show_shop(screen):
    """Display the shop screen between runs."""
    global coin_count, permanent_upgrades
    shop_items = [
        {"name": "Increase Max Health (+10)", "cost": 5, "key": pygame.K_1},
        {"name": "Increase Damage (+0.2)", "cost": 5, "key": pygame.K_2},
        {"name": "Increase Speed (+0.5)", "cost": 5, "key": pygame.K_3},
        {"name": "Finish Shopping", "cost": 0, "key": pygame.K_4}
    ]
    shopping = True
    while shopping:
        draw_background(screen)
        draw_text(screen, "SHOP - Spend your coins", 48, (255, 255, 0), WIDTH//2 - 250, 50)
        draw_text(screen, f"Coins: {coin_count}", 36, (255, 255, 255), WIDTH//2 - 100, 120)
        y_offset = 200
        for item in shop_items:
            draw_text(screen, f"{pygame.key.name(item['key']).upper()}: {item['name']} (Cost: {item['cost']})", 36, (255, 255, 255), WIDTH//2 - 200, y_offset)
            y_offset += 50
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                for item in shop_items:
                    if event.key == item["key"]:
                        if item["name"] == "Finish Shopping":
                            shopping = False
                        else:
                            if coin_count >= item["cost"]:
                                coin_count -= item["cost"]
                                if "Health" in item["name"]:
                                    permanent_upgrades["bonus_health"] += 10
                                elif "Damage" in item["name"]:
                                    permanent_upgrades["bonus_damage"] += 0.2
                                elif "Speed" in item["name"]:
                                    permanent_upgrades["bonus_speed"] += 0.5

def handle_pause(screen):
    """Handle the pause state."""
    paused = True
    draw_text(screen, "PAUSED", 64, (255, 255, 255), WIDTH//2 - 100, HEIGHT//2 - 50)
    draw_text(screen, "Press P to resume", 36, (255, 255, 255), WIDTH//2 - 130, HEIGHT//2 + 10)
    pygame.display.flip()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

def draw_hud(screen, player):
    """Draw the heads-up display during gameplay."""
    # Health bar
    health_bar_width = 200
    health_bar_height = 20
    fill = int((player.health / player.max_health) * health_bar_width)
    health_bar_rect = pygame.Rect(10, 10, health_bar_width, health_bar_height)
    fill_rect = pygame.Rect(10, 10, fill, health_bar_height)
    pygame.draw.rect(screen, (0, 255, 0), fill_rect)
    pygame.draw.rect(screen, (255, 255, 255), health_bar_rect, 2)
    
    # HUD text
    hud_text = f"Class: {player.class_type}  Health: {player.health:.0f}/{player.max_health}  XP: {player.xp}  Level: {player.level}  Coins: {coin_count}  Score: {score}"
    draw_text(screen, hud_text, 24, (255, 255, 255), 10, 40)