# WoW Survivors

A Vampire Survivors-like roguelite game featuring World of Warcraft classes and abilities, built with Pygame.

![WoW Survivors Game](https://via.placeholder.com/800x400?text=WoW+Survivors+Game)

## 🎮 Game Overview

WoW Survivors is an action-packed survival game inspired by Vampire Survivors, where you choose from classic World of Warcraft classes and battle against waves of enemies. Level up, unlock powerful abilities, and see how long you can survive!

### Features

- **5 Playable Classes**: Choose from Warrior, Mage, Hunter, Priest, and Paladin
- **Unique Abilities**: Each class has 5 distinct abilities with different effects
- **Roguelite Progression**: Collect coins during runs to purchase permanent upgrades
- **Auto-Combat System**: Your character automatically attacks while you focus on movement
- **Boss Encounters**: Face a powerful boss after surviving for 60 seconds
- **Pickup System**: Collect health and damage boosts during gameplay

## 🎲 Classes & Abilities

### Warrior
- **Berserker Rage**: Area damage over time with movement speed boost
- **Cleave**: Area damage to nearby enemies
- **Battle Cry**: Passive damage and speed boost
- **War Cry**: Passive damage and speed boost
- **Whirlwind**: Large area damage over time

### Mage
- **Frost Nova**: Area slow effect with damage over time
- **Arcane Explosion**: Area damage to nearby enemies
- **Mana Burst**: Passive damage boost
- **Chain Lightning**: Area damage over time
- **Mana Shield**: Reduces incoming damage

### Hunter
- **Trap**: Area slow effect
- **Focus Shot**: Passive damage boost
- **Eagle Eye**: Increases attack range
- **Rapid Fire**: Reduces attack cooldown
- **Camouflage**: Temporary invisibility to enemies

### Priest
- **Divine Shield**: Protective area effect
- **Healing Wave**: Periodic healing
- **Holy Smite**: Area damage over time
- **Renew**: Healing over time
- **Purify**: Temporary speed boost

### Paladin
- **Consecration**: Area damage over time
- **Judgment**: Passive damage boost
- **Divine Protection**: Protective area effect
- **Shield of the Righteous**: Reduces incoming damage
- **Hammer of Justice**: Area damage with slow effect

## 🎯 How to Play

1. **Start Game**: Launch the game and press any key to start
2. **Select Class**: Choose from 5 WoW classes, each with unique abilities
3. **Movement**: Use arrow keys to move your character
4. **Combat**: Your character attacks automatically
5. **Level Up**: Gain XP by defeating enemies and choose new abilities when leveling up
6. **Collect Items**: Gather coins and pickups to become stronger
7. **Survive**: Try to survive as long as possible against increasingly difficult waves
8. **Shop**: Spend coins on permanent upgrades between runs

## 🛠️ Requirements

- Python 3.x
- Pygame

## 📥 Installation

1. Clone this repository:
```bash
git clone https://github.com/Paladin92/wow-survivors.git
```

2. Navigate to the project directory:
```bash
cd wow-survivors
```

3. Install Pygame if you don't have it:
```bash
pip install pygame
```

4. Run the game:
```bash
python main.py
```

## 🎛️ Controls

- **Arrow Keys**: Move your character
- **P**: Pause game
- **1-5**: Select options in menus

## 🔄 Game Loop

1. **Menu Screen**: Start game and select class
2. **Gameplay**: Move, attack, collect items, and level up
3. **Level Up**: Choose from 3 random abilities when gaining a level
4. **Game Over**: When your health reaches zero
5. **Shop**: Spend coins on permanent upgrades
6. **Repeat**: Start a new run with your permanent upgrades

## 🚀 Future Enhancements

- Additional classes and abilities
- More enemy types and bosses
- Enhanced graphics and sound effects
- Talent tree system
- Difficulty settings
- Leaderboards

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Inspired by Vampire Survivors
- World of Warcraft for class and ability concepts
- Pygame community for the game framework