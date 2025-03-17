import pygame
import math
from settings import *
from utils import calculate_distance, calculate_angle

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, class_type):
        super().__init__()
        self.class_type = class_type
        data = class_data.get(class_type, class_data["Warrior"])
        self.max_health = data["health"] + permanent_upgrades.get("bonus_health", 0)
        self.health = self.max_health
        self.speed = data["speed"] + permanent_upgrades.get("bonus_speed", 0)
        self.damage = data["damage"] + permanent_upgrades.get("bonus_damage", 0)
        self.fire_rate = data["fire_rate"]
        self.color = data["color"]
        self.pattern = data["pattern"]
        self.last_shot = pygame.time.get_ticks()
        self.xp = 0
        self.level = 1
        self.invulnerable = False
        self.periodic_upgrades = {}
        self.mana_shield = False
        self.camouflage = False
        self.camouflage_timer = 0
        self.purify = False
        self.purify_timer = 0
        self.damage_reduction = 0
        self.slow_timer = 0
        self.image = pygame.Surface((30, 30))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self, keys_pressed):
        if self.camouflage:
            self.camouflage_timer -= pygame.time.get_ticks() - self._last_update
            if self.camouflage_timer <= 0:
                self.camouflage = False
        if self.purify:
            self.purify_timer -= pygame.time.get_ticks() - self._last_update
            if self.purify_timer <= 0:
                self.purify = False
        if self.slow_timer > 0:
            self.slow_timer -= pygame.time.get_ticks() - self._last_update
            if self.slow_timer < 0:
                self.slow_timer = 0
                
        self._last_update = pygame.time.get_ticks()
        
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        
    def find_nearest_enemy(self, enemy_group):
        nearest = None
        min_dist = float("inf")
        for enemy in enemy_group:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        return nearest, min_dist
        
    def auto_shoot(self, enemy_group):
        projectiles = []
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            self.last_shot = now
            if self.pattern == "8_directions":
                for i in range(8):
                    angle = i * (2 * math.pi / 8)
                    projectiles.append(Projectile(self.rect.centerx, self.rect.centery, angle, self.damage))
            elif self.pattern == "4_directions":
                for i in range(4):
                    angle = i * (2 * math.pi / 4)
                    projectiles.append(Projectile(self.rect.centerx, self.rect.centery, angle, self.damage))
            elif self.pattern == "6_directions":
                for i in range(6):
                    angle = i * (2 * math.pi / 6)
                    projectiles.append(Projectile(self.rect.centerx, self.rect.centery, angle, self.damage))
            elif self.pattern == "aimed":
                nearest, _ = self.find_nearest_enemy(enemy_group)
                if nearest:
                    dx = nearest.rect.centerx - self.rect.centerx
                    dy = nearest.rect.centery - self.rect.centery
                    angle = math.atan2(dy, dx)
                    projectiles.append(Projectile(self.rect.centerx, self.rect.centery, angle, self.damage))
                else:
                    for i in range(8):
                        angle = i * (2 * math.pi / 8)
                        projectiles.append(Projectile(self.rect.centerx, self.rect.centery, angle, self.damage))
            else:
                for i in range(8):
                    angle = i * (2 * math.pi / 8)
                    projectiles.append(Projectile(self.rect.centerx, self.rect.centery, angle, self.damage))
        return projectiles

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=1):
        super().__init__()
        self.max_health = float(health)
        self.health = float(health)
        self.image = pygame.Surface((20, 20))
        if self.max_health == 1:
            self.image.fill((255, 0, 0))
        elif self.max_health == 3:
            self.image.fill((255, 165, 0))
        else:
            self.image.fill((128, 0, 128))
        self.rect = self.image.get_rect(center=(x, y))
        self.slow_timer = 0
        self._last_update = pygame.time.get_ticks()
        
    def update(self, player, dt):
        current_time = pygame.time.get_ticks()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance:
            dx, dy = dx / distance, dy / distance
        speed = ENEMY_BASE_SPEED
        if self.slow_timer > 0:
            speed *= 0.5
            self.slow_timer -= dt
            if self.slow_timer < 0:
                self.slow_timer = 0
        self.rect.x += dx * speed
        self.rect.y += dy * speed
        
    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 3
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 5, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 5, fill, bar_height)
        pygame.draw.rect(surface, (0, 255, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=50)
        self.image = pygame.Surface((60, 60))
        self.image.fill((128, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self, player, dt):
        current_time = pygame.time.get_ticks()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance:
            dx, dy = dx / distance, dy / distance
        speed = ENEMY_BASE_SPEED * 0.8
        if self.slow_timer > 0:
            speed *= 0.5
            self.slow_timer -= dt
            if self.slow_timer < 0:
                self.slow_timer = 0
        self.rect.x += dx * speed
        self.rect.y += dy * speed

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, damage):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 7
        self.damage = damage
        
    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, value=1):
        super().__init__()
        self.value = value
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 223, 0))
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        pass

class Pickup(pygame.sprite.Sprite):
    def __init__(self, x, y, pickup_type):
        super().__init__()
        self.pickup_type = pickup_type  # "health" or "damage"
        self.image = pygame.Surface((15, 15))
        if self.pickup_type == "health":
            self.image.fill((0, 255, 0))
        elif self.pickup_type == "damage":
            self.image.fill((255, 0, 255))
        else:
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        pass

class Ability:
    def __init__(self, effect_type, x, y, radius, duration, attached=False, owner=None):
        self.effect_type = effect_type
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration  # in ms
        self.timer = duration
        self.attached = attached
        self.owner = owner
        color_map = {
            "berserker_rage": (255, 69, 0),
            "frost_nova": (173, 216, 230),
            "trap": (139, 69, 19),
            "divine_shield": (255, 255, 0),
            "consecration": (255, 255, 255),
            "arcane_explosion": (138, 43, 226),
            "holy_smite": (255, 105, 180),
            "whirlwind": (255, 140, 0),
            "chain_lightning": (75, 0, 130),
            "renew": (144, 238, 144),
            "hammer_of_justice": (220, 20, 60)
        }
        self.color = color_map.get(effect_type, (255, 255, 255))
        self._last_update = pygame.time.get_ticks()
        
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        dt = current_time - self._last_update
        self._last_update = current_time
        
        self.timer -= dt
        if self.attached and self.owner:
            self.x, self.y = self.owner.rect.center
            
    def is_active(self):
        return self.timer > 0
        
    def draw(self, surface):
        s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        alpha = int(128 * (self.timer / self.duration))
        pygame.draw.circle(s, (*self.color, alpha), (self.radius, self.radius), self.radius)
        surface.blit(s, (self.x - self.radius, self.y - self.radius))