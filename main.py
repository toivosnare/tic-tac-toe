'''
Ohjelma on skaalautuva versio ristinollasta. Käyttäjälle aukeaa ikkuna, johon
voi syöttää pelin tiedot. Kummallekin pelaajalle voi valita nimen ja värin.
Peliruudukon kokoa ja määrää, kuinka monta ristiä/nollaa tarvitaan riviin
voittaakseen, voi myös muuttaa. Start-nappulan painaminen tarkistaa, että
käyttäjän syöttet ovat kelpaavat ja aloittaa uuden pelin.
'''

import tkinter as tk


class Game(tk.Toplevel):
    PADDING = 10
    CELL_SIZE = 50 
    TURN_DISPLAY_HEIGHT = 50

    def __init__(self, cells_x, cells_y, winning_count, players, colors, master, **kw):
        # cells_x: horizontal grid cell amount
        # cells_y: vertical grid cell amount
        # winning_count: amount of lined up marks required to win the game
        # players: list of player names
        # colors: list of player colors
        # master: tkinter master widget
        super().__init__(master, kw)
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.winning_count = winning_count
        self.players = players
        self.colors = colors

        self.title('Tic Tac Toe')
        self.resizable(False, False)
        self.canvas = tk.Canvas(self)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.pack()

        self.grid = [[None for _ in range(self.cells_x)] for _ in range(self.cells_y)]
        self.turn = False
        self.draw_grid()
        self.draw_turn_display()

    def draw_grid(self):
        width = 2 * self.PADDING + self.cells_x * self.CELL_SIZE
        height = 2 * self.PADDING + self.cells_y * self.CELL_SIZE + self.TURN_DISPLAY_HEIGHT
        self.canvas.config(width=width, height=height)

        for i in range(self.cells_x + 1): # Vertical lines
            x = self.PADDING + i * self.CELL_SIZE
            self.canvas.create_line(x, self.TURN_DISPLAY_HEIGHT + self.PADDING, x, height - self.PADDING)

        for i in range(self.cells_y + 1): # Horizontal lines
            y = self.TURN_DISPLAY_HEIGHT + self.PADDING + i * self.CELL_SIZE
            self.canvas.create_line(self.PADDING, y, width - self.PADDING, y)

    def draw_turn_display(self):
        # Display which player's turn it is on top of the window
        if self.turn:
            background0 = 'white'
            text0 = 'black'
            background1 = self.colors[1]
            text1 = 'white'
        else:
            background0 = self.colors[0]
            text0 = 'white'
            background1 = 'white'
            text1 = 'black'
        self.canvas.update()
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width() / 2, self.TURN_DISPLAY_HEIGHT, fill=background0)
        self.canvas.create_text(self.PADDING, self.TURN_DISPLAY_HEIGHT / 2, anchor='w', text=self.players[0], fill=text0)
        self.canvas.create_rectangle(self.canvas.winfo_width() / 2, 0, self.canvas.winfo_width(), self.TURN_DISPLAY_HEIGHT, fill=background1)
        self.canvas.create_text(self.canvas.winfo_width() - self.PADDING, self.TURN_DISPLAY_HEIGHT / 2, anchor='e', text=self.players[1], fill=text1)

    def on_click(self, event):
        # Determine which cell was clicked on.
        # If the cell is free mark it for the player in turn.
        # Check if the mark is a winning move and either display final result or change turns.
        grid_x = (event.x - self.PADDING) // self.CELL_SIZE
        grid_y = (event.y - self.PADDING - self.TURN_DISPLAY_HEIGHT) // self.CELL_SIZE

        try:
            self.grid[grid_y][grid_x]
        except IndexError: # User clicked outside the grid (on padding)
            return

        if self.grid[grid_y][grid_x] == None: # Check clicked cell is empty
            self.grid[grid_y][grid_x] = self.turn
            self.mark(grid_x, grid_y)
            if self.check_win(grid_x, grid_y):
                self.title(f'Tic Tac Toe - {self.players[1] if self.turn else self.players[0]} won!')
                self.canvas.unbind('<Button-1>')
            else:
                self.turn = not self.turn 
                self.draw_turn_display()

    def mark(self, grid_x, grid_y):
        # Mark a cell specified by grid_x and grid_y for the player in turn.
        x0 = self.PADDING + (grid_x + 0.1) * self.CELL_SIZE
        y0 = self.TURN_DISPLAY_HEIGHT + self.PADDING + (grid_y + 0.1) * self.CELL_SIZE
        x1 = self.PADDING + (grid_x + 0.9) * self.CELL_SIZE
        y1 = self.TURN_DISPLAY_HEIGHT + self.PADDING + (grid_y + 0.9) * self.CELL_SIZE

        if self.turn:
            self.canvas.create_oval(x0, y0, x1, y1, width=2, outline=self.colors[1]) # O
        else:
            self.canvas.create_line(x0, y0, x1, y1, width=2, fill=self.colors[0]) # X
            self.canvas.create_line(x0, y1, x1, y0, width=2, fill=self.colors[0])

    def check_win(self, grid_x, grid_y):
        # If marking the cell specified by grid_x and grid_y completes a long enough line
        # for the player in turn return True and highlight the winning line.
        # Otherwise return False.
        for x_offset in range(-1, 2): # Iterate over 8 possible directions to form a line
            for y_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue
                for i in range(1, self.winning_count):
                    try:
                        cell = self.grid[grid_y + i * y_offset][grid_x + i * x_offset]
                    except IndexError: # Grid edge
                        break
                    if not cell == self.turn:
                        break
                else:
                    x0 = self.PADDING + (grid_x + 0.5) * self.CELL_SIZE
                    y0 = self.TURN_DISPLAY_HEIGHT + self.PADDING + (grid_y + 0.5) * self.CELL_SIZE
                    x1 = self.PADDING + (grid_x + 0.5 + i * x_offset) * self.CELL_SIZE
                    y1 = self.TURN_DISPLAY_HEIGHT + self.PADDING + (grid_y + 0.5 + i * y_offset) * self.CELL_SIZE
                    self.canvas.create_line(x0, y0, x1, y1, width=5) # Highlight winning line
                    return True
        return False


