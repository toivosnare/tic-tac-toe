'''
Ohjelma on skaalautuva versio ristinollasta. Käyttäjälle aukeaa ikkuna, johon
voi syöttää pelin tiedot. Kummallekin pelaajalle voi valita nimen ja värin.
Peliruudukon kokoa ja määrää, kuinka monta ristiä/nollaa tarvitaan riviin
voittaakseen, voi myös muuttaa. Start-nappulan painaminen tarkistaa, että
käyttäjän syöttet ovat kelpaavat ja aloittaa uuden pelin.
'''

from game import Game
import tkinter as tk


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
