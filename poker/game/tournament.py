# poker/game/tournament.py  — MINIMAL stub for Task 4 tests
# Full implementation comes in Task 5
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from poker.game.deck import Card


class PlayerStatus(Enum):
    ACTIVE = 'active'
    FOLDED = 'folded'
    ALL_IN = 'all_in'
    ELIMINATED = 'eliminated'


@dataclass
class Player:
    sid: str
    name: str
    seat: int
    chips: int = 1000
    hole_cards: list[Card] = field(default_factory=list)
    ready: bool = False
    status: PlayerStatus = PlayerStatus.ACTIVE
    total_bet_in_hand: int = 0
    street_bet: int = 0
    disconnected_at: Optional[float] = None
