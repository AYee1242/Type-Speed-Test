import tkinter
import requests
from tkinter import Label, Text, INSERT

# Constants
BLUE = "#333652"
LIGHT_BLUE = "#90ADC6"
WHITE = "#E9EAEC"
RED = "#ff726f"
FONT = "Courier"


class TypeSpeed:
    def __init__(self):
        self.correct_characters = 0
        self.incorrect_words = 0
        self.typed_incorrectly = False

        # UI setup
        # Window
        self.window = tkinter.Tk()
        self.window.title("Speed Test")
        self.window.config(width=500, height=500,
                           background=BLUE, pady=50, padx=50)

        # Title
        self.title_label = Label(text="Typing Speed Test",
                                 font=(FONT, 50, "bold"), fg=WHITE, bg=BLUE)
        self.title_label.grid(column=0, row=0, pady=(0, 50))

        # Getting list of random words
        response = requests.get(
            "https://random-word-api.herokuapp.com/word?number=1000")
        words_list = response.json()

        # Input text box
        self.text = Text(self.window, bg=WHITE, height=1, width=52, font=(FONT, 30),
                         wrap="word", highlightthickness=0)
        self.text.grid(column=0, row=2)
        self.text.focus()
        self.text.insert(INSERT, words_list)
        self.text.mark_set("insert", "%d.%d" % (1.0, 0.0))
        self.text.tag_add("start", "1.0", "5.0")
        self.text.tag_config("start", background=WHITE, foreground=BLUE)
        self.text.config(bg=LIGHT_BLUE)
        self.text.bind("<Key>", self.type_check)

        # Timer
        self.timer_label = Label(text="60", font=(
            FONT, 30, "bold"), fg=WHITE, bg=BLUE)
        self.timer_label.grid(column=0, row=1)

    def start(self):
        self.count_down(60)
        self.window.mainloop()

    # Count down mechanism
    def count_down(self, count):
        if count > 0:
            self.window.after(1000, self.count_down, count - 1)
            self.timer_label.config(text=count)
        else:
            self.final_results()

    # Checking user input

    def type_check(self, key):

        if self.text.get("insert") == key.char:
            insert = self.text.index("insert")
            self.text.delete(insert)
            self.correct_characters += 1
            self.typed_incorrectly = False
            self.text.config(bg=LIGHT_BLUE)
        else:
            # Prevent multiple errors for the same word
            if self.typed_incorrectly == False:
                self.typed_incorrectly = True
                self.incorrect_words += 1
                self.text.config(bg=RED)

    def final_results(self):
        # Removing unnecessary widgets
        self.timer_label.destroy()
        self.text.destroy()

        # Calculating results
        correct_words = self.correct_characters / 5
        net_wpm = correct_words - self.incorrect_words
        accuracy = (float(net_wpm) / float(correct_words)) * 100

        # Formatting data
        net_wpm = '{0:.0f}'.format(net_wpm)
        accuracy = f"{'{0:.2f}'.format(accuracy)}%"

        self.title_label.config(text="Time's Up!")
        wpm_label = Label(text=f"WPM : {net_wpm} words", font=(
            FONT, 30), fg=WHITE, bg=BLUE, padx=20, pady=20)
        wpm_label.grid(column=0, row=1)

        accuracy_label = Label(text=f"Accuracy : {accuracy}", font=(
            FONT, 30), fg=WHITE, bg=BLUE, padx=20, pady=20)
        accuracy_label.grid(column=0, row=2)