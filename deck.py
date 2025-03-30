from card import Card
from pygame import Surface
from CONSTANTS import TRANSPARENT
from random import shuffle

class Deck:
    def __init__(self, pos=(0,0), movable=False) -> None:
        self.cards : list[Card] = []
        self.deck_display = Surface((140, 200))
        self.deck_display.set_colorkey(TRANSPARENT)
        self.deck_display.fill(TRANSPARENT)
        self.deck_rect = self.deck_display.get_rect()
        self.deck_rect.topleft = pos
        self.movable = movable

    def create_deck(self, size=100) -> list[Card]:
        suits = ['h', 'd', 's', 'c']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(size, suit, rank))

    def shuffle(self) -> None:
        shuffle(self.cards)
        self.cards[-1].add_back_image()

    def draw_card(self) -> None:
        if len(self.cards) > 0:
            new_card = self.cards.pop()
            if len(self.cards) > 0:
                self.cards[-1].add_front_image()
            return new_card
        else:
            return None

    def draw_deck(self) -> Card:
        if len(self.cards) > 0:
            if self.cards[-1].face_up:
                self.deck_display.blit(self.cards[-1].front_image, (0, 0))
            else:
                self.deck_display.blit(self.cards[-1].back_image, (0, 0))
        else:   
            pass
        
    def add(self, card: Card) -> None:
        self.cards.append(card)

    def handle_click(self, mouse_pos, moving_stack):
        '''
        conditions to check:
        - are we clicking on the main deck, to draw a new card
        - are we clicking on a deck to move all or part of a stack
        - are we clicking on a deck to move a single card to the final stacks
        - are we moving a stack?
        '''
        self.deck_rect = self.deck_display.get_rect()
        # draw new card
        if (self.deck_rect.collidepoint(mouse_pos) and 
                not self.movable and
                not moving_stack and
                len(self.cards) > 0 and
                not self.cards[-1].face_up):
            cards = [self.draw_card()]
            return moving_stack, cards
        elif (self.deck_rect.collidepoint(mouse_pos) and
                not self.movable and
                not moving_stack and
                len(self.cards) > 0):
            # pick up stack of cards
            moving_stack = True
            cards = self.get_stack(mouse_pos)
            return moving_stack, cards
        elif (self.deck_rect.collidepoint(mouse_pos) and
                self.movable and
                moving_stack):
        else:
            return False, None
        
    def get_stack(self, mouse_pos) -> list[Card]:
        cards = []
        for card in self.cards:
            if card.rect.collidepoint(mouse_pos):
                cards.append(card)
                # remove the card from the deck
                self.cards.remove(card)
        return cards