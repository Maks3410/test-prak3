from card_game import Card, Deck, Player, Game
import random


def main():
    deck = Deck()
    random.shuffle(deck.cards)

    attacker = Player(input("Введите имя первого игрока: "))
    defender = Player(input("Введите имя второго игрока: "))

    attacker.hand = [deck.cards.pop() for _ in range(6)]
    defender.hand = [deck.cards.pop() for _ in range(6)]

    game = Game()
    game.set_players(attacker, defender)

    while True:
        attacker, defender = game.attacker, game.defender
        print(f"Колода {attacker.name}: {[f'{card.rank} {card.suit}' for card in attacker.hand]}")
        print(f"Колода {defender.name}: {[f'{card.rank} {card.suit}' for card in defender.hand]}")

        rank, suit = input("Выберите карту для атаки: ").split()
        attack_card = attacker.find_card(suit, rank)
        while attack_card is None:
            print("Нет такой карты")
            rank, suit = input("Выберите карту для атаки: ").split()
            attack_card = attacker.find_card(suit, rank)

        if game.attack(attack_card):
            print(f"{attacker.name} ходит картой {attack_card.rank} {attack_card.suit}")

        rank, suit = input("Выберите карту для защиты: ").split()
        defend_card = defender.find_card(suit, rank)
        while defend_card is None:
            print("Нет такой карты")
            rank, suit = input("Выберите карту для защиты: ").split()
            defend_card = defender.find_card(suit, rank)

        if game.defend(defend_card):
            print(f"{defender.name} кроет картой {defend_card.rank} {defend_card.suit}")
        else:
            print("Этой картой покрыть нельзя")

        game.end_round()

        print(f"Колода {attacker.name} после раунда: {[f'{card.rank} {card.suit}' for card in attacker.hand]}")
        print(f"Колода {defender.name} после раунда: {[f'{card.rank} {card.suit}' for card in defender.hand]}")

        if game.is_game_over():
            print("Игра окончена!")
            return
        else:
            print("Игра продолжается...")


if __name__ == '__main__':
    main()
