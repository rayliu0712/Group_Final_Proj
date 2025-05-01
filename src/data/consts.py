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
