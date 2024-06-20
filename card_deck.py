class CardDeck:
    ranks = ('6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
    suits = ('H', 'S', 'D', 'C')
    fine = -500

    @staticmethod
    def full_deck() -> list:
        full_deck = list()

        for rank in CardDeck.ranks:
            for suit in CardDeck.suits:
                full_deck.append(rank + suit)
        full_deck.remove("6S")
        full_deck.remove("6C")
        full_deck.append("JB")
        full_deck.append("JR")

        return full_deck

    @staticmethod
    def points(word: int, taken: int) -> int:
        if word != 0 and taken == 0:
            return CardDeck.fine

        if word == taken:
            return 50 + word * 50 if word != 9 else 900

        return taken * 10

    @staticmethod
    def highest_card(cards, suit):
        if CardDeck.has_suit(cards, suit):
            ranks = list(CardDeck.ranks)
            ranks.reverse()
            for rank in ranks:
                if rank + suit in cards:
                    return rank + suit
        else:
            return None

    @staticmethod
    def has_suit(cards, suit):
        for card in cards:
            if card[-1] == suit:
                return True
        return False

    @staticmethod
    def sort_cards(cards):
        res = []
        if 'JB' in cards:
            res.append('JB')
            cards.remove('JB')
        if 'JR' in cards:
            res.append('JR')
            cards.remove('JR')

        for suit in CardDeck.suits:
            highest_card = True
            while highest_card:
                highest_card = CardDeck.highest_card(cards, suit)
                if highest_card:
                    res.append(highest_card)
                    cards.remove(highest_card)
        return res
