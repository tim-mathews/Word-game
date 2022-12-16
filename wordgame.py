"""A word guessing game"""
import random
from collections import Counter
from tkinter import *


class WordGame:
    def __init__(self):
        self.words_dict = None
        self.chosen_word = None
        self.high = None
        self.low = None
        self.answers = None
        self.string = ""
        self.correct_guesses = []


def num_range():
    '''Gathers range from input. Accounts for various formatting entry.'''

    num_rng = []

    while len(num_rng) < 2:
        num_rng.clear()
        # rng = input("Enter the range of word lengths (low,high): ")
        nums_str = ""
        rng = txtinput.get()
        for i in rng:
            if i.isnumeric():
                nums_str += i
            else:
                nums_str += " "
        for k in nums_str.split():
            num_rng.append(int(k))
        if len(num_rng) < 2:
            return "Invalid input, please try again.\n"
    return num_rng


def shuf(word):
    """Takes a string as an argument and returns a shuffled version of the word"""
    shuf_word = list(word)
    random.shuffle(shuf_word)
    shuffled_word = ''.join(shuf_word)
    return shuffled_word


def guesses_total(words_dict):
    """Returns the total amount of possible words"""
    total = 0
    for i in words_dict.values():
        total += len(i)
    return total


def update_list(lyst, correct_guesses):
    """Updates the list of currently guessed words"""
    ul = []
    for i in lyst:
        if i in correct_guesses:
            ul.append(f"{i}")
        else:
            ul.append(f"{ '_' * len(i)}")
    if len(ul) > 0:
        my_game.string = my_game.string + str(ul)


def word_game():
    """Function that runs the game after being given the
    chosen word and dict containing words to guess"""
    total = guesses_total(my_game.words_dict)
    my_game.string = ""

    hint.config(text=f"Hint: {shuf(my_game.chosen_word)}")
    for i in my_game.words_dict.values():
        my_game.string = my_game.string + "\n"
        update_list(i, my_game.correct_guesses)
    output.delete(0.0, END)
    output.insert(END, my_game.string)

    if len(my_game.correct_guesses) < total:

        guess = txtinput.get()
        if my_game.low > len(guess):
            output.delete(0.0, END)
            output.insert(END, my_game.string + "\nWord out of range, try again.")
        elif len(guess) > my_game.high:
            output.delete(0.0, END)
            output.insert(END, my_game.string + "\nWord out of range, try again.")
        elif guess in my_game.correct_guesses:
            output.delete(0.0, END)
            output.insert(END, my_game.string + "\nWord already guessed.")
        else:
            if guess in my_game.words_dict[len(guess)]:
                my_game.correct_guesses.append(guess)
                my_game.string = ""
                for i in my_game.words_dict.values():
                    my_game.string = my_game.string + "\n"
                    update_list(i, my_game.correct_guesses)
                output.delete(0.0, END)
                output.insert(END, my_game.string + "\nCorrect!")
            else:
                output.delete(0.0, END)
                output.insert(END, my_game.string + "\nSorry. Try again")
            for i in my_game.words_dict.values():
                update_list(i, my_game.correct_guesses)

    if total == len(my_game.correct_guesses):
        output.delete(0.0, END)
        output.insert(END, "You win!")
    else:
        print(my_game.answers)
    txtinput.delete(0, END)


def make_dict():
    """Accepts range input and selects a word from range.
    Makes a dict of total word options for the word"""
    with open("words.txt", 'r', encoding="utf-8") as f:
        words = list(f.read().split())

    nums = num_range()

    # add high and low variables
    low = nums[0]
    high = nums[1]

    # Puts a cap on length of the highest word
    largest_word = 0
    for item in words:
        if len(item) > largest_word:
            largest_word = len(item)
    if nums[1] > largest_word:
        nums[1] = largest_word
    if low > largest_word:
        print("No words of matching length")
        quit()

    # Creates list of words to be used.
    word_options = [word for word in words if len(word) == nums[1]]

    # Randomizes the word
    chosen_word = random.choice(word_options)

    # Returns a list of all words that are subsets of the chosen word
    all_words = [word for word in words if set(word).issubset(chosen_word)
                 if nums[1] >= len(word) >= nums[0]]

    # Removes words from all words that have too many of any letter
    bl = []
    for letter in chosen_word:
        for word in all_words:
            if Counter(word)[letter] > Counter(chosen_word)[letter]:
                bl.append(word)
    for word in bl:
        if word in all_words:
            all_words.remove(word)

    # Sorts list
    all_words = sorted(all_words)
    # Creates dict of words by word length
    words_dict = {}
    for i in range(nums[0], nums[1] + 1):
        words_dict[i] = [word for word in all_words if len(word) == i]

    answers = []
    for k in words_dict:
        for i in words_dict[k]:
            answers.append(i)

    txtinput.delete(0, END)
    my_label.config(text="Enter a guess")
    btn.configure(command=word_game)

    # Runs the game with chosen words
    my_game.words_dict = words_dict
    my_game.chosen_word = chosen_word
    my_game.low = low
    my_game.high = high
    my_game.answers = answers

    hint.config(text=f"Hint: {shuf(my_game.chosen_word)}")
    for i in my_game.words_dict.values():
        my_game.string = my_game.string + "\n"
        update_list(i, [])
    output.delete(0.0, END)
    output.insert(END, my_game.string)


my_game = WordGame()
root = Tk()
root.title("Word Game")
hint = Label(root, text="Hint: ")
my_label = Label(root, text="Enter minimum and maximum length of words you would like to play with: ")
txtinput = Entry(root, width=20)
btn = Button(root, text="Submit", width=6, command=make_dict)
my_label2 = Label(root, text="Results")
output = Text(root, width=75)

hint.pack()
output.pack()
my_label.pack()
txtinput.pack()
btn.pack()
root.mainloop()
