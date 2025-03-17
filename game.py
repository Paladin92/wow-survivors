import pygame
import random
import sys
from settings import *
from utils import draw_text, draw_background, apply_upgrade
from sprites import Player, Enemy, Boss, Projectile, Coin, Pickup, Ability
from ui import show_menu, class_selection_screen, show_upgrade_menu, show_game_over, show_shop, handle_pause, draw_hud

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 36)
        self.game_state = "menu"  # "menu", "playing", "upgrade", "shop", "paused", "game_over"
        self.player = None
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.pickup_group = pygame.sprite.Group()
        self.ability_list = []
        self.enemy_spawn_timer = 0
        self.pickup_spawn_timer = 0
        self.game_start_time = 0
        self.current_upgrades = []  # holds upgrade options during level-up
        self.run_timer = 0
        self.boss_spawned = False
        self.boss = None
        
    def reset_game(self):
        """Reset game state for a new run."""
        self.player_group.empty()
        self.enemy_group.empty()
        self.projectile_group.empty()
        self.coin_group.empty()
        self.pickup_group.empty()
        self.ability_list.clear()
        self.enemy_spawn_timer = 0
        self.pickup_spawn_timer = 0
        self.run_timer = 0
        self.boss_spawned = False
        self.boss = None
        self.game_start_time = pygame.time.get_ticks()
        
    def initialize_player(self, selected_class):
        """Initialize player with selected class."""
        self.player = Player(WIDTH//2, HEIGHT//2, selected_class)
        self.player_group = pygame.sprite.Group(self.player)
        self.player.periodic_upgrades = {}
        self.player.xp = 0
        self.player.level = 1
        global score
        score = 0
        
    def handle_menu(self):
        """Handle menu state."""
        show_menu(self.screen)
        selected_class = class_selection_screen(self.screen)
        self.reset_game()
        self.initialize_player(selected_class)
        self.game_state = "playing"
        
    def handle_playing(self):
        """Handle playing state."""
        dt = self.clock.tick(60)  # dt in ms
        self.run_timer += dt
        elapsed_time = self.run_timer
        current_time = pygame.time.get_ticks()
        current_spawn_interval = max(200, 1000 - (elapsed_time // 10000) * 100)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game_state = "paused"
        
        # Update player
        keys = pygame.key.get_pressed()
        self.player_group.update(keys)
        
        # Auto-shoot
        new_projectiles = self.player.auto_shoot(self.enemy_group)
        for proj in new_projectiles:
            self.projectile_group.add(proj)
        
        # Update entities
        for enemy in self.enemy_group:
            enemy.update(self.player, dt)
        self.projectile_group.update()
        self.coin_group.update()
        self.pickup_group.update()
        
        # Spawn pickups
        self.pickup_spawn_timer += dt
        if self.pickup_spawn_timer >= PICKUP_SPAWN_INTERVAL:
            self.pickup_spawn_timer -= PICKUP_SPAWN_INTERVAL
            self.pickup_group.add(Pickup(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50),
                                "health" if random.random() < 0.7 else "damage"))
        
        # Handle projectile collisions
        for proj in self.projectile_group:
            hits = pygame.sprite.spritecollide(proj, self.enemy_group, False)
            for enemy in hits:
                enemy.health -= proj.damage
                if enemy.health <= 0:
                    enemy.kill()
                    self.player.xp += XP_PER_ENEMY
                    global score
                    score += 100
                    if random.random() < 0.5:
                        self.coin_group.add(Coin(enemy.rect.centerx, enemy.rect.centery))
                proj.kill()
        
        # Handle pickup collisions
        for pickup in pygame.sprite.spritecollide(self.player, self.pickup_group, True):
            if pickup.pickup_type == "health":
                self.player.health = min(self.player.max_health, self.player.health + 20)
                score += 50
            elif pickup.pickup_type == "damage":
                self.player.damage += 0.2
                score += 50
        
        # Handle abilities
        for ability in self.ability_list:
            for enemy in self.enemy_group:
                dx = enemy.rect.centerx - ability.x
                dy = enemy.rect.centery - ability.y
                if math.hypot(dx, dy) <= ability.radius:
                    if ability.effect_type == "berserker_rage":
                        enemy.health -= 0.05 * dt
                    elif ability.effect_type == "frost_nova":
                        enemy.slow_timer = max(enemy.slow_timer, 1000)
                        enemy.health -= 0.02 * dt
                    elif ability.effect_type == "trap":
                        enemy.slow_timer = max(enemy.slow_timer, 1500)
                        if ability in self.ability_list:
                            self.ability_list.remove(ability)
                    elif ability.effect_type == "consecration":
                        enemy.health -= 0.03 * dt
                    elif ability.effect_type == "arcane_explosion":
                        enemy.health -= 0.04 * dt
                    elif ability.effect_type == "holy_smite":
                        enemy.health -= 0.04 * dt
                    elif ability.effect_type == "whirlwind":
                        enemy.health -= 0.06 * dt
                    elif ability.effect_type == "chain_lightning":
                        enemy.health -= 0.05 * dt
                    elif ability.effect_type == "hammer_of_justice":
                        enemy.health -= 0.05 * dt
                        enemy.slow_timer = max(enemy.slow_timer, 2000)
                    elif ability.effect_type == "renew":
                        self.player.health = min(self.player.max_health, self.player.health + 0.03 * dt)
                    if enemy.health <= 0:
                        enemy.kill()
                        self.player.xp += XP_PER_ENEMY
                        score += 100
                        if random.random() < 0.5:
                            self.coin_group.add(Coin(enemy.rect.centerx, enemy.rect.centery))
        
        # Trigger periodic abilities
        for effect, info in self.player.periodic_upgrades.items():
            if current_time - info["last_trigger"] >= info["cooldown"]:
                upgrade = info["upgrade"]
                attached = effect in ["berserker_rage", "divine_shield"]
                ability = Ability(
                    effect_type=upgrade["effect"],
                    x=self.player.rect.centerx,
                    y=self.player.rect.centery,
                    radius=upgrade.get("radius", 50),
                    duration=upgrade.get("duration", 2000),
                    attached=attached,
                    owner=self.player if attached else None
                )
                self.ability_list.append(ability)
                info["last_trigger"] = current_time
        
        # Update abilities
        for ability in self.ability_list[:]:
            ability.update(dt)
            if not ability.is_active():
                self.ability_list.remove(ability)
        
        # Spawn enemies
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= current_spawn_interval:
            self.enemy_spawn_timer -= current_spawn_interval
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                x = random.randint(0, WIDTH)
                y = 0
            elif side == "bottom":
                x = random.randint(0, WIDTH)
                y = HEIGHT
            elif side == "left":
                x = 0
                y = random.randint(0, HEIGHT)
            else:
                x = WIDTH
                y = random.randint(0, HEIGHT)
            r = random.random()
            if r < 0.05:
                health = 5
            elif r < 0.30:
                health = 3
            else:
                health = 1
            self.enemy_group.add(Enemy(x, y, health))
        
        # Spawn boss
        if self.run_timer >= BOSS_SPAWN_TIME and not self.boss_spawned:
            self.boss = Boss(WIDTH//2, 0)
            self.enemy_group.add(self.boss)
            self.boss_spawned = True
        
        # Handle player-enemy collisions
        if not self.player.camouflage:
            collisions = pygame.sprite.spritecollide(self.player, self.enemy_group, True)
            if collisions:
                damage = 20 * len(collisions) * (1 - self.player.damage_reduction)
                self.player.health -= damage
                if self.player.health <= 0:
                    self.game_state = "game_over"
        
        # Handle coin collection
        coin_hits = pygame.sprite.spritecollide(self.player, self.coin_group, True)
        for coin in coin_hits:
            global coin_count
            coin_count += coin.value
        
        # Level up
        if self.player.xp >= self.player.level * XP_THRESHOLD_FACTOR:
            self.game_state = "upgrade"
            possible = upgrades_dict.get(self.player.class_type, [])
            if len(possible) >= 5:
                self.current_upgrades = random.sample(possible, 3)
            else:
                self.current_upgrades = possible
        
        # Check for boss defeat
        if self.boss_spawned and self.boss not in self.enemy_group:
            coin_count += 10
            self.game_state = "shop"
        
        # Draw everything
        self.draw_game()
        
    def handle_upgrade(self):
        """Handle upgrade state."""
        show_upgrade_menu(self.screen, self.current_upgrades)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    index = event.key - pygame.K_1
                    if index < len(self.current_upgrades):
                        apply_upgrade(self.player, self.current_upgrades[index], pygame.time.get_ticks())
                        self.player.level += 1
                        self.player.xp = 0
                        self.game_state = "playing"
        
    def handle_shop(self):
        """Handle shop state."""
        show_shop(self.screen)
        self.game_state = "menu"
        
    def handle_game_over(self):
        """Handle game over state."""
        show_game_over(self.screen, self.player)
        self.game_state = "shop"
        
    def handle_pause(self):
        """Handle pause state."""
        handle_pause(self.screen)
        self.game_state = "playing"
        
    def draw_game(self):
        """Draw all game elements."""
        draw_background(self.screen)
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.projectile_group.draw(self.screen)
        self.coin_group.draw(self.screen)
        self.pickup_group.draw(self.screen)
        
        for ability in self.ability_list:
            ability.draw(self.screen)
        
        draw_hud(self.screen, self.player)
        
        for enemy in self.enemy_group:
            if hasattr(enemy, "draw_health_bar"):
                enemy.draw_health_bar(self.screen)
        
    def run(self):
        """Main game loop handler."""
        if self.game_state == "menu":
            self.handle_menu()
        elif self.game_state == "playing":
            self.handle_playing()
        elif self.game_state == "upgrade":
            self.handle_upgrade()
        elif self.game_state == "shop":
            self.handle_shop()
        elif self.game_state == "game_over":
            self.handle_game_over()
        elif self.game_state == "paused":
            self.handle_pause()