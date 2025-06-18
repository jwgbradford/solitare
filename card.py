from pygame import Surface, draw, font, transform
from math import pi, sin, cos
from CONSTANTS import BLACK, RED, WHITE, BLUE, TRANSPARENT

class Suit:
    def __init__(self, size=100, suit='s') -> None:
        self.image = self.make_image(size, suit)
        self.rect = self.image.get_rect()

    def make_image(self, size, suit) -> Surface:
        image = Surface((size, size))
        image.set_colorkey(TRANSPARENT) # transparency
        image.fill(TRANSPARENT)
        match suit:
            case 'h':
                self.colour = RED
                image = self.draw_heart(image)
            case 'c':
                self.colour = BLACK
                image = self.draw_club(image)
            case 'd':
                self.colour = RED
                image = self.draw_diamond(image)
            case 's':
                self.colour = BLACK
                image = self.draw_spade(image)
            case _:
                pass
        return image

    def heart_coordinates(self, t) -> tuple:
        x = 16 * sin(t)**3
        y = 13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
        return x, y

    def draw_heart(self, image) -> Surface:
        WIDTH = image.get_width()
        HEIGHT = image.get_height()
        scale =  WIDTH / 50 # Adjust for overall size
        t = 0
        points = []
        while t < 2 * pi:
            # Calculate the next point on the heart curve
            t += 0.001  # Adjust for speed of drawing
            x, y = self.heart_coordinates(t)
            # Scale and center the coordinates
            scaled_x = int(WIDTH // 2 + x * scale)
            scaled_y = int(HEIGHT // 2 - y * scale)  # Subtract y to flip vertically
            # Add the point to the list
            points.append((scaled_x, scaled_y))
        draw.polygon(image, self.colour, points, 0)
        return image

    def draw_club(self, image) -> Surface:
        WIDTH = image.get_width()
        HEIGHT = image.get_height()
        draw.circle(image, self.colour, (WIDTH / 2, HEIGHT / 4), WIDTH / 4, 0)
        draw.circle(image, self.colour, ((WIDTH / 16)*5, (HEIGHT / 8)*5), WIDTH / 4, 0)
        draw.circle(image, self.colour, ((WIDTH / 16)*11, (HEIGHT / 8)*5), WIDTH / 4, 0)
        draw.line(image, self.colour, (WIDTH / 2 - WIDTH / 40, HEIGHT / 8), 
                  (WIDTH / 2 - WIDTH / 40, (HEIGHT / 8)*8), WIDTH // 10)
        return image
    
    def draw_diamond(self, image) -> Surface:
        WIDTH = image.get_width()
        HEIGHT = image.get_height()
        draw.polygon(image, self.colour, [(WIDTH // 2, 0), (0, HEIGHT // 2), (WIDTH // 2, HEIGHT), (WIDTH, HEIGHT // 2)], 0)
        return image
    
    def draw_spade(self, image) -> Surface:
        WIDTH = image.get_width()
        HEIGHT = image.get_height()
        scale = WIDTH / 50  # Adjust for overall size
        t = 0
        points = []
        while t < 2 * pi:
            # Calculate the next point on the heart curve
            t += 0.001  # Adjust for speed of drawing

            x, y = self.heart_coordinates(t)

            # Scale and center the coordinates
            scaled_x = int(WIDTH // 2 + x * scale)
            scaled_y = int(HEIGHT // 2 + y * scale)  # Subtract y to flip vertically

            # Add the point to the list
            points.append((scaled_x, scaled_y))
        draw.polygon(image, self.colour, points, 0)
        draw.line(image, self.colour, (WIDTH / 2 - WIDTH / 40, HEIGHT / 4), 
                  (WIDTH / 2 - WIDTH / 40, (HEIGHT / 8)*8), WIDTH // 10)
        return image
    
class Card:
    def __init__(self, scale=200, suit='s', value='10') -> None:
        font.init()
        self.suit = suit
        self.value = value
        self.scale = scale
        self.back_image = None
        self.front_image = None
        self.face_up = False
        self.position = (0, 0)

    def flip_card(self) -> None:
        self.face_up = True
        if self.front_image is None:
            self.add_front_image()
            self.convert_values()

    def convert_values(self) -> None:
        match self.value:
            case 'A':
                self.value = 1
            case 'J':
                self.value = 11
            case 'Q':
                self.value = 12
            case 'K':
                self.value = 13
            case _:
                self.value = int(self.value)

    def make_image(self, colour=BLUE) -> Surface:
        image = Surface((self.scale * 0.7, self.scale))
        offset = self.scale // 4
        line_offset = self.scale // 8
        image.set_colorkey(TRANSPARENT)
        image.fill(TRANSPARENT)
        # draw card
        draw.arc(image, colour, (0, 0, offset, offset), pi / 2, pi, offset)
        draw.arc(image, colour, (0, self.scale - offset, offset, offset), pi, 3 * pi / 2, offset)
        draw.arc(image, colour, (self.scale * 0.7 - offset, 0, offset, offset), 0, pi / 2, offset)
        draw.arc(image, colour, (self.scale * 0.7 - offset, self.scale - offset, offset, offset), 3 * pi / 2, 0, offset)
        # draw sides
        draw.line(image, colour, (line_offset, 0), (self.scale * 0.7 - line_offset, 0), self.scale * 2)
        draw.line(image, colour, (0, line_offset), (0, self.scale - line_offset), int(self.scale * 0.7) * 2)
        # draw borders
        draw.arc(image, BLACK, (0, 0, offset, offset), pi / 2, pi, 1)
        draw.arc(image, BLACK, (0, self.scale - offset, offset, offset), pi, 3 * pi / 2, 1)
        draw.arc(image, BLACK, (self.scale * 0.7 - offset, 0, offset, offset), 0, pi / 2, 1)
        draw.arc(image, BLACK, (self.scale * 0.7 - offset, self.scale - offset, offset, offset), 3 * pi / 2, 0, 1)
        # draw sides
        draw.line(image, BLACK, (line_offset, 0), (self.scale * 0.7 - line_offset, 0), 1)
        draw.line(image, BLACK, (0, line_offset), (0, self.scale - line_offset), 1)
        draw.line(image, BLACK, (self.scale * 0.7 - 1, line_offset), (self.scale * 0.7 - 1, self.scale - line_offset), 1)
        draw.line(image, BLACK, (line_offset, self.scale - 1), (self.scale * 0.7 - line_offset, self.scale - 1), 1)
        return image

    def add_back_image(self) -> None:
        self.back_image = self.make_image(BLUE)

    def add_front_image(self) -> None:
        self.front_image = self.make_image(WHITE)
        self.add_corner_values()
        self.add_values()
        self.rect = self.front_image.get_rect()

    def add_corner_values(self) -> None:
        offset = self.scale // 20
        small = self.scale * 0.7 // 8
        suit_image = Suit(size=small, suit=self.suit)
        card_font = font.Font(None, int(small))
        text = card_font.render(self.value, True, suit_image.colour)
        text_rect = text.get_rect(center=(offset * 2, offset))
        # top left text & image
        self.front_image.blit(suit_image.image, (offset, offset * 2))
        self.front_image.blit(text, text_rect)
        # bottom right text & image
        self.front_image.blit(suit_image.image, (self.scale * 0.7 - offset - small, self.scale - offset * 4))
        text = transform.flip(text, True, True)
        text_rect = text.get_rect(center=(self.scale * 0.7 - offset * 2, self.scale - offset))
        self.front_image.blit(text, text_rect)
    
    def add_values(self) -> None:
        match self.value:
            case 'A':
                self.add_ace()
            case 'K':
                self.add_face_card()
            case 'Q':
                self.add_face_card()
            case 'J':
                self.add_face_card()
            case _: # not a face card
                self.add_number_pattern()

    def add_face_card(self) -> None:
        suit_image = Suit(size=self.scale // 2, suit=self.suit)
        card_font = font.Font(None, int(self.scale // 2))
        text = card_font.render(self.value, True, suit_image.colour)
        text_rect = text.get_rect(center=(self.scale // 2 - text.get_width() // 3 * 2, self.scale // 2))
        self.front_image.blit(text, text_rect)

    def add_ace(self) -> None:
        suit_image = Suit(size=self.scale//2, suit=self.suit)
        self.front_image.blit(suit_image.image, (self.scale * 0.7 // 6, self.scale // 4))

    def add_number_pattern(self) -> None:
        small = self.scale * 0.7 // 8
        suit_image = Suit(size=small, suit=self.suit)
        match self.value:
            case '2':
                self.add_twos(suit_image.image, 0)
            case '3':
                self.add_threes(suit_image.image, 0)
            case '4':
                self.add_twos(suit_image.image, self.scale // 8)
                self.add_twos(suit_image.image, self.scale // 8 * -1)
            case '5':
                self.add_twos(suit_image.image, self.scale // 8)
                self.add_twos(suit_image.image, self.scale // 8 * -1)
                self.front_image.blit(suit_image.image, (self.scale * 0.7 // 2 - suit_image.image.get_width() / 2, self.scale // 2))
            case '6':
                self.add_threes(suit_image.image, self.scale // 8)
                self.add_threes(suit_image.image, self.scale // 8 * -1)
            case '7':
                self.add_threes(suit_image.image, self.scale // 8)
                self.add_threes(suit_image.image, self.scale // 8 * -1)
                self.front_image.blit(suit_image.image, (self.scale * 0.7 // 2 - suit_image.image.get_width() / 2, self.scale // 2.75))
            case '8':
                self.add_fours(suit_image.image, self.scale // 8)
                self.add_fours(suit_image.image, self.scale // 8 * -1)
            case '9':
                self.add_fours(suit_image.image, self.scale // 8)
                self.add_fours(suit_image.image, self.scale // 8 * -1)
                self.front_image.blit(suit_image.image, (self.scale * 0.7 // 2 - suit_image.image.get_width() / 2, self.scale // 2.75))
            case '10':
                self.add_fours(suit_image.image, self.scale // 8)
                self.add_fours(suit_image.image, self.scale // 8 * -1)
                self.front_image.blit(suit_image.image, (self.scale * 0.7 // 2 - suit_image.image.get_width() / 2, self.scale // 2.75))
                self.front_image.blit(suit_image.image, (self.scale * 0.7 // 2 - suit_image.image.get_width() / 2, self.scale - self.scale // 2.75))

    def add_twos(self, image, x_pos) -> None:
        self.front_image.blit(image, (self.scale * 0.7 // 2 - image.get_width() / 2 - x_pos, self.scale // 4))
        self.front_image.blit(image, (self.scale * 0.7 // 2 - image.get_width() / 2 - x_pos, self.scale - self.scale // 4))

    def add_threes(self, image, x_pos) -> None:
        self.add_twos(image, x_pos)
        self.front_image.blit(image, (self.scale * 0.7 // 2 - image.get_width() / 2 - x_pos, self.scale // 2))

    def add_fours(self, image, x_pos) -> None:
        self.front_image.blit(image, (self.scale * 0.7 // 2 - image.get_width() / 2 - x_pos, self.scale // 4))
        self.front_image.blit(image, (self.scale * 0.7 // 2 - image.get_width() / 2 - x_pos, self.scale // 4 + self.scale // 6))
        self.front_image.blit(image, (self.scale * 0.7 // 2 - image.get_width() / 2 - x_pos, self.scale - self.scale // 4))
        self.front_image.blit(image, (self.scale * 0.7 // 2 - image.get_width() / 2 - x_pos, self.scale - self.scale // 4 - self.scale // 6))
