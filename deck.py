from CONSTANTS import TRANSPARENT, BLACK
from card import Card
from pygame import Surface, draw
from random import shuffle
from math import pi

class Deck:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)
        self.cards : list[Card] = []
        self.deck_display = self.empty_deck()
        self.deck_rect = self.deck_display.get_rect()
        self.set_pos()
        self.last_mouse_pos = (-1,-1) # off the screen

    def empty_deck(self) -> Surface:
        if 'game' in self.name: # game decks are larger
            image = Surface((self.size * 0.7, self.size + self.size * 9 * 0.3))
        else:
            image = Surface((self.size * 0.7, self.size))
        image.set_colorkey(TRANSPARENT)
        image.fill(TRANSPARENT)
        if self.name == 'mobile':
            return image
        offset = self.size // 4
        line_offset = self.size // 8
        # draw borders
        draw.arc(image, BLACK, (0, 0, offset, offset), pi / 2, pi, 1)
        draw.arc(image, BLACK, (0, self.size - offset, offset, offset), pi, 3 * pi / 2, 1)
        draw.arc(image, BLACK, (self.size * 0.7 - offset, 0, offset, offset), 0, pi / 2, 1)
        draw.arc(image, BLACK, (self.size * 0.7 - offset, self.size - offset, offset, offset), 3 * pi / 2, 0, 1)
        # draw sides
        draw.line(image, BLACK, (line_offset, 0), (self.size * 0.7 - line_offset, 0), 1)
        draw.line(image, BLACK, (0, line_offset), (0, self.size - line_offset), 1)
        draw.line(image, BLACK, (self.size * 0.7 - 1, line_offset), (self.size * 0.7 - 1, self.size - line_offset), 1)
        draw.line(image, BLACK, (line_offset, self.size - 1), (self.size * 0.7 - line_offset, self.size - 1), 1)
        return image

    def set_pos(self) -> None:
        xy_pos = (self.pos[0] * self.size - self.size / 2, self.pos[1] * self.size * 1.25 - self.size)
        self.deck_rect.topleft = xy_pos

    def create_deck(self, ) -> list[Card]:
        suits = ['h', 'd', 's', 'c']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(self.size, suit, rank))

    def shuffle(self) -> None:
        shuffle(self.cards)
        self.cards[0].add_back_image()

    def draw_card(self) -> list[Card]:
        if len(self.cards) > 0:
            new_card = self.cards.pop(-1)
            if len(self.cards) > 0:
                self.cards[-1].add_back_image()
            new_card.flip_card()
            return [new_card]
        else:
            return None

    def draw_deck(self) -> None:
        self.deck_display = self.empty_deck()
        if len(self.cards) > 0:
            for card in self.cards:
                if card.face_up:
                    self.deck_display.blit(card.front_image, card.position)
                else:
                    self.deck_display.blit(card.back_image, card.position)
                    break
        return
        
    def add_card(self, card_stack : list[Card]) -> None:
        for card in card_stack:
            if len(self.cards) == 0:
                card.position = (0, 0)
            elif 'game' in self.name:
                card.position = (0, self.cards[-1].position[1] + self.size * 0.1)
            else:
                card.position = (0, 0)
            self.cards.append(card)
            #self.cards.insert(0, card)

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
                if self.name == 'main': # we're clicking on the main deck
                    # draw new card
                    cards = self.draw_card()
                    #print('draw card')
                else: # pick up stack of cards
                    moving_stack = True
                    self.last_mouse_pos = mouse_pos
                    cards = self.get_stack(mouse_pos)
                    #print(f'pick up stack {len(cards)}')}')
        return moving_stack, cards

    def drop_cards(self, mouse_pos : tuple[int,int], card_stack : list[Card]) -> list[Card]:
        if self.name == 'mobile':
            return card_stack
        if self.deck_rect.collidepoint(mouse_pos):
            if self.next_card_in_stack(card_stack):
                self.add_card(card_stack)
                return []
        return card_stack

    def next_card_in_stack(self, card_stack : list[Card]) -> bool:
        if len(self.cards) == 0:
            return True
        top_card = self.cards[-1]
        bottom_card = card_stack[0]
        '''
        check suits different
        check value +=1
        '''
        if (
            (
            (top_card.suit == 'h' or top_card.suit == 'd'
                and
                bottom_card.suit == 'c' or bottom_card.suit == 's')
            or
            (top_card.suit == 'c' or top_card.suit == 's'
                and
                bottom_card.suit == 'h' or bottom_card.suit == 'd')
            )
            and
                top_card.value == bottom_card.value  + 1
            ):
            return True
        else:
            return False

    def get_stack(self, mouse_pos) -> list[Card]:
        if self.name == 'discard':
            return [self.cards.pop()] # if we're the discard pile, just return the top card
        card_stack = []
        card_index = -1
        # find the top card that was clicked
        for index, card in enumerate(self.cards):
            card.rect.topleft = (self.deck_rect.x, self.deck_rect.y + index * self.size * 0.1) # update rect to current card position
            if card.rect.collidepoint(mouse_pos):
                card_index += 1
            else:
                break
        if card_index == -1:  # no card was clicked
            return []
        # now we have the index of the top card, we can get the stack
        card_pickup_loop = len(self.cards) - card_index
        for _ in range(card_pickup_loop):
            card_stack.append(self.cards.pop())
        card_stack.reverse()
        return card_stack