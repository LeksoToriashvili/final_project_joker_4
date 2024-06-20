class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.cards_taken = 0
        self.word = 0
        self.on_prime = False
        self.points = 0
        self.total_points = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards):
        self._cards = cards

    @property
    def cards_taken(self):
        return self._cards_taken

    @cards_taken.setter
    def cards_taken(self, cards_taken):
        self._cards_taken = cards_taken

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        self._word = word

    @property
    def on_prime(self):
        return self._on_prime

    @on_prime.setter
    def on_prime(self, on_prime):
        self._on_prime = on_prime

    @property
    def total_points(self):
        return self._total_points

    @total_points.setter
    def total_points(self, total_points):
        self._total_points = total_points

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
