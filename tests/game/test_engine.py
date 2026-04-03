import pytest
from poker.game.engine import calculate_pots, Pot


def make_contrib(sid: str, total_bet: int, folded: bool = False) -> dict:
    return {'sid': sid, 'total_bet': total_bet, 'folded': folded}


def test_no_side_pot_when_all_equal():
    contribs = [
        make_contrib('a', 100),
        make_contrib('b', 100),
        make_contrib('c', 100),
    ]
    pots = calculate_pots(contribs)
    assert len(pots) == 1
    assert pots[0].amount == 300
    assert set(pots[0].eligible_sids) == {'a', 'b', 'c'}


def test_side_pot_when_short_stack_all_in():
    # a: all-in 50, b: 100, c: 100
    contribs = [
        make_contrib('a', 50),   # all-in
        make_contrib('b', 100),
        make_contrib('c', 100),
    ]
    pots = calculate_pots(contribs)
    assert len(pots) == 2
    main_pot = next(p for p in pots if set(p.eligible_sids) == {'a', 'b', 'c'})
    side_pot = next(p for p in pots if set(p.eligible_sids) == {'b', 'c'})
    assert main_pot.amount == 150   # 50 × 3
    assert side_pot.amount == 100   # 50 × 2


def test_folded_player_contributes_to_pot_but_not_eligible():
    # a: 100 (folded), b: 100, c: 100
    contribs = [
        make_contrib('a', 100, folded=True),
        make_contrib('b', 100),
        make_contrib('c', 100),
    ]
    pots = calculate_pots(contribs)
    assert len(pots) == 1
    assert pots[0].amount == 300
    assert set(pots[0].eligible_sids) == {'b', 'c'}


def test_multiple_all_ins():
    # a: 50 (all-in), b: 150 (all-in), c: 300
    contribs = [
        make_contrib('a', 50),
        make_contrib('b', 150),
        make_contrib('c', 300),
    ]
    pots = calculate_pots(contribs)
    assert len(pots) == 3
    total = sum(p.amount for p in pots)
    assert total == 500  # 50+150+300


from poker.game.engine import Hand
from poker.game.tournament import Player, PlayerStatus


def make_player(sid: str, name: str, seat: int, chips: int = 1000) -> Player:
    return Player(sid=sid, name=name, seat=seat, chips=chips,
                  status=PlayerStatus.ACTIVE)


def test_hand_deals_two_cards_per_player():
    players = [make_player('a', 'Alice', 0), make_player('b', 'Bob', 1)]
    hand = Hand(players=players, dealer_pos=0, small_blind=25, big_blind=50)
    hand.deal()
    for p in players:
        assert len(p.hole_cards) == 2


def test_hand_posts_blinds():
    players = [make_player('a', 'Alice', 0, chips=1000),
               make_player('b', 'Bob', 1, chips=1000)]
    hand = Hand(players=players, dealer_pos=0, small_blind=25, big_blind=50)
    hand.deal()
    # In heads-up: dealer = SB, other = BB
    total_posted = sum(p.total_bet_in_hand for p in players)
    assert total_posted == 75  # 25 + 50


def test_hand_fold_wins_pot():
    players = [make_player('a', 'Alice', 0, chips=1000),
               make_player('b', 'Bob', 1, chips=1000)]
    hand = Hand(players=players, dealer_pos=0, small_blind=25, big_blind=50)
    hand.deal()
    # Alice folds → Bob wins blinds
    result = hand.apply_action('a', 'fold')
    assert result['winners'][0]['sid'] == 'b'
    assert result['winners'][0]['amount'] == 75
