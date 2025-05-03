from deck import Deck
from pygame import display, time, event, mouse, rect, QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_SPACE, K_ESCAPE
from CONSTANTS import GREEN, DECKS

class MyGame:
    def __init__(self) -> None:
        self.screen = display.set_mode((1500, 600))
        self.add_decks()

    def add_decks(self) -> None:
        self.my_decks = []
        for data in DECKS:
            print(data)
            self.my_decks.append(Deck(**data))
        self.my_decks[0].create_deck()
        self.my_decks[0].shuffle()

    def handle_mouse_click(self) -> None:
        moving_stack = False
        card_stack = []
        pickup_deck = 99
        while True:
            event.get()
            if mouse.get_pressed()[0]: # left mouse button
                for index, deck in enumerate(self.my_decks): # check each deck in turn
                    moving_stack, card_stack = deck.handle_click(mouse.get_pos(), moving_stack)
                    if len(card_stack) > 0:
                        if moving_stack: # add the stack of cards to move, to the mobile deck
                            self.my_decks[-1].add_card(card_stack)
                            pickup_deck = index
                        else: # add card to discard deck
                            self.my_decks[1].add_card(card_stack)
                        card_stack = []
                self.update_screen()
            elif len(self.my_decks[-1].cards) > 0: # we're moving cards
                # drop cards on new deck
                for deck in range(len(self.my_decks) - 1): 
                    card_stack = self.my_decks[deck].drop_cards(mouse.get_pos(), self.my_decks[-1].cards)
                if len(card_stack) > 0: # not dropped on a deck
                    self.my_decks[pickup_deck].add_card(card_stack)
                    card_stack = []
                break
        self.my_decks[-1].cards = [] # clear mobile deck

    def update_screen(self) -> None:
        self.screen.fill((GREEN))
        for deck in self.my_decks:
            deck.draw_deck()
            self.screen.blit(deck.deck_display, deck.deck_rect)
        display.flip()

    def run(self) -> None:
        run = True
        while run:
            for each_event in event.get():
                if each_event.type == QUIT:
                    run = False
                elif each_event.type == KEYDOWN:
                    if each_event.key == K_ESCAPE: # quit
                        run = False
                    elif each_event.key == K_SPACE: # pick another card
                        self.my_decks[1].add_card(self.my_decks[0].draw_card())
                elif each_event.type == MOUSEBUTTONDOWN:
                    if mouse.get_pressed()[0]:
                        self.handle_mouse_click()
            time.wait(100)
            self.update_screen()

if __name__ == '__main__':
    my_game = MyGame()
    my_game.run()