#printer_style must be "icon" or "hybrid"

BLACK = '\033[30m'
RED = '\033[31m'
BACKGROUND_WHITE = '\033[107m'
RESET = '\033[0m'
CARD_BACK = chr(0x1F0A0)


class Printer:
    def __init__(self, printer_style="hybrid"):
        self.printer_style = printer_style

    @property
    def printer_style(self):
        return self._printer_style

    @printer_style.setter
    def printer_style(self, style):
        self._printer_style = style

    def print_card(self, card):
        if self._printer_style == "hybrid":
            background = BACKGROUND_WHITE
            color = str()
            if card[-1] == 'H':
                card = card.replace('H', chr(9829))
                color = RED
            elif card[-1] == 'S':
                card = card.replace('S', chr(9827))
                color = BLACK
            elif card[-1] == 'D':
                card = card.replace('D', chr(9830))
                color = RED
            elif card[-1] == 'C':
                card = card.replace('C', chr(9824))
                color = BLACK
            elif card == "JR":
                card = chr(0x1F0CF)
                color = RED
            elif card == "JB":
                card = chr(0x1F0CF)
                color = BLACK
            else:
                raise ValueError("Invalid card type")
            print(background + color + card + RESET, end='')

    def print_cards(self, cards, separator=' '):
        if self._printer_style == "hybrid":
            for card in cards:
                self.print_card(card)
                print(separator, end='')

    def print_cards_number(self, cards, separator=' '):
        if self._printer_style == "hybrid":
            i = 1
            for card in cards:
                print(str(i) + ':', end='' )
                self.print_card(card)
                print(separator, end='')
                i += 1
