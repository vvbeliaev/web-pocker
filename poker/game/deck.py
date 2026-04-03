from __future__ import annotations
import random
from dataclasses import dataclass

SUITS: tuple[str, ...] = ('h', 'd', 'c', 's')  # hearts, diamonds, clubs, spades
RANKS: tuple[int, ...] = tuple(range(2, 15))    # 2–14 (14 = Ace)

SUIT_SYMBOLS = {'h': '♥', 'd': '♦', 'c': '♣', 's': '♠'}
RANK_SYMBOLS = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}


@dataclass(frozen=True)
class Card:
    rank: int   # 2–14
    suit: str   # 'h', 'd', 'c', 's'

    def to_dict(self) -> dict:
        return {'rank': self.rank, 'suit': self.suit,
                'rank_symbol': RANK_SYMBOLS[self.rank],
                'suit_symbol': SUIT_SYMBOLS[self.suit]}


class Deck:
    def __init__(self) -> None:
        self._cards: list[Card] = [Card(rank=r, suit=s) for r in RANKS for s in SUITS]
        random.shuffle(self._cards)

    def deal(self, n: int = 1) -> list[Card]:
        if len(self._cards) < n:
            raise ValueError(f"Not enough cards: need {n}, have {len(self._cards)}")
        dealt = self._cards[:n]
        self._cards = self._cards[n:]
        return dealt

    def __len__(self) -> int:
        return len(self._cards)
