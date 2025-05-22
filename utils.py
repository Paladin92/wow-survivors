import pygame
import math

def draw_text(surface, text, size, color, x, y):
    """Renders text onto the given surface."""
    font_obj = pygame.font.Font(None, size)
    text_surface = font_obj.render(text, True, color)
    surface.blit(text_surface, (x, y))

def apply_upgrade(player, upgrade, current_time):
    """
    Applies an upgrade to the player.
    For periodic upgrades, add them to player.periodic_upgrades;
    for immediate upgrades, apply their effects directly.
    """
    if upgrade.get("periodic", False):
        player.periodic_upgrades[upgrade["effect"]] = {
            "last_trigger": current_time,
            "cooldown": upgrade.get("cooldown", 5000),
            "upgrade": upgrade
        }
    else:
        # Example immediate upgrade handling based on the effect type
        if upgrade["effect"] == "buff":
            player.damage += upgrade.get("damage_buff", 0)
            player.speed += upgrade.get("speed_buff", 0)
        elif upgrade["effect"] == "war_cry":
            player.damage += upgrade.get("damage_buff", 0)
            player.speed += upgrade.get("speed_buff", 0)
        elif upgrade["effect"] == "camouflage":
            player.camouflage = True
            player.camouflage_timer = upgrade.get("duration", 3000)
        elif upgrade["effect"] == "mana_shield":
            player.mana_shield = True
            player.base_damage_reduction += upgrade.get("damage_reduction", 0.2)
            player.damage_reduction = player.base_damage_reduction
        elif upgrade["effect"] == "rapid_fire":
            player.fire_rate = max(100, player.fire_rate - upgrade.get("reduction", 100))
        elif upgrade["effect"] == "eagle_eye":
            player.projectile_speed += upgrade.get("range_bonus", 2)
        elif upgrade["effect"] == "shield_of_the_righteous":
            player.base_damage_reduction += upgrade.get("damage_reduction", 0.15)
            player.damage_reduction = player.base_damage_reduction
        elif upgrade["effect"] == "purify":
            player.purify = True
            player.purify_timer = upgrade.get("duration", 2000)
        # Add further handling as needed for other upgrade types

def draw_background(surface):
    """Draws the game background."""
    surface.fill((30, 30, 30))

def calculate_distance(x1, y1, x2, y2):
    """Calculate distance between two points."""
    return math.hypot(x2 - x1, y2 - y1)

def calculate_angle(x1, y1, x2, y2):
    """Calculate angle between two points."""
    return math.atan2(y2 - y1, x2 - x1)