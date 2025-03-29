from deck import Deck
from pygame import display, time, event, mouse, rect, QUIT, KEYDOWN, MOUSEBUTTONDOWN
from CONSTANTS import GREEN

class MyGame:
    def __init__(self) -> None:
        self.screen = display.set_mode((400, 400))
        self.add_decks()

    def add_decks(self) -> None:
        self.my_decks = []
        for _ in range(8):
            self.my_decks.append(Deck())
        self.my_decks[0].create_deck()
        self.my_decks[0].shuffle()
        self.my_decks[0].cards[-1].add_back_image()
        self.my_card = self.my_decks[0].draw()
        self.show_card = self.my_card.back_image

    def move_card(self, button_pressed) -> None:
        card_to_move = self.my_decks[0].cards[-1].front_image
        self.my_decks[0].cards[-2].add_back_image()
        self.show_card = self.my_decks[0].cards[-2].back_image
        while button_pressed:
            button_pressed = False
            event.get()
            if mouse.get_pressed()[0]:
                button_pressed = True
                mouse_pos = mouse.get_pos()
                self.update_screen(moving_card=card_to_move, pos=mouse_pos)
        self.show_card = self.my_decks[0].cards[-1].front_image

    def update_screen(self, moving_card = None, pos = (0,0)) -> None:
        self.screen.fill((GREEN))
        self.screen.blit(self.show_card, (50,50))
        if moving_card:
            card_rect = moving_card.get_rect()
            card_rect.center = pos
            self.screen.blit(moving_card, card_rect)
        display.flip()

    def run(self) -> None:
        run = True
        while run:
            for each_event in event.get():
                if each_event.type == QUIT:
                    run = False
                elif each_event.type == KEYDOWN:
                    my_card = self.my_decks[0].draw()
                    if my_card is not None:
                        self.show_card = my_card.front_image
                    else:
                        run = False
                elif each_event.type == MOUSEBUTTONDOWN:
                    if mouse.get_pressed()[0]:
                        mouse_pos = mouse.get_pos()
                        card_rect = self.show_card.get_rect()
                        if card_rect.collidepoint(mouse_pos):
                            self.move_card(True)
                            break
            time.wait(100)
            self.update_screen()

if __name__ == '__main__':
    my_game = MyGame()
    my_game.run()