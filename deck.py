from CONSTANTS import TRANSPARENT, BLACK, SIZE
from card import Card
from pygame import Surface, draw
from random import shuffle
from math import pi

class Deck:
    def __init__(self, data) -> None:
        self.name = data['name']
        self.pos = data['pos']
        self.movable = data['movable']
        self.size = SIZE
        self.cards : list[Card] = []
        self.deck_display = self.empty_deck()
        self.deck_rect = self.deck_display.get_rect()
        self.set_pos()
        self.last_mouse_pos = (-1,-1) # off the screen

    def empty_deck(self) -> Surface:
        if 'game' in self.name: # game decks are larger
            image = Surface((self.size * 0.7, self.size + self.size *12 * 0.1))
        else:
            image = Surface((self.size * 0.7, self.size))
        image.set_colorkey(TRANSPARENT)
        image.fill(TRANSPARENT) # dark background
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

    def create_deck(self) -> list[Card]:
        suits = ['h', 'd', 's', 'c']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self) -> None:
        shuffle(self.cards)
        self.cards[-1].add_back_image()

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
            if self.name == 'main':
                self.deck_display.blit(self.cards[-1].back_image, self.cards[-1].position)
            else:
                for card in self.cards:
                    self.deck_display.blit(card.front_image, card.position)
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
                else: # pick up stack of cards
                    cards = self.get_stack(mouse_pos)
                    if len(cards) == 0: # no cards picked up, clicked on deck surface but not on a card
                        return moving_stack, cards
                    moving_stack = True
                    self.last_mouse_pos = mouse_pos
            elif self.name == 'main' and len(self.cards) == 0: # clicked on empty main deck to restock
                moving_stack = True
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
        if len(self.cards) == 0: # empty deck
            if 'final' in self.name: # final stacks start with aces
                if card_stack[0].value == 1: # ace
                    return True
                else:
                    return False
            elif 'game' in self.name: # empty game stacks can take any card
                return True
            else: # you can't drop cards on the discard pile or main deck
                return False 
        my_top_card = self.cards[-1]
        moving_bottom_card = card_stack[0]
        '''
        check suits different
        check value +=1
        '''
        if ('final' in self.name 
            and
            len(card_stack) == 1 
            and
            (
            (my_top_card.suit == moving_bottom_card.suit)
            )
            and
                moving_bottom_card.value == my_top_card.value + 1
            ):
            return True # fina stacks take same suits in ascending order
        elif ('game' in self.name 
            and
            (
            (my_top_card.suit == 'h' or my_top_card.suit == 'd'
                and
                moving_bottom_card.suit == 'c' or moving_bottom_card.suit == 's')
            or
            (my_top_card.suit == 'c' or my_top_card.suit == 's'
                and
                moving_bottom_card.suit == 'h' or moving_bottom_card.suit == 'd')
            )
            and
                moving_bottom_card.value == my_top_card.value - 1
            ):
            return True # game stacks take different suits in descending order
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
    
    def handle_double_click(self, mouse_pos) -> tuple[Card, str]:
        card = None  # no card to move
        original_deck = ''
        if 'discard' in self.name or 'game' in self.name: # post cards from discard or game stacks to final stacks
            if len(self.cards) > 0 and self.cards[-1].rect.collidepoint(mouse_pos):
                original_deck = self.name
                card = self.cards.pop()  # get the top card
        return card, original_deck
    
    def build_final_decks(self, card : Card) -> bool:
        print(f"Deck size: {len(self.cards)}, Card value: {card.value}, Card suit: {card.suit}")
        if len(self.cards) == 0 and card.value == 1:
            self.add_card([card])
            return True
        elif self.cards[-1].suit == card.suit and self.cards[-1].value == card.value - 1:
            self.add_card([card])
            return True
        else:
            return False
