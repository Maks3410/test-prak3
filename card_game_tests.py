import unittest
from card_game import Card, Player, Deck, Game


class TestCardGame(unittest.TestCase):

    def test_card_creation(self):
        # Проверяем, что создается карта с мастью и рангом
        card = Card("пики", "A")
        self.assertEqual(card.suit, "пики")
        self.assertEqual(card.rank, "A")
        self.assertEqual(str(card), "A пики")

    def test_deck_creation(self):
        # Проверяем, что в колоде 36 карт (4 масти по 9 рангов)
        deck = Deck()
        self.assertEqual(len(deck.cards), 36)
        self.assertEqual(str(deck.cards[0]), "6 червы")  # Проверка первой карты
        self.assertEqual(str(deck.cards[-1]), "A пики")  # Проверка последней карты

    def test_player_hand(self):
        # Проверяем, что игрок может держать карты в руке и играть карты
        player = Player("Alice")
        card = Card("трефы", "K")
        player.hand.append(card)

        # Проверяем поиск карты в руке
        found_card = player.find_card("трефы", "K")
        self.assertEqual(found_card, card)

        # Проверяем успешную игру карты
        played_card = player.play_card(card)
        self.assertEqual(played_card, card)
        self.assertNotIn(card, player.hand)

        # Проверяем, что игра карты не проходит, если карты нет в руке
        self.assertIsNone(player.play_card(card))

    def test_game_setup(self):
        # Проверяем настройку игры, игроков, и атаку
        game = Game()
        player1 = Player("Alice")
        player2 = Player("Bob")

        card1 = Card("пики", "8")
        card2 = Card("пики", "K")

        player1.hand.append(card1)
        player2.hand.append(card2)

        game.set_players(player1, player2)

        # Проверяем атаку: карта должна быть на столе после успешной атаки
        attack_successful = game.attack(card1)
        self.assertTrue(attack_successful)
        self.assertIn(card1, game.table_cards)
        self.assertNotIn(card1, player1.hand)

        # Проверяем, что не удается атаковать картой, которой нет в руке
        attack_unsuccessful = game.attack(card2)
        self.assertFalse(attack_unsuccessful)

    def test_game_defense(self):
        # Проверяем успешную и неудачную защиту
        game = Game()
        player1 = Player("Alice")
        player2 = Player("Bob")

        card1 = Card("пики", "8")
        card2 = Card("пики", "K")

        player1.hand.append(card1)
        player2.hand.append(card2)

        game.set_players(player1, player2)

        game.attack(card1)

        # Проверяем успешную защиту: карта должна быть сильнее и добавлена на стол
        defend_successful = game.defend(card2)
        self.assertTrue(defend_successful)
        self.assertIn(card2, game.table_cards)
        self.assertNotIn(card2, player2.hand)

        # Проверяем неудачную защиту (нет карты в руке или она слабее)
        card3 = Card("пики", "7")
        player2.hand.append(card3)

        defend_unsuccessful = game.defend(card3)
        self.assertFalse(defend_unsuccessful)
        self.assertIn(card3, player2.hand)

    def test_game_end_round(self):
        # Проверяем завершение раунда
        game = Game()
        player1 = Player("Alice")
        player2 = Player("Bob")

        card1 = Card("пики", "8")
        card2 = Card("бубны", "K")
        card3 = Card("червы", "10")

        player1.hand.extend([card1, card2])
        player2.hand.append(card3)

        game.set_players(player1, player2)

        game.attack(card1)
        game.defend(card3)

        game.end_round()

        # Проверяем, что стол очищен
        self.assertEqual(len(game.table_cards), 0)

    def test_game_over(self):
        # Проверяем окончание игры
        game = Game()
        player1 = Player("Alice")
        player2 = Player("Bob")

        player1.hand = []
        player2.hand.append(Card("червы", "7"))

        game.set_players(player1, player2)

        self.assertTrue(game.is_game_over())


if __name__ == "__main__":
    unittest.main()
