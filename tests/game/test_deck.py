import pytest
from poker.game.deck import Card, Deck, SUITS, RANKS


def test_card_equality():
    assert Card(rank=14, suit='h') == Card(rank=14, suit='h')
    assert Card(rank=14, suit='h') != Card(rank=13, suit='h')


def test_deck_has_52_cards():
    deck = Deck()
    assert len(deck) == 52


def test_deck_cards_are_unique():
    deck = Deck()
    all_cards = deck.deal(52)
    assert len(set(all_cards)) == 52


def test_deck_deals_requested_count():
    deck = Deck()
    cards = deck.deal(5)
    assert len(cards) == 5
    assert len(deck) == 47


def test_deck_raises_when_empty():
    deck = Deck()
    deck.deal(52)
    with pytest.raises(ValueError, match="Not enough cards"):
        deck.deal(1)


def test_deck_is_shuffled():
    # Two decks in sequence order should differ (astronomically unlikely to be equal)
    d1 = Deck()
    d2 = Deck()
    cards1 = d1.deal(52)
    cards2 = d2.deal(52)
    assert cards1 != cards2
