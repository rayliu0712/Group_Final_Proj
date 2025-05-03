from enum import Enum


class DiffLevel(Enum):
    EASY = 0
    HARD = 1
    MASTER = 2


class Character(Enum):
    WARRIOR = 'WARRIOR'
    ARCHER = 'ARCHER'


class CardType(Enum):
    ATTACK = 0
    DEFENSE = 1


cards = [
    {"type": "Attack", "name": "Attack1", "color": (255, 100, 100)},
    {"type": "Attack", "name": "Attack2", "color": (255, 100, 100)},
    {"type": "Attack", "name": "Attack3", "color": (255, 100, 100)},
    {"type": "Attack", "name": "Attack4", "color": (255, 100, 100)},
    {"type": "Attack", "name": "Attack5", "color": (255, 100, 100)},
    {"type": "Defense", "name": "Defense1", "color": (100, 100, 255)},
    {"type": "Defense", "name": "Defense2", "color": (100, 100, 255)},
    {"type": "Defense", "name": "Defense3", "color": (100, 100, 255)},
    {"type": "Defense", "name": "Defense4", "color": (100, 100, 255)},
    {"type": "Defense", "name": "Defense5", "color": (100, 100, 255)},
    {"type": "Special", "name": "Special1", "color": (100, 255, 100)},
    {"type": "Special", "name": "Special2", "color": (100, 255, 100)},
]
