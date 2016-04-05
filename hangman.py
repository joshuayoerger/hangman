#!/usr/bin/env python3
"""
Computer version of the game hangman.

Inspired by the classic text-based games distributed with some versions of BSD
and linux.
"""

import os
import random

import graphics  # Contains ASCII art for the game


def clear_display():
    """Sends appropriate 'clear screen' command to the system."""
    os.system('cls' if os.name == 'nt' else 'clear')


def word_generator():
    """Yields a generator object from the standard unix word list."""
    f = open('/usr/share/dict/words')
    for line in f.readlines():
        yield line.strip()
    else:
        f.close()


class Hangman():
    def __init__(self):
        self.guesses, self.bad_guesses = set(), set()
        self.game_words = self.get_words()
        self.current_word = self.game_words.pop().lower()
        self.blanks = self.get_blanks()
        self.game_over, self.game_won = False, False

    def __str__(self):
        """Allows game graphics and info to be displayed with a print() call"""
        return ("{}\n{}\nSecret Word: {}\nGuessed: {}\nMissed: {}/7\n"
                .format(graphics.TITLE_ART,
                        graphics.GALLOWS_ART[len(self.bad_guesses)],
                        self.blanks,
                        ', '.join(sorted(self.guesses)),
                        len(self.bad_guesses)
                        ))

    def print_screen(self):
        """Clears the screen then prints game graphics using __str__."""
        clear_display()
        print(self)

    def get_words(self):
        """Returns a random sample of 50 words in a list."""
        return random.sample([word for word in word_generator()
                              if len(word) >= 6], 50)

    def get_blanks(self):
        """Generates blanks and letters for secret word."""
        return ''.join(letter if letter in self.guesses and
                       letter in self.current_word
                       else '_' for letter in self.current_word)

    def get_guess(self):
        """Gets a new guess from user and updates attributes as necessary."""
        new_guess = input("Guess a letter: ")
        if len(new_guess) > 1 or not new_guess.isalpha():
            print("Please enter a (single) letter of the alphabet!")
            return self.get_guess()
        else:
            self.guesses.add(new_guess)
            self.bad_guesses = self.guesses.difference(set(self.current_word))
            self.blanks = self.get_blanks()

    def set_state(self):
        """ Sets game state via 'game_over' and 'game_won'"""
        if len(self.bad_guesses) >= 7:
            self.game_over, self.game_won = True, False
        if '_' not in self.blanks:
            self.game_over, self.game_won = True, True

    def play_again(self):
        """Prompts user to quit or setup new round."""
        if input('Try again? [Y]es/[N]o: ').lower() == 'y':
            self.current_word = self.game_words.pop().lower()
            self.guesses, self.bad_guesses = set(), set()
            self.blanks = self.get_blanks()
            self.game_over, self.game_won = False, False
        else:
            print("Thank you for playing!")
            raise SystemExit


def game():
    game = Hangman()  # Creates a new game instance.
    while True:
        while not game.game_over:
            game.print_screen()  # Prints ASCII art, blanks, and info.
            game.get_guess()  # Gets guess from user and updates attributes.
            game.set_state()  # Checks and sets game state.
        if game.game_won:  # If game is over, checks if game was won.
            game.print_screen()
            print("You guessed it - Great job!")
        else:
            game.print_screen()
            print("You ran out of guesses. The word was '{}'."
                  .format(game.current_word))
        game.play_again()

if __name__ == '__main__':  # Execute game if run as script:
    game()
