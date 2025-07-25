from deck import Deck, Card
from pygame import init, quit, display, time, event, mouse, font, QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, K_SPACE, K_ESCAPE
from CONSTANTS import GREEN, DECKS, DOUBLECLICKTIME

class MyGame:
    def __init__(self) -> None:
        init()
        self.screen = display.set_mode((1500, 900))
        self.my_font = font.Font(None, 36)

    def add_decks(self) -> None:
        self.my_decks = {}
        for data in DECKS:
            self.my_decks[data['name']] = (Deck(data))
        self.my_decks['main'].create_deck()
        self.my_decks['main'].shuffle()

    def handle_mouse_click(self, pickup_deck) -> str:
        card_stack = []
        moving_stack = False
        for deck in self.my_decks: # check each deck in turn
            moving_stack, card_stack = self.my_decks[deck].handle_click(mouse.get_pos(), moving_stack)
            if len(card_stack) > 0:
                if moving_stack: # add the stack of cards to move, to the mobile deck
                    self.my_decks['mobile'].add_card(card_stack)
                    pickup_deck = self.my_decks[deck].name
                else: # add card to discard deck
                    self.my_decks['discard'].add_card(card_stack)
                break
            elif len(card_stack) == 0 and moving_stack: # clicked on empty main deck
                card_stack = self.my_decks['discard'].cards
                self.my_decks['discard'].cards = [] # clear discard deck
                card_stack.reverse() # flip the stack
                self.my_decks['main'].add_card(card_stack)
        return pickup_deck
    
    def handle_double_click(self) -> None:
        card = None # start with no card
        dropped = False
        for deck in self.my_decks: # check each deck in turn
            card  = self.my_decks[deck].handle_double_click(mouse.get_pos())
            if card is not None: # found a card to move
                for deck in self.my_decks: # check each deck in turn
                    if 'final' in deck: # try drop card on final stacks
                        dropped = self.my_decks[deck].build_final_decks(card)
                        if dropped:
                            break
                break
        if not dropped and isinstance(card, Card): # if not dropped on a final stack
            self.my_decks[deck].add_card([card]) # return card to original deck
        return

    def handle_stack_drop(self, pickup_deck) -> None:
        if len(self.my_decks['mobile'].cards) > 0: # we're moving cards
            cards_to_drop = self.my_decks['mobile'].cards
            # drop cards on new deck
            for deck in self.my_decks: 
                cards_to_drop = self.my_decks[deck].drop_cards(mouse.get_pos(), cards_to_drop)
            if len(cards_to_drop) > 0: # not dropped on a deck
                self.my_decks[pickup_deck].add_card(cards_to_drop)
        self.my_decks['mobile'].cards = [] # clear mobile deck

    def update_screen(self) -> None:
        self.screen.fill((GREEN))
        for deck in self.my_decks:
            self.my_decks[deck].draw_deck()
            self.screen.blit(self.my_decks[deck].deck_display, self.my_decks[deck].deck_rect)
        self.display_game_time()
        display.flip()

    def display_game_time(self) -> None:
        game_time = time.get_ticks() - self.game_time
        minutes = game_time // 60000
        seconds = (game_time // 1000) % 60
        microseconds = (game_time // 10) % 100  # hundredths of a second
        time_string = f'Time: {minutes:02}:{seconds:02}:{microseconds:02}'
        text_surface = self.my_font.render(time_string, True, (5, 5, 5))
        self.screen.blit(text_surface, (480, 120))

    def deal_cards(self) -> None:
        cards_to_deal = 1
        for deck in self.my_decks:
            if 'game' in deck:
                for _ in range(cards_to_deal):
                    if len(self.my_decks['main'].cards) > 0:
                        self.my_decks[deck].add_card(self.my_decks['main'].draw_card())
                        self.my_decks[deck].cards[-1].face_up = False
                self.my_decks[deck].cards[-1].face_up = True # last card in each game stack is face up
                cards_to_deal += 1

    def check_game_over(self) -> bool:
        for deck in self.my_decks:
            if 'final' in deck and len(self.my_decks[deck].cards) < 13:
                return False
        return True

    def play_game(self) -> None:
        db_clock = time.Clock()
        game_clock = time.Clock()
        self.game_time = time.get_ticks()
        run = True
        pickup_deck = ''
        self.add_decks()
        self.deal_cards()  # deal initial cards
        while run:
            run = not self.check_game_over()
            for each_event in event.get():
                if each_event.type == QUIT:
                    run = False
                elif each_event.type == KEYDOWN: # handle key events
                    if each_event.key == K_ESCAPE: # quit
                        run = False
                    elif each_event.key == K_SPACE: # pick another card
                        self.my_decks['discard'].add_card(self.my_decks['main'].draw_card())
                elif each_event.type == MOUSEBUTTONDOWN and each_event.button == 1: # left mouse button clicked
                    if db_clock.tick() < DOUBLECLICKTIME:
                        self.handle_double_click() # handle double click
                    else:
                        pickup_deck = self.handle_mouse_click(pickup_deck)
                elif each_event.type == MOUSEBUTTONUP and each_event.button == 1: # left mouse button released
                    self.handle_stack_drop(pickup_deck)
            self.my_decks['mobile'].deck_rect.center = mouse.get_pos()
            game_clock.tick(60)  # limit to 60 FPS
            self.update_screen()

    def run(self) -> None:
        self.play_game()
        play_game = True
        while play_game:
            for each_event in event.get():
                if each_event.type == QUIT:
                    play_game = False
                elif each_event.type == KEYDOWN: # handle key events
                    if each_event.key == K_ESCAPE: # quit
                        play_game = False
                    elif each_event.key == K_SPACE: # pick another card
                        self.play_game()
        quit()
        raise SystemExit("Game Over")

if __name__ == '__main__':
    my_game = MyGame()
    my_game.run()