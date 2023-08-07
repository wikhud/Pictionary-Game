import tkinter as tk
from datetime import datetime, timedelta
import re
from tkinter import PhotoImage
from game_functions import clear_canvas, draw_new_word, start_drawing, draw, update_timer, settings, back_to_main_menu, classify_image, entry_condition, canvas_size, file_path

# ------------------- GAME -------------------

def start_game():
    # Condition if 1st game or modyfied settings
    if first_button_frame.winfo_ismapped():
        first_button_frame.pack_forget()

    # Condition if another game with the same settings
    if game_over_button_frame.winfo_ismapped():
        clear_canvas(canvas)
    
    # Set variables and actions
    entry_condition(timing_entry)
    end_time = datetime.now() + timedelta(minutes=float(timing_entry.get()))
    win_count = [0]
    canvas.bind('<Button-1>', lambda event: start_drawing(event, canvas))
    canvas.bind('<B1-Motion>', lambda event: draw(event, canvas))
    canvas.bind("<ButtonRelease-1>", lambda event: classify_image(event, window, canvas, win_count, match_label, word_label, match_button_frame))
    draw_new_word(word_label, canvas)
    update_timer(window, canvas, end_time, win_count, time_label, gover_label, score_label, play_again_button, clear_button, new_word_button, game_over_button_frame)
    # Buttons disabled after game over
    clear_button.config(state=tk.NORMAL)
    new_word_button.config(state=tk.NORMAL)

    # Adjust widgets
    game_button_frame.pack()
    setting_button_button_frame.pack_forget()
    setting_button_button_frame.pack(anchor=tk.SE)







# ------------------- MAIN WINDOW SETTINGS -------------------

window = tk.Tk()
window.title("Image Classification")
window.geometry('900x850')
window.configure(background="AliceBlue")
window.update_idletasks()

# ------------------- BUTTON FRAMES -------------------

game_button_frame = tk.Frame(window, bg=window["bg"])
game_up_button_frame = tk.Frame(game_button_frame, bg=window["bg"])
game_down_button_frame = tk.Frame(game_button_frame, bg=window["bg"])
settings_button_frame = tk.Frame(window, bg=window["bg"])
first_button_frame = tk.Frame(window, bg=window["bg"])
setting_button_button_frame = tk.Frame(window, bg=window["bg"])
game_over_button_frame = tk.Frame(window, bg=window["bg"])
match_button_frame = tk.Frame(window, bg=window["bg"])

# ------------------- CANVAS -------------------

width, height = canvas_size
canvas = tk.Canvas(game_button_frame, width=width, height=height, bg=window["bg"], borderwidth=2, highlightbackground='#7092BE')


# ------------------- BUTTON FRAMES PACKING -------------------

game_up_button_frame.pack(pady=20)
canvas.pack()
game_down_button_frame.pack()

# ------------------- BUTTONS -------------------

# Load the image files
clear_image = PhotoImage(file = file_path + "clear.png")
new_word_image = PhotoImage(file = file_path + "new_word.png")
play_again_image = PhotoImage(file = file_path + "play_again.png")
back_image = PhotoImage(file = file_path + "back.png")
start_game_image = PhotoImage(file = file_path + "start.png")
setting_image = PhotoImage(file = file_path + "setting.png")
clear_image = clear_image.subsample(2)
new_word_image = new_word_image.subsample(2)
back_image = back_image.subsample(2)
setting_image = setting_image.subsample(4)

# Create a button to play
start_game_button = tk.Button(first_button_frame, image=start_game_image, text="Let's play!", font=('Comic Sans MS', 40, 'bold'), bg=window["bg"], borderwidth = 0, command=start_game)
start_game_button.pack(pady=100)

# Add a button to clear the canvas
clear_button = tk.Button(game_down_button_frame, image=clear_image, text='Clear', font=('Comic Sans MS', 13, 'bold'), bg=window["bg"],  borderwidth = 0, command=lambda: clear_canvas(canvas))
clear_button.pack(side=tk.LEFT)

