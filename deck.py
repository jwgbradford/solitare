from CONSTANTS import TRANSPARENT, BLACK
from card import Card
from pygame import Surface, draw
from random import shuffle
from math import pi

class Deck:
    def __init__(self, data) -> None:
        self.name = data['name']
        self.cards : list[Card] = []
        self.deck_display = self.empty_deck(data['size'])
        self.set_pos(data)
        self.last_mouse_pos = (-1,-1) # off the screen

    def empty_deck(self, scale) -> Surface:
        image = Surface((scale * 0.7, scale))
        image.set_colorkey(TRANSPARENT)
        image.fill(TRANSPARENT)
        offset = scale // 4
        line_offset = scale // 8
        # draw borders
        draw.arc(image, BLACK, (0, 0, offset, offset), pi / 2, pi, 1)
        draw.arc(image, BLACK, (0, scale - offset, offset, offset), pi, 3 * pi / 2, 1)
        draw.arc(image, BLACK, (scale * 0.7 - offset, 0, offset, offset), 0, pi / 2, 1)
        draw.arc(image, BLACK, (scale * 0.7 - offset, scale - offset, offset, offset), 3 * pi / 2, 0, 1)
        # draw sides
        draw.line(image, BLACK, (line_offset, 0), (scale * 0.7 - line_offset, 0), 1)
        draw.line(image, BLACK, (0, line_offset), (0, scale - line_offset), 1)
        draw.line(image, BLACK, (scale * 0.7 - 1, line_offset), (scale * 0.7 - 1, scale - line_offset), 1)
        draw.line(image, BLACK, (line_offset, scale - 1), (scale * 0.7 - line_offset, scale - 1), 1)
        return image

    def set_pos(self, data) -> None:
        self.deck_rect = self.deck_display.get_rect()
        pos = (data['pos'][0] * data['size'] - data['size'] / 2, data['pos'][1] * data['size'] * 1.25 - data['size'] / 2)
        self.deck_rect.center = pos
        self.movable = data['movable']

    def create_deck(self, ) -> list[Card]:
        suits = ['h', 'd', 's', 'c']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        scale = self.deck_display.get_height()
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(scale, suit, rank))

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

    def handle_click(self, mouse_pos : tuple[int, int], moving_stack : bool) -> tuple[bool, list[Card]]:
        '''
        conditions to check:
        - are we clicking on the main deck, to draw a new card
        - are we clicking on a deck to move all or part of a stack
        - are we clicking on a deck to move a single card to the final stacks (handle on mouse_up)
        - are we already moving a stack?
        '''
        cards = []
        if self.deck_rect.collidepoint(mouse_pos): # we're clicking on a deck
            if (not self.movable and
                    not moving_stack and
                    len(self.cards) > 0): # not the mobile stack, not yet moving a stack, and there are cards in current deck
                if not self.cards[-1].face_up: # top card is face down
                    # draw new card
                    cards = self.draw_card()
                    #print('draw card')
                else: # pick up stack of cards
                    moving_stack = True
                    self.last_mouse_pos = mouse_pos
                    cards = self.get_stack(mouse_pos)
                    #print(f'pick up stack {len(cards)}')
            elif (self.movable and 
                    moving_stack): # we're holding some cards
                self.deck_rect.center = mouse_pos
                #print(f'movable {self.movable} , moving_stack {moving_stack}, length {len(self.cards)}')
            else:
                pass
        else:
            pass
        return moving_stack, cards

    def drop_cards(self, mouse_pos : tuple[int,int], card_stack : list[Card]) -> list[Card]:
        if self.deck_rect.collidepoint(mouse_pos):
            if (self.next_card_in_stack(card_stack) and
                card_stack not in self.cards):
                self.cards.append(card_stack)
                return []
        return card_stack

    def next_card_in_stack(self, card_stack : list[Card]) -> bool:
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