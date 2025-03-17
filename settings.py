# Game window settings
WIDTH, HEIGHT = 800, 600

# Game mechanics settings
XP_PER_ENEMY = 10
XP_THRESHOLD_FACTOR = 100  # XP needed = level * this value
ENEMY_BASE_SPEED = 2       # Base enemy speed
BOSS_SPAWN_TIME = 60000    # Final boss spawns after 60 seconds
PICKUP_SPAWN_INTERVAL = 20000  # Spawn a pickup every 20 seconds

# Global variables that persist across runs
coin_count = 0
score = 0
permanent_upgrades = {"bonus_health": 0, "bonus_damage": 0, "bonus_speed": 0}

# Class data
class_data = {
    "Warrior":  {"health": 150, "speed": 5, "damage": 1.5, "fire_rate": 500, "color": (200, 0, 0), "pattern": "8_directions"},
    "Mage":     {"health": 80, "speed": 6, "damage": 2.0, "fire_rate": 400, "color": (0, 0, 255), "pattern": "4_directions"},
    "Hunter":   {"health": 100, "speed": 6, "damage": 1.2, "fire_rate": 450, "color": (0, 200, 0), "pattern": "aimed"},
    "Priest":   {"health": 90, "speed": 5, "damage": 1.0, "fire_rate": 600, "color": (220, 220, 220), "pattern": "8_directions"},
    "Paladin":  {"health": 130, "speed": 5, "damage": 1.3, "fire_rate": 550, "color": (255, 215, 0), "pattern": "6_directions"}
}

# Upgrades dictionary
upgrades_dict = {
    "Warrior": [
        {"name": "Berserker Rage", "effect": "berserker_rage", "periodic": True, "cooldown": 5000,
         "radius": 50, "duration": 2000, "damage_buff": 0.5, "speed_buff": 1},
        {"name": "Cleave", "effect": "arcane_explosion", "periodic": True, "cooldown": 4000,
         "radius": 40, "duration": 1500, "bonus_damage": 0.5},
        {"name": "Battle Cry", "effect": "buff", "periodic": False, "damage_buff": 0.3, "speed_buff": 0.5},
        {"name": "War Cry", "effect": "war_cry", "periodic": False, "damage_buff": 0.4, "speed_buff": 0.2},
        {"name": "Whirlwind", "effect": "whirlwind", "periodic": True, "cooldown": 6000,
         "radius": 60, "duration": 2500, "bonus_damage": 0.6}
    ],
    "Mage": [
        {"name": "Frost Nova", "effect": "frost_nova", "periodic": True, "cooldown": 5000,
         "radius": 100, "duration": 2000, "slow_factor": 0.5, "damage_over_time": 0.1},
        {"name": "Arcane Explosion", "effect": "arcane_explosion", "periodic": True, "cooldown": 4000,
         "radius": 80, "duration": 1500, "bonus_damage": 0.5},
        {"name": "Mana Burst", "effect": "buff", "periodic": False, "damage_buff": 0.4},
        {"name": "Chain Lightning", "effect": "chain_lightning", "periodic": True, "cooldown": 5500,
         "radius": 90, "duration": 2000, "bonus_damage": 0.5},
        {"name": "Mana Shield", "effect": "mana_shield", "periodic": False, "damage_reduction": 0.2}
    ],
    "Hunter": [
        {"name": "Trap", "effect": "trap", "periodic": True, "cooldown": 6000,
         "radius": 40, "duration": 3000, "slow_factor": 0.5},
        {"name": "Focus Shot", "effect": "buff", "periodic": False, "damage_buff": 0.5},
        {"name": "Eagle Eye", "effect": "buff", "periodic": False, "range_bonus": 10},
        {"name": "Rapid Fire", "effect": "rapid_fire", "periodic": False, "reduction": 100},
        {"name": "Camouflage", "effect": "camouflage", "periodic": False, "duration": 3000}
    ],
    "Priest": [
        {"name": "Divine Shield", "effect": "divine_shield", "periodic": True, "cooldown": 5000,
         "radius": 40, "duration": 2000},
        {"name": "Healing Wave", "effect": "healing_wave", "periodic": True, "cooldown": 5000,
         "heal_amount": 30},
        {"name": "Holy Smite", "effect": "holy_smite", "periodic": True, "cooldown": 5000,
         "radius": 60, "duration": 2000, "bonus_damage": 0.5},
        {"name": "Renew", "effect": "renew", "periodic": True, "cooldown": 5000,
         "duration": 3000, "heal_over_time": 0.03},
        {"name": "Purify", "effect": "purify", "periodic": False, "speed_buff": 1, "duration": 2000}
    ],
    "Paladin": [
        {"name": "Consecration", "effect": "consecration", "periodic": True, "cooldown": 5000,
         "radius": 75, "duration": 2500, "damage_over_time": 0.1},
        {"name": "Judgment", "effect": "buff", "periodic": False, "damage_buff": 0.5},
        {"name": "Divine Protection", "effect": "divine_protection", "periodic": True, "cooldown": 5000,
         "radius": 40, "duration": 2000},
        {"name": "Shield of the Righteous", "effect": "shield_of_the_righteous", "periodic": False, "damage_reduction": 0.15},
        {"name": "Hammer of Justice", "effect": "hammer_of_justice", "periodic": True, "cooldown": 6000,
         "radius": 50, "duration": 1500}
    ]
}