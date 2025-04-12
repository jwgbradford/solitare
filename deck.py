from card import Card
from pygame import Surface
from CONSTANTS import TRANSPARENT
from random import shuffle

class Deck:
    def __init__(self, pos=(0,0)) -> None:
        self.cards : list[Card] = []
        self.deck_display = Surface((140, 200))
        self.deck_display.set_colorkey(TRANSPARENT)
        self.deck_display.fill(TRANSPARENT)
        self.deck_rect = self.deck_display.get_rect()
        self.deck_rect.topleft = pos
        self.movable = False
        self.last_mouse_pos = (-1,-1) # off the screen

    def create_deck(self, size=100) -> list[Card]:
        suits = ['h', 'd', 's', 'c']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(size, suit, rank))

    def shuffle(self) -> None:
        shuffle(self.cards)
        self.cards[-1].add_back_image()

    def draw_card(self) -> list[Card]:
        if len(self.cards) > 0:
            new_card = self.cards.pop()
            if len(self.cards) > 0:
                self.cards[-1].add_back_image()
            new_card.flip_card()
            return [new_card]
        else:
            return None

    def draw_deck(self) -> None:
        if len(self.cards) > 0:
            if self.cards[-1].face_up:
                self.deck_display.blit(self.cards[-1].front_image, (0, 0))
            else:
                self.deck_display.blit(self.cards[-1].back_image, (0, 0))
        else:   
            pass
        
    def add_card(self, card_stack : list[Card]) -> None:
        for card in card_stack:
            self.cards.append(card)

    def handle_click(self, mouse_pos, moving_stack) -> tuple[bool, list[Card]]:
        '''
        conditions to check:
        - are we clicking on the main deck, to draw a new card
        - are we clicking on a deck to move all or part of a stack
        - are we clicking on a deck to move a single card to the final stacks (handle on mouse_up)
        - are we already moving a stack?
        '''
        cards = []
        if (self.deck_rect.collidepoint(mouse_pos) and 
                not self.movable and
                not moving_stack and
                len(self.cards) > 0 and
                not self.cards[-1].face_up):        
            # draw new card
            cards = [self.draw_card()]
        elif (self.deck_rect.collidepoint(mouse_pos) and
                not self.movable and
                not moving_stack and
                len(self.cards) > 0):
            # pick up stack of cards
            moving_stack = True
            self.last_mouse_pos = mouse_pos
            cards = self.get_stack(mouse_pos)
        elif (self.deck_rect.collidepoint(mouse_pos) and
                self.movable and
                moving_stack and
                len(self.cards) > 0):
            #we're the stack being moved
            self.deck_rect.center = mouse_pos
        else:
            pass
        return moving_stack, cards

    def drop_cards(self, mouse_pos, card_stack):
        if (self.deck_rect.collidepoint(mouse_pos) and
                self.next_card_in_stack(card_stack)):
            self.cards.append(card_stack)
            return False

    def next_card_in_stack(self, card_stack):
        last_card = self.cards[-1]
        first_card = card_stack[0]
        '''
        check suits different
        check value +=1
        '''
        if (
            (
            (last_card.suit == 'h' or last_card.suit == 'd'
            and
            first_card.suit == 'c' or first_card.suit == 's')
            or
            (last_card.suit == 'c' or last_card.suit == 's'
            and
            first_card.suit == 'h' or first_card.suit == 'd')
            )
            and
            first_card.value == last_card.value + 1
            ):
            return True
        else:
            return False

    def get_stack(self, mouse_pos) -> list[Card]:
        card_stack = []
        card_index = 0
        # find the top card that was clicked
        for index, card in enumerate(self.cards):
            if card.rect.collidepoint(mouse_pos):
                card_index = index
            else:
                break
        for _ in range(card_index, len(self.cards)):
            card_stack.append(self.cards.pop(card_index))
        card_stack.reverse()
        return card_stack