from deck import Deck
from pygame import display, time, event, QUIT, KEYDOWN
from CONSTANTS import GREEN

def run() -> None:
    screen = display.set_mode((400, 400))
    main_deck = Deck()
    main_deck.shuffle()
    my_card = main_deck.draw()
    show_card = my_card.back_image
    run = True
    while run:
        screen.fill((GREEN))
        screen.blit(show_card, (50,50))
        time.wait(100)
        display.update()
        for each_event in event.get():
            if each_event.type == QUIT:
                run = False
            elif each_event.type == KEYDOWN:
                my_card = main_deck.draw()
                if my_card is not None:
                    show_card = my_card.front_image
                else:
                    run = False

if __name__ == '__main__':
    run()