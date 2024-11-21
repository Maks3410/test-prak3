class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} {self.suit}"

    def __repr__(self) -> str:
        return f"{self.rank} {self.suit}"


class Deck:
    suits = ["червы", "бубны", "трефы", "пики"]
    ranks = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card

    def find_card(self, suit, rank):
        for card in self.hand:
            if card.suit == suit and card.rank == rank:
                return card
        return None


class Game:
    def __init__(self):
        self.table_cards = []
        self.attacker = None
        self.defender = None

    def set_players(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender

    def attack(self, card):
        if card in self.attacker.hand:
            self.attacker.hand.remove(card)
            self.table_cards.append(card)
            return True
        return False

    def defend(self, card):
        if card in self.defender.hand:
            last_attack = self.table_cards[-1]
            if card.suit == last_attack.suit and self.is_stronger(card, last_attack):
                self.defender.hand.remove(card)
                self.table_cards.append(card)
                return True
        return False

    def is_stronger(self, card1, card2):
        rank_order = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return rank_order.index(card1.rank) > rank_order.index(card2.rank)

    def end_round(self):
        if len(self.table_cards) % 2 != 0:
            self.defender.hand.extend(self.table_cards)
        else:
            self.attacker, self.defender = self.defender, self.attacker
        self.table_cards.clear()

    def is_game_over(self):
        return len(self.attacker.hand) == 0 or len(self.defender.hand) == 0
