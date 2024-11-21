from behave import given, when, then
from card_game import Card, Deck, Player, Game
import random

# Шаги для сценария "Начало игры"
@given('колода перемешана')
def step_shuffle_deck(context):
    context.deck = Deck()
    context.deck.cards.reverse()

@given('каждому игроку раздано по 6 карт')
def step_deal_cards(context):
    context.attacker = Player("Алиса")
    context.defender = Player("Боб")
    context.attacker.hand = [context.deck.cards.pop() for _ in range(6)]
    context.defender.hand = [context.deck.cards.pop() for _ in range(6)]
    context.game = Game()
    context.game.set_players(context.attacker, context.defender)

# Шаги для сценария "Атака игрока"
@given('игрок "{player_name}" является атакующим')
def step_set_attacker(context, player_name):
    context.attacker = context.game.attacker
    assert context.attacker.name == player_name

@when('{player_name} выбирает карту "{rank} {suit}" для атаки')
def step_player_attacks(context, player_name, rank, suit):
    context.attacker = context.game.attacker
    card = context.attacker.find_card(suit, rank)
    assert card is not None, "Карта не найдена"
    context.attack_success = context.game.attack(card)

@then('карта "{rank} {suit}" должна быть положена на стол при атаке')
def step_attack_card_on_table(context, rank, suit):
    card_on_table = context.game.table_cards[-1]
    assert card_on_table.rank == rank and card_on_table.suit == suit

@then('карта должна быть удалена из руки {player_name} при атаке')
def step_card_removed_from_hand(context, player_name):
    assert context.attack_success
    assert len(context.attacker.hand) == 5  # Игрок играл 1 карту

# Шаги для сценария "Защита игрока"
@given('игрок "{player_name}" является защищающимся')
def step_set_defender(context, player_name):
    context.defender = context.game.defender
    context.game.table_cards = [Card("червы", "6")]
    assert context.defender.name == player_name

@when('{player_name} выбирает карту "{rank} {suit}" для защиты')
def step_player_defends(context, player_name, rank, suit):
    context.defender = context.game.defender
    card = context.defender.find_card(suit, rank)
    assert card is not None, "Карта не найдена"
    context.defend_success = context.game.defend(card)

@then('карта "{rank} {suit}" должна быть положена на стол при защите')
def step_defense_card_on_table(context, rank, suit):
    card_on_table = context.game.table_cards[-1]
    assert card_on_table.rank == rank and card_on_table.suit == suit

@then('карта должна быть удалена из руки {player_name} при защите')
def step_defense_card_removed_from_hand(context, player_name):
    assert context.defend_success
    assert len(context.defender.hand) == 5  # Игрок играл 1 карту

@then('{player_name} должен успешно защититься от атаки "{rank} {suit}"')
def step_check_successful_defense(context, player_name, rank, suit):
    assert context.defend_success, f"{player_name} не смог защититься"
