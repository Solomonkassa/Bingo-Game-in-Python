import random
import tkinter as tk
from tkinter import messagebox
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

class BingoBoard:
    def __init__(self, master):
        self.master = master
        master.title("Bingo Game")

        # Create a list of numbers from 1 to 25, shuffle it and assign it to self.numbers
        self.numbers = list(range(1, 26))
        random.shuffle(self.numbers)

        # Create the grid of squares for the numbers
        self.grid = []
        for i in range(5):
            row = []
            for j in range(5):
                # Create a button for each square, add it to the grid and assign it a number from self.numbers
                button = tk.Button(master, width=5, height=2, font=("Helvetica", 12), command=lambda i=i, j=j: self.mark_square(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.grid.append(row)

        # Assign the numbers to the buttons
        for i in range(5):
            for j in range(5):
                self.grid[i][j].config(text=self.numbers.pop())

        # Create button to check for a win
        self.check_button = tk.Button(master, text="Check", width=10, command=self.check_win)
        self.check_button.grid(row=6, column=2)
        
        # Create a model to predict the next number
        self.model = Sequential()
        self.model.add(Dense(5, input_dim=25, activation='relu'))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def check_win(self):
        """Check for a win and show a messagebox if the player wins"""
        for i in range(5):
            for j in range(5):
                if self.grid[i][j]["text"] != "X":
                    return

        messagebox.showinfo("Bingo!", "You win!")

    def predict_next_number(self):
        """Predict the next number to be called, but keep in mind the model is not trained, so it's not capable of making accurate predictions"""
        data = []
        for i in range(5):
            for j in range(5):
                data.append(int(self.grid[i][j]["text"]))
        next_number = self.model.predict(data)
        return int(next_number)

    def mark_square(self, i, j):
        """Mark the square by changing its text to 'X'"""
        self.grid[i][j].config(text="X")


root = tk.Tk()
board = BingoBoard(root)
root.mainloop()
