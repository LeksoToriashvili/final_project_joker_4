from player import Player
from card_deck import CardDeck
from printer import Printer
from file_handler import FileHandler
import random


class GameFlow:
    def __init__(self):
        self._data = dict()
        self._players = None
        self._first_player = 0
        self._current = None
        self._round = 1
        self._quarter = 1
        self._bower = None
        self._printer = Printer()
        self._board = []
        self._words_said = 0
        self._jr = None
        self._jb = None
        self._logger = FileHandler()

    def init_players(self):
        player_names = set()
        while len(player_names) < 4:
            input_name = input(f"Input player{len(player_names) + 1} name: ").strip()
            if input_name == '' or len(input_name) > 20:
                print("name must contain at least one character and must be less than 20 characters...")
                continue
            player_names.add(input_name)

        self._players = tuple(Player(player_names.pop()) for _ in range(4))
        self._data["players"] = [p.name for p in self._players]
        for player in self._players:
            print(player.name, end='\t')
        print()

    def play(self):
        self.init_players()
        for _ in range(4):
            for player in self._players:
                player.on_prime = True
                player.points = 0
            self.play_quarter()
            self._quarter += 1
            self._round = 1
        self.log()

    def log(self):
        user_input = input("Do you want to save game(y/n)")
        if user_input == 'y' or user_input == 'Y':
            self._logger.save(self._data)

    def play_quarter(self):
        self._data[self._quarter] = dict()

        for player in self._players:
            player.on_prime = True

        for i in range(4):
            self._first_player = i
            self._current = self._first_player
            self.deal()
            self.set_bower()
            self.sort_cards()
            self.say_words()
            self.play_hand()
            self.set_points_and_prime()

            self._data[self._quarter][self._round] = []
            for player in self._players:
                self._data[self._quarter][self._round].append(player.word)
                self._data[self._quarter][self._round].append(player.points)
                if player.word != player.cards_taken:
                    player.on_prime = False
                player.cards_taken = 0
                player.word = 0
                player.points = 0
            if self._round < 4:
                self.print_points_table()
            self._words_said = 0
            self._jr = None
            self._jb = None
            self._round += 1

        for index in range(4):
            if self._players[index].on_prime:
                high_score_list = max(self._data[self._quarter].values(), key=lambda val: val[2 * index + 1])
                self._players[index].total_points += high_score_list[2 * index + 1]

        self._data[self._quarter][self._round] = []
        for player in self._players:
            self._data[self._quarter][self._round].append(player.total_points)

        self.print_points_table()

    def print_points_table(self):
        for player in self._data["players"]:
            print(player, end='\t\t')
        print()

        for q in range(5):
            if q in self._data:
                print("quarter " + str(q) + ":")
                for val in self._data[q].values():
                    if len(val) == 4:
                        for i in range(4):
                            print(f"{val[i]}", end='\t\t')
                        print()
                    else:
                        for i in range(4):
                            print(f"{val[2 * i]}: {val[2 * i + 1]}", end='\t\t')
                        print()
        print()

    def set_points_and_prime(self):
        for player in self._players:
            player.points = CardDeck.points(player.word, player.cards_taken)
            player.total_points += player.points
            if player.word != player.cards_taken:
                player.on_prime = False

    def set_bower(self):
        print(self._players[self._first_player].name + ': ')
        suits = ['D', 'H', 'S', 'C']
        self._printer.print_cards(self._players[self._first_player].cards[0:3])
        print()
        self._printer.print_cards_number(suits)
        index = GameFlow.input_index(4, "Please choose bower or hit enter for play without bower: ")
        if index:
            self._bower = suits[index - 1]
            print("bower is : ", end='')
            self._printer.print_card(self._bower)
            print('\n')
        else:
            self._bower = None
            print("Playing without bower")
            print('\n')

    def deal(self):
        deck = CardDeck.full_deck()
        for player in self._players:
            for _ in range(9):
                card = random.choice(deck)
                deck.remove(card)
                player.cards.append(card)

    def play_hand(self):
        print(f"\nround {self._round} begin: ")
        for _ in range(9):
            for _ in range(4):
                self.lead_card()
                self._current = self.next_player
                print("\nBoard: ", end='')
                self._printer.print_cards(self._board, separator=' ')
                print()

            player_index = self._current + self.who_takes_cards()
            if player_index > 3:
                player_index = player_index % 4
            self._current = player_index
            self.player.cards_taken += 1

            print(self.player.name, "takes cards")
            for player in self._players:
                print(f"{player.name}: {player.cards_taken}", end='     ')
            print('\n')
            self._board.clear()

    def who_takes_cards(self):
        command, main_suit = self.command_and_main_suit()

        for i in range(3, -1, -1):
            if self._board[i] == 'JR':
                if self._jr == "Get":
                    return i
            if self._board[i] == 'JB':
                if self._jb == "Get":
                    return i

        if command == "Get":
            return 0

        bower_on_board = False
        for card in self._board[0:4]:
            if card[-1] == self._bower:
                bower_on_board = True

        if command == "Request":
            if main_suit == self._bower:
                return 0
            else:
                if not bower_on_board:
                    return 0

        if bower_on_board:
            highest_card = CardDeck.highest_card(self._board, self._bower)
            return self._board.index(highest_card)

        highest_card = CardDeck.highest_card(self._board, main_suit)
        return self._board.index(highest_card)

    def lead_card(self):
        print(self.player.name + ': ', end='')
        self._printer.print_cards_number(self.player.cards)
        print()

        text = "Please choose a card to lead: "
        card_index = GameFlow.input_index(len(self.player.cards), text)
        while True:
            if card_index and self.legal_move(self.player.cards[card_index - 1]):
                if self.player.cards[card_index - 1] in ('JB', 'JR'):
                    self.joker_actions(self.player.cards[card_index - 1])
                self._board.append(self.player.cards[card_index - 1])
                self.player.cards.pop(card_index - 1)
                break
            text = "Please choose a valid card to lead: "
            card_index = GameFlow.input_index(len(self.player.cards), text)

    def legal_move(self, card):
        if len(self._board) == 0:
            return True

        if card in ('JR', 'JB'):
            return True

        command, main_suit = self.command_and_main_suit()

        if command == "Get":
            return True

        if CardDeck.has_suit(self.player.cards, main_suit):
            if command == "Request":
                if CardDeck.highest_card(self.player.cards, main_suit) == card:
                    return True
                else:
                    return False
            if card[-1] == main_suit:
                return True
        elif CardDeck.has_suit(self.player.cards, self._bower):
            if card[-1] == self._bower:
                return True
        else:
            return True
        return False

    def command_and_main_suit(self):
        command = None
        main_suit = None

        first_card = self._board[0]
        if first_card not in ('JR', 'JB'):
            main_suit = first_card[-1]
        else:
            if first_card == 'JR':
                if self._jr != "Get":
                    command = self._jr.split(':')[0]
                    main_suit = self._jr.split(':')[1]
            if first_card == 'JB':
                if self._jb != "Get":
                    command = self._jb.split(':')[0]
                    main_suit = self._jb.split(':')[1]
        return command, main_suit

    def joker_actions(self, joker):
        command = None
        if len(self._board) == 0:
            text = "Please choose an action:\t1: Get(*Request high bower)\t2: Request high card\t3: Give it to suit: "
            index = GameFlow.input_index(3, text)
            if index in (0, 1):
                command = "Get"
                if self._bower:
                    command = "Request:" + self._bower
            else:
                self._printer.print_cards_number(CardDeck.suits)
                suit_index = GameFlow.input_index(4, "Please choose a suit: ")
                if suit_index == 0:
                    suit_index = 1
                suit = CardDeck.suits[suit_index - 1]
                if index == 2:
                    command = "Request:" + suit
                if index == 3:
                    command = "Give:" + suit
        else:
            action = GameFlow.input_index(2, "Please choose an action:\t1: Get\t2: Give: ")
            if action == 2:
                command = "Under"
            else:
                command = "Get"

        if joker == 'JR':
            self._jr = command
        else:
            self._jb = command

    def say_words(self):
        for _ in range(4):
            print(self.player.name + ': ')
            self._printer.print_cards(self.player.cards)
            print()

            if self._first_player == self.next_player:
                restricted = 9 - self._words_said
                text = f"Say the word(0-9), or hit enter for pass(you can't say {restricted}): "
                if restricted < 0:
                    restricted = None
                    text = "Say the word(0-9), or hit enter for pass: "
                word = restricted
                while word == restricted:
                    word = GameFlow.input_index(9, text)
            else:
                text = f"Say the word(0-9), or hit enter for pass: "
                word = GameFlow.input_index(9, text)

            self._words_said += word
            self.player.word = word
            self._current = self.next_player

        print("\nwords - ", end='')
        for player in self._players:
            print(f"{player.name}: {player.word}", end='\t\t')
        print()

    def sort_cards(self):
        for player in self._players:
            player.cards = CardDeck.sort_cards(player.cards)

    @property
    def player(self):
        return self._players[self._current]

    @property
    def next_player(self):
        next_player = self._current + 1
        if next_player >= 4:
            next_player = 0
        return next_player

    @staticmethod
    def input_index(count, text):
        while True:
            user_input = input(text)
            if user_input == '' or user_input == '0':
                return 0
            try:
                index = int(user_input)
            except Exception:
                print("Try to enter number")
                continue
            if not (0 < index < count + 1):
                print("Wrong input!")
                continue
            return index
