import pygame
import pytest
from sprites import Player
from utils import apply_upgrade
from settings import upgrades_dict


def test_apply_periodic_upgrade():
    pygame.init()
    player = Player(0, 0, "Warrior")
    upgrade = upgrades_dict["Warrior"][0]
    assert upgrade["periodic"] is True
    apply_upgrade(player, upgrade, current_time=0)
    assert upgrade["effect"] in player.periodic_upgrades
    pygame.quit()
