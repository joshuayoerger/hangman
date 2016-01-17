from functools import partial
import os
import random

from graphics import Graphics


class Hangman():
    graphics = Graphics()

    def word_list(self):
        f = open('/usr/share/dict/words')
        for line in f.readlines():
            yield line.strip()
        else:
            f.close()

    def word_length(self, word, length):
        return len(word) <= length and len(word) > 5

    def filter_words(self, length):
        return filter(
            partial(self.word_length, length=length), self.word_list()
            )

    def clear_display(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu(self):
        self.clear_display()
        print(self.graphics.title)
        print('[N]ew Game')
        print('[H]elp')
        print('[Q]uit')
        choice = input('>>> ').lower()

        if choice in 'nhq' and len(choice) == 1:
            return choice
        else:
            return self.menu()

    def get_difficulty(self):
        print('Select Difficulty: [E]asy, [M]edium, or [H]ard')
        difficulty = input('>>> ').lower()
        if difficulty in 'emh'and len(difficulty) == 1:
            return difficulty
        else:
            print('Invalid entry.')
            return self.get_difficulty()

    def draw_board(self):
        return '_'*len(self.current_word)

    def update_board(self):
        return ''.join(letter if letter in self.guesses and
                       letter in self.current_word
                       else '_' for letter in self.current_word)

    def setup(self):
        self.missed = []
        self.guesses = set()
        self.difficulty = self.get_difficulty()
        if self.difficulty == 'e':
            self.word_list = self.easy
        elif self.difficulty == 'm':
            self.word_list = self.med
        else:  # if self.difficulty == 'h':
            self.word_list = self.hard

        self.current_word = self.word_list.pop().lower()
        self.board = self.draw_board()

    def __init__(self):
        self.easy = random.sample(list(self.filter_words(7)), 50)
        self.med = random.sample(list(self.filter_words(9)), 50)
        self.hard = random.sample(list(self.filter_words(12)), 50)

        while True:
            choice = self.menu()
            if choice == 'n':
                self.setup()

                while True:
                    self.clear_display()
                    self.graphics.print_graphics(self.missed)
                    print('Guesses: {}'.format(', '.join(self.guesses)))
                    # print(self.current_word)
                    print('Secret Word: {}'.format(self.board))
                    print('Guess a letter or enter \'menu\'')
                    self.guess = input('>>> ')
                    self.guesses.add(self.guess)

                    if self.guess == 'menu':
                        break

                    if self.guess in self.current_word:
                        self.board = self.update_board()
                    else:
                        self.missed.append(self.guess)

                    if len(self.missed) == 7:
                        self.clear_display()
                        self.graphics.print_graphics(self.missed)
                        print('Sorry, you lost. The word was \"{}\".'
                              .format(self.current_word))
                        print('Try again? [Y]es/[N]o')

                        if input('>>> ').lower() == 'y':
                            break
                        else:
                            raise SystemExit

                    if '_' not in self.board:
                        print('You won! The word was \"{}\".'
                              .format(self.current_word))
                        print('Play again? [Y]es/[N]o')

                        if input('>>> ').lower() == 'y':
                            break
                        else:
                            raise SystemExit
            # elif choice == 'h':
                # Show help. Use docstring?
            else:  # self.menu() == 'q':
                raise SystemExit

if __name__ == '__main__':
    Hangman()
