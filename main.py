from deck import Deck
from pygame import display, time, event, mouse, rect, QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_SPACE, K_ESCAPE
from CONSTANTS import GREEN, deck_pos

class MyGame:
    def __init__(self) -> None:
        self.screen = display.set_mode((1500, 600))
        self.add_decks()

    def add_decks(self) -> None:
        size = 200
        self.my_decks = []
        '''
        0 - main deck
        1 - discard deck
        2 - final stack - hearts
        3 - final stack - diamonds
        4 - final stack - spades
        5 - final stack - clubs
        6 - game stack
        7 - game stack
        8 - game stack
        9 - game stack
        10 - game stack
        11 - game stack
        12 - game stack
        13 - mobile stack
        '''
        for i in range(14):
                pos = (deck_pos[i][0] * size - size / 2, deck_pos[i][1] * size * 1.25 - size / 2)
                self.my_decks.append(Deck(scale=size, pos=pos))
        self.my_decks[0].create_deck(scale=size)
        self.my_decks[0].shuffle()
        self.my_decks[-1].movable = True

    def handle_mouse_click(self) -> None:
        moving_stack = True
        card_stack = []
        while moving_stack:
            event.get()
            if mouse.get_pressed()[0]: # left mouse button
                for deck in self.my_decks: # check each deck in turn
                    moving_stack, card_stack = deck.handle_click(mouse.get_pos(), moving_stack)
                    if len(card_stack) > 0:
                        if moving_stack: # add the stack of cards to move, to the mobile deck
                            self.my_decks[-1].add_card(card_stack)
                        else: # add card to discard deck
                            self.my_decks[1].add_card(card_stack)
                        card_stack = []
                self.update_screen()
            else:
                # drop cards on new deck
                for deck in self.my_decks:
                    card_stack = deck.drop_cards(mouse.get_pos(), self.my_decks[1].my_deck)
        self.my_decks[1] = []

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
                    if each_event.key == K_ESCAPE:
                        run = False
                    elif each_event.key == K_SPACE:
                        self.my_decks[1].add_card(self.my_decks[0].draw_card())
                elif each_event.type == MOUSEBUTTONDOWN:
                    if mouse.get_pressed()[0]:
                        self.handle_mouse_click()
            time.wait(100)
            self.update_screen()

if __name__ == '__main__':
    my_game = MyGame()
    my_game.run()