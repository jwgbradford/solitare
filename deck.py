from card import Card
from random import shuffle

class Deck:
    def __init__(self) -> None:
        self.cards : list[Card] = []

    def create_deck(self, size=100) -> list[Card]:
        suits = ['h', 'd', 's', 'c']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(size, suit, rank))

    def shuffle(self) -> None:
        shuffle(self.cards)
        self.cards[-1].add_front_image()

    def draw(self) -> Card:
        if len(self.cards) > 0:
            returned_card = self.cards.pop()
            self.cards[-1].add_front_image()
            return returned_card
        else:   
            return None
        
    def add(self, card: Card) -> None:
        self.cards.append(card)