# Create a button to draw a new word
new_word_button = tk.Button(game_up_button_frame, image=new_word_image, text='Draw New Word To Draw It!', font=('Comic Sans MS', 13, 'bold'), bg=window["bg"], borderwidth = 0, command=lambda: draw_new_word(word_label, canvas))
new_word_button.pack(side=tk.LEFT, padx=50)


# Create a button to go back to main menu
back_button = tk.Button(settings_button_frame, image=back_image, text='Back to\nmain menu', font=('Comic Sans MS', 10, 'bold'), bg=window["bg"], borderwidth = 0, command=lambda: back_to_main_menu(window, start_game_button, setting_button, settings_button_frame, first_button_frame, setting_button_button_frame))
back_button.pack(anchor=tk.E, pady = 20)

# ------------------- LABELS -------------------

# Add a label to display a drawn word
word_label = tk.Label(game_up_button_frame, text='', font=('Comic Sans MS', 35, 'bold'), fg = '#C8BFE7', bg = window["bg"], width = 10, height = 2)
word_label.pack(side=tk.LEFT)

# Create a label for holding remaining time:
time_label = tk.Label(game_up_button_frame, text='', font=('Comic Sans MS', 20, 'bold'), fg = '#C8BFE7', bg=window["bg"])
time_label.pack(side=tk.LEFT, padx=50)

# Add a label to display "Match!" for a matching word
match_label = tk.Label(match_button_frame, text="MATCH!", font=('Comic Sans MS', 70, 'bold'), fg = 'black', bg=window["bg"])
match_label.pack()

# Create a label for displaying the "Time's up!" at the end:
gover_label = tk.Label(game_over_button_frame, text="Time's up!", font=('Comic Sans MS', 50, 'bold'), fg = 'black', bg=window["bg"])
gover_label.pack()

# Create a label for displaying the score:
score_label = tk.Label(game_over_button_frame, text='', font=('Comic Sans MS', 15, 'bold'), fg= 'black', bg=window["bg"])
score_label.pack()

# Create a label for setting up game timer:
set_timing_label = tk.Label(settings_button_frame, text='Set timer: ', font=('Comic Sans MS', 25, 'bold'),  fg = '#C8BFE7', bg=window["bg"])
set_timing_label.pack(side=tk.LEFT, padx= 20, pady=60)

# ------------------- ENTRY -------------------

# Create a label for getting game timer:
timing_entry = tk.Entry(settings_button_frame)
timing_entry.insert(0, "0.2")  # Set the default value
def validate_entry(text):
    # Regular expression pattern to allow digits and a single decimal point
    pattern = r'^\d*\.?\d*$'
    # Check if the entered text matches the pattern
    return re.match(pattern, text) is not None
# validation = window.register(validate_entry)
validation = settings_button_frame.register(validate_entry)
timing_entry.configure(bg=window["bg"], fg = 'black',  borderwidth = 0, font=('Comic Sans MS', 25, 'bold'), width=5, validate="key", validatecommand=(validation, "%P"))
timing_entry.pack(side=tk.LEFT, padx= 20, pady=60)


# Create a button to go to settings and pack button_frame to dispaly it
setting_button = tk.Button(first_button_frame, image=setting_image, text="Settings", font=('Comic Sans MS', 10, 'bold'), bg=window["bg"], borderwidth = 0, command=lambda: settings(window, canvas, back_button, set_timing_label, timing_entry, word_label, game_button_frame, settings_button_frame, first_button_frame, setting_button_button_frame, game_over_button_frame))

setting_button_2 = tk.Button(setting_button_button_frame, image=setting_image, text="Settings", font=('Comic Sans MS', 10, 'bold'), bg=window["bg"], borderwidth = 0, command=lambda: settings(window, canvas, back_button, set_timing_label, timing_entry, word_label, game_button_frame, settings_button_frame, first_button_frame, setting_button_button_frame, game_over_button_frame))
setting_button_2.pack()

# Create a button to play again
play_again_button = tk.Button(game_over_button_frame, image=play_again_image, text='Play again!', font=('Comic Sans MS', 25, 'bold'), bg=window["bg"], borderwidth = 0, command=start_game)
play_again_button.pack(pady = 50)

first_button_frame.pack()
setting_button_button_frame.pack(anchor=tk.NE)

window.mainloop()
