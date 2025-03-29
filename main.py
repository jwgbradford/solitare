from deck import Deck
from pygame import display, time, event, mouse, rect, QUIT, KEYDOWN, MOUSEBUTTONDOWN
from CONSTANTS import GREEN

class MyGame:
    def __init__(self) -> None:
        self.screen = display.set_mode((400, 400))
        self.main_deck = Deck()
        self.main_deck.shuffle()
        self.main_deck.cards[-1].add_back_image()
        self.my_card = self.main_deck.draw()
        self.show_card = self.my_card.back_image

    def move_card(self, button_pressed) -> None:
        card_to_move = self.main_deck.cards[-1].front_image
        self.main_deck.cards[-2].add_back_image()
        self.show_card = self.main_deck.cards[-2].back_image
        while button_pressed:
            button_pressed = False
            event.get()
            if mouse.get_pressed()[0]:
                button_pressed = True
                mouse_pos = mouse.get_pos()
                self.update_screen(moving_card=card_to_move, pos=mouse_pos)
        self.show_card = self.main_deck.cards[-1].front_image

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
                    my_card = self.main_deck.draw()
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