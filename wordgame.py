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


def num_range(txt):
    '''Gathers range from input. Accounts for various formatting entry.'''
    return [int(s) for s in txt.split() if s.isdigit()]


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
    output.configure(state='normal')
    total = guesses_total(my_game.words_dict)
    my_game.string = ""

    hint.config(text=f"Hint: {shuf(my_game.chosen_word)}")
    for i in my_game.words_dict.values():
        my_game.string = my_game.string + "\n"
        update_list(i, my_game.correct_guesses)
    output.delete(0.0, END)
    output.insert(END, my_game.string)

    if len(my_game.correct_guesses) < total:

        guess = txtinput1.get()
        if my_game.low > len(guess):
            output.delete(0.0, END)
            output.insert(END, my_game.string + "\n\nWord out of range, try again.")
        elif len(guess) > my_game.high:
            output.delete(0.0, END)
            output.insert(END, my_game.string + "\n\nWord out of range, try again.")
        elif guess in my_game.correct_guesses:
            output.delete(0.0, END)
            output.insert(END, my_game.string + "\n\nWord already guessed.")
        else:
            if guess in my_game.words_dict[len(guess)]:
                my_game.correct_guesses.append(guess)
                my_game.string = ""
                for i in my_game.words_dict.values():
                    my_game.string = my_game.string + "\n"
                    update_list(i, my_game.correct_guesses)
                output.delete(0.0, END)
                output.insert(END, my_game.string + "\n\nCorrect!")
            else:
                output.delete(0.0, END)
                output.insert(END, my_game.string + "\n\nSorry. Try again")
            for i in my_game.words_dict.values():
                update_list(i, my_game.correct_guesses)

    if total == len(my_game.correct_guesses):
        output.delete(0.0, END)
        output.insert(END, "You win!")
    else:
        print(my_game.answers)
    txtinput1.delete(0, END)
    output.configure(state='disabled')


def make_dict():
    """Accepts range input and selects a word from range.
    Makes a dict of total word options for the word"""
    with open("words.txt", 'r', encoding="utf-8") as f:
        words = list(f.read().split())

    output.configure(state='normal')
    # add high and low variables
    low = num_range(txtinput1.get())[0]
    high = num_range(txtinput2.get())[0]

    # Puts a cap on length of the highest word
    largest_word = 0
    for item in words:
        if len(item) > largest_word:
            largest_word = len(item)
    if high > largest_word:
        high = largest_word
    if low > largest_word:
        output.delete(0.0, END)
        output.insert(END, "No words of matching length")


    # Creates list of words to be used.
    word_options = [word for word in words if len(word) == high]

    # Randomizes the word
    chosen_word = random.choice(word_options)

    # Returns a list of all words that are subsets of the chosen word
    all_words = [word for word in words if set(word).issubset(chosen_word)
                 if high >= len(word) >= low]

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
    for i in range(low, high + 1):
        words_dict[i] = [word for word in all_words if len(word) == i]

    answers = []
    for k in words_dict:
        for i in words_dict[k]:
            answers.append(i)

    txtinput2.destroy()
    low_label.destroy()
    txtinput1.delete(0, END)
    txtinput1.config(width=20)
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
    output.configure(state='disabled')


my_game = WordGame()
root = Tk()
root.configure(bg='#3C3F41')
root.title("Word Game")
input_frame = Frame(root)

hint = Label(root, text="",bg='#3C3F41', fg='white', font=('Arial', 12))
my_label = Label(root, text="Enter minimum and maximum length of words you would like to use: ", bg='#3C3F41', fg='white', font=('Arial', 12))
txtinput1 = Entry(input_frame, width=5, bg='#3C3F41', fg='white')
txtinput2 = Entry(input_frame, width=5, bg='#3C3F41', fg='white')
btn = Button(root, text="Submit", width=6, bg='#444441', fg='white', command=make_dict, padx=2, pady=2)
my_label2 = Label(root, text="Results", bg='#3C3F41', fg='white')

output = Text(root, width=75, wrap="none")
low_label = Label(input_frame, text="Low: \nHigh: ", bg='#3C3F41', fg='white', padx=2, pady=2)
output.configure(state='disabled', bg='#2B2B2B', fg='white')
sbar = Scrollbar(root, orient=HORIZONTAL)


hint.pack()
output.pack()
sbar.pack(side=BOTTOM, fill=X)
sbar.config(command=output.xview)
my_label.pack()
input_frame.pack()
low_label.pack(in_=input_frame, side=LEFT)
txtinput1.pack(in_=input_frame, side=TOP)
txtinput2.pack(in_=input_frame, side=BOTTOM)
btn.pack()

root.mainloop()
