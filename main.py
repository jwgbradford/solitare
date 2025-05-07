from deck import Deck
from pygame import display, time, event, mouse, QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, K_SPACE, K_ESCAPE
from CONSTANTS import GREEN, DECKS

class MyGame:
    def __init__(self) -> None:
        self.screen = display.set_mode((1500, 600))
        self.add_decks()

    def add_decks(self) -> None:
        self.my_decks = {}
        for data in DECKS:
            self.my_decks[data['name']] = (Deck(**data))
        self.my_decks['main'].create_deck()
        self.my_decks['main'].shuffle()

    def handle_mouse_click(self, pickup_deck) -> None:
        card_stack = []
        moving_stack = False
        for deck in self.my_decks: # check each deck in turn
            moving_stack, card_stack = deck.handle_click(mouse.get_pos(), moving_stack)
            if len(card_stack) > 0:
                if moving_stack: # add the stack of cards to move, to the mobile deck
                    self.my_decks['mobile'].add_card(card_stack)
                    pickup_deck = deck.name
                else: # add card to discard deck
                    self.my_decks['discard'].add_card(card_stack)
                return pickup_deck

    def handle_stack_drop(self) -> None:
        if len(self.my_decks[-1].cards) > 0: # we're moving cards
            # drop cards on new deck
            for deck in range(len(self.my_decks) - 1): 
                card_stack = self.my_decks[deck].drop_cards(mouse.get_pos(), self.my_decks[-1].cards)
            if len(card_stack) > 0: # not dropped on a deck
                self.my_decks[pickup_deck].add_card(card_stack)
                card_stack = []
        self.my_decks['mobile'].cards = [] # clear mobile deck

    def update_screen(self) -> None:
        self.screen.fill((GREEN))
        for deck in self.my_decks:
            self.my_decks[deck].draw_deck()
            self.screen.blit(self.my_decks[deck].deck_display, self.my_decks[deck].deck_rect)
        display.flip()

    def run(self) -> None:
        run = True
        pickup_deck = ''
        while run:
            for each_event in event.get():
                if each_event.type == QUIT:
                    run = False
                elif each_event.type == KEYDOWN:
                    if each_event.key == K_ESCAPE: # quit
                        run = False
                    elif each_event.key == K_SPACE: # pick another card
                        self.my_decks['discard'].add_card(self.my_decks['main'].draw_card())
                elif each_event.type == MOUSEBUTTONDOWN:
                    if mouse.get_pressed()[0]:
                        pickup_deck = self.handle_mouse_click(pickup_deck)
                elif each_event.type == MOUSEBUTTONUP:
                    if mouse.get_pressed()[0]:
                        self.handle_stack_drop(pickup_deck)
            time.wait(10)
            self.update_screen()

if __name__ == '__main__':
    my_game = MyGame()
    my_game.run()