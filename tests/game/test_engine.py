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


def test_hand_call_advances_action():
    """After both players call/check, hand advances to flop."""
    players = [make_player('a', 'Alice', 0, chips=1000),
               make_player('b', 'Bob', 1, chips=1000)]
    hand = Hand(players=players, dealer_pos=0, small_blind=25, big_blind=50)
    hand.deal()
    # Heads-up preflop: dealer(Alice)=SB posted 25, Bob=BB posted 50
    # Action starts on Alice (left of BB in heads-up = dealer)
    # Alice calls (50 total)
    result = hand.apply_action('a', 'call')
    assert result is None  # hand continues
    # Bob checks (already at 50)
    result = hand.apply_action('b', 'call')
    assert result is None  # hand continues, now on flop
    assert hand.phase == 'flop'
    assert len(hand.community_cards) == 3


def test_hand_completes_all_streets():
    """A hand where both players check all streets reaches showdown."""
    players = [make_player('a', 'Alice', 0, chips=1000),
               make_player('b', 'Bob', 1, chips=1000)]
    hand = Hand(players=players, dealer_pos=0, small_blind=25, big_blind=50)
    hand.deal()
    # Preflop: Alice calls, Bob checks
    hand.apply_action('a', 'call')
    hand.apply_action('b', 'call')
    assert hand.phase == 'flop'
    # Flop: both check
    hand.apply_action('b', 'call')   # Bob acts first post-flop (left of dealer=Alice)
    hand.apply_action('a', 'call')
    assert hand.phase == 'turn'
    # Turn: both check
    hand.apply_action('b', 'call')
    hand.apply_action('a', 'call')
    assert hand.phase == 'river'
    # River: both check → showdown
    hand.apply_action('b', 'call')
    result = hand.apply_action('a', 'call')
    assert result is not None
    assert result['phase'] == 'showdown'
    assert len(result['winners']) >= 1
    assert len(hand.community_cards) == 5


def test_hand_raise_then_call():
    """Raise forces the other player to act again."""
    players = [make_player('a', 'Alice', 0, chips=1000),
               make_player('b', 'Bob', 1, chips=1000)]
    hand = Hand(players=players, dealer_pos=0, small_blind=25, big_blind=50)
    hand.deal()
    # Alice raises to 150
    result = hand.apply_action('a', 'raise', amount=150)
    assert result is None
    # Bob must now call/fold/raise (not auto-advance)
    assert hand.phase == 'preflop'
    # Bob calls → round ends, advance to flop
    result = hand.apply_action('b', 'call')
    assert result is None
    assert hand.phase == 'flop'


def test_all_in_ends_hand_when_called():
    """Player goes all-in, opponent calls (also goes all-in), hand runs to showdown."""
    players = [make_player('a', 'Alice', 0, chips=100),
               make_player('b', 'Bob', 1, chips=100)]
    hand = Hand(players=players, dealer_pos=0, small_blind=10, big_blind=20)
    hand.deal()
    # Alice goes all-in
    result = hand.apply_action('a', 'all_in')
    assert result is None
    # Bob calls all-in → no more active players, runs to showdown
    result = hand.apply_action('b', 'call')
    assert result is not None
    assert result['phase'] == 'showdown'
    total_awarded = sum(w['amount'] for w in result['winners'])
    assert total_awarded > 0
