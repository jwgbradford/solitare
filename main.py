from deck import Deck
from pygame import display, time, event, mouse, rect, QUIT, KEYDOWN, MOUSEBUTTONDOWN
from CONSTANTS import GREEN, deck_pos

class MyGame:
    def __init__(self) -> None:
        self.screen = display.set_mode((1200, 600))
        self.add_decks()

    def add_decks(self) -> None:
        self.my_decks = []
        for i in range(14):
            if i == 1:
                self.my_decks.append(Deck(pos=deck_pos[i], movable=True))
            else:
                self.my_decks.append(Deck(pos=deck_pos[i], movable=False))
        self.my_decks[0].create_deck()
        self.my_decks[0].shuffle()

    def handle_mouse_click(self) -> None:
        moving_stack = True
        while moving_stack:
            moving_stack = False
            event.get()
            if mouse.get_pressed()[0]:
                for deck in self.my_decks:
                    moving_stack = deck.handle_click(mouse.get_pos(), moving_stack)
                self.update_screen()

    def update_screen(self, moving_card = False, pos = (0,0)) -> None:
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
                    self.my_decks[0].draw()
                elif each_event.type == MOUSEBUTTONDOWN:
                    if mouse.get_pressed()[0]:
                        self.handle_mouse_click()
            time.wait(100)
            self.update_screen()

if __name__ == '__main__':
    my_game = MyGame()
    my_game.run()