def main():
    # Display a window for the user to enter game options and start the game.
    root = tk.Tk()
    root.title('New game')
    root.resizable(False, False)
    frame = tk.Frame(root) # For padding
    frame.grid(padx=(20, 20), pady=(20, 20))

    colors = ('red', 'blue', 'green', 'orange', 'purple', 'yellow')
    name_entries = []
    color_variables = []
    for i in range(2):
        tk.Label(frame, text=f'Player {i + 1}').grid(row=i, column=0, sticky=tk.E, pady=(2, 2))

        name_entry = tk.Entry(frame, width=10) # Player name
        name_entry.insert(tk.END, 'Alice' if i == 0 else 'Bob') # Default values
        name_entry.grid(row=i, column=1, sticky=tk.EW, pady=(2, 2))
        name_entries.append(name_entry)

        color_variable = tk.StringVar(frame)
        color_variable.set(colors[i]) # Default values
        color_menu = tk.OptionMenu(frame, color_variable, *colors) # Player color
        color_menu.grid(row=i, column=2, sticky=tk.W, pady=(2, 2))
        color_variables.append(color_variable)

    grid_spinboxes = []
    tk.Label(frame, text='Grid size').grid(row=2, column=0, sticky=tk.E, pady=(2, 2))
    for i in range(2):
        grid_spinbox = tk.Spinbox(frame, from_=3, to=20, width=3) # Grid size
        grid_spinbox.delete(0, tk.END)
        grid_spinbox.insert(0, 15) # Default values
        grid_spinbox.grid(row=2, column=i + 1, sticky=tk.E if i == 0 else tk.W, pady=(2, 2))
        grid_spinboxes.append(grid_spinbox)

    tk.Label(frame, text='Winning length').grid(row=3, column=0, sticky=tk.E, pady=(2, 2)) # Winning length
    count_spinbox = tk.Spinbox(frame, from_=2, to=10, width=3)
    count_spinbox.delete(0, tk.END)
    count_spinbox.insert(0, 5) # Default value
    count_spinbox.grid(row=3, column=1, sticky=tk.E, pady=(2, 2))

    def start():
        # Instantiate a new game if user entered options are valid.
        try:
            cells_x = int(grid_spinboxes[0].get())
            cells_y = int(grid_spinboxes[1].get())
            assert cells_x > 0 and cells_y > 0
        except (ValueError, AssertionError):
            print('Grid size must be a positive integer')
            return
        try:
            winning_count = int(count_spinbox.get())
            assert winning_count > 0
        except (ValueError, AssertionError):
            print('Winning length must be a positive integer')
            return
        players = (name_entries[0].get(), name_entries[1].get())
        colors = (color_variables[0].get(), color_variables[1].get())
        Game(cells_x, cells_y, winning_count, players, colors, root)
    tk.Button(frame, text='Start', command=start).grid(row=3, column=2, sticky=tk.EW, padx=(2, 0), pady=(2, 2)) # Start button

    root.mainloop()


main()
