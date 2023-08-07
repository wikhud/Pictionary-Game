# import tkinter.messagebox as messagebox
# import random
# from datetime import datetime, timedelta
# import tkinter as tk
# import numpy as np
# from PIL import Image, ImageDraw
# import tensorflow as tf
# import tkinter.messagebox as messagebox
# import time
# import tkinter as tk
# import numpy as np
# from PIL import Image, ImageDraw
# import tensorflow as tf
# import io
# import tkinter.messagebox as messagebox
# import tkinter.simpledialog as simpledialog
# import random
# import cv2
# from PIL import Image
# import numpy as np
# import tensorflow as tf

# from random import randint
# import numpy as np
# from tensorflow import keras
# from datetime import datetime, timedelta
import random
from datetime import datetime
import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf
import matplotlib.pyplot as plt

# ------------------- GLOBAL VARIABLES -------------------

model_input_image_size = 28
canvas_size = 500, 500

file_path = '/widget_images/'

model = tf.keras.models.load_model('/keras.h5')

with open(('/categories.txt'), 'r') as f:
    words = f.read().splitlines()     

# ------------------- DRAWING -------------------

def start_drawing(event, canvas):
    # Initialize the drawing
    canvas.x = event.x
    canvas.y = event.y
    canvas.current_path = []
    
def draw(event, canvas):
    # Draw lines as the mouse moves
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    current_color = colors[int(event.x % len(colors))]

    canvas.create_line(
        canvas.x, canvas.y, event.x, event.y,
        width = 5,
        smooth=True, splinesteps=100,
        capstyle='round', joinstyle='round',
        fill=current_color, tags='current_path'
    )

    # Update the current point
    canvas.x = event.x
    canvas.y = event.y

    # Add the current point to the current path
    canvas.current_path.append((event.x, event.y))

# ------------------- CLASSIFICATION -------------------

def preprocess(image):
    
    # Resize the image to match the input size of the model (28x28)
    tuple_model_input_image_size = model_input_image_size, model_input_image_size
    resized_image = image.resize(tuple_model_input_image_size)

    # Reverse the colors (invert)
    inverted_image = Image.fromarray(255 - np.array(resized_image))

    # Convert the image to grayscale
    grayscale_image = inverted_image.convert('L')

    # Reshape the image for model input
    sample = np.array(grayscale_image).reshape(-1, model_input_image_size, model_input_image_size, 1).astype('float32')
    # sample = np.array(grayscale_image).reshape(-1, model_input_image_size, 1).astype('float32')

    # Normalize the image
    sample = sample / 255.0

    # plt.imshow(sample.squeeze())
    # plt.show()

    return sample

def classify_image(event, window, canvas, win_count, match_label, word_label, match_button_frame):

    # Get the content of the canvas as an image
    image = Image.new('RGB', canvas_size, 'white')
    draw_obj  = ImageDraw.Draw(image)
    # Iterate over each line segment and draw it on the image
    for path in canvas.find_withtag('current_path'):
        coords = canvas.coords(path)
        draw_obj.line(coords, fill='black', width=20)

    preprocessed_img = preprocess(image)

    # Perform image classification
    predictions = model.predict(preprocessed_img)

    # Get the top 3 class indices and probabilities
    top_indices = np.argsort(-predictions[0])[:3]

    # Get the class names for the top predictions
    top_classes = []
    for i in top_indices:
        top_classes.append(words[i])
    print(top_classes)

    # Check if correct prediction
    new_word = word_label.cget("text")
    if " " or "\n" in new_word:
        new_word = new_word.replace(" ", "_").replace("\n", "_")

    if new_word in top_classes:
        winning(event, canvas, window, win_count, match_label, word_label, match_button_frame)

# ------------------- APP OPTIONS -------------------

def clear_canvas(canvas):
    canvas.delete('all')

def draw_new_word(word_label, canvas, width=10):
    # Choose new word
    new_words = random.choice(words)

    # Adjust size
    if "_" in new_words:
        new_words = new_words.replace("_", " ")

    # Split words if longer than width
    words_list = new_words.split()
    split_words = []
    line = ""
    for word in words_list:
        if len(line + word) <= width or len(words_list) == 1 :
            line += word + " "
        else:
            split_words.append(line.rstrip())
            line = word + " "
    split_words.append(line.rstrip())
    formatted_text = "\n".join(split_words)
    word_label.config(text=formatted_text)

    clear_canvas(canvas)

def update_timer(window, canvas, end_time, win_count, time_label, gover_label, score_label, play_again_button, clear_button, new_word_button, game_over_button_frame):
    # Stop timer
    if hasattr(window, '_after_id'):
        window.after_cancel(window._after_id)

    # Update timer
    remaining_time = end_time - datetime.now()
    minutes = remaining_time.seconds // 60
    seconds = remaining_time.seconds % 60

    if minutes == 0 and seconds == 0:
        game_over(canvas, win_count, time_label, gover_label, score_label, play_again_button, clear_button, new_word_button, game_over_button_frame)
    else:
        time_label.config(text=f'{minutes}:{seconds:02}')

        # Change the color to red when 10 seconds remain
        if minutes == 0 and seconds <= 10 and seconds > 3:
            current_color = time_label.cget("fg")
            if current_color == "red":
                # time_label.config(font=('Comic Sans MS', 20, 'bold'))
                next_color = "#C8BFE7"
            else:
                # time_label.config(font=('Comic Sans MS', 25, 'bold'))
                next_color = "red"
            time_label.config(fg=next_color)
        # Change the color to red when 3nseconds remain
        elif minutes == 0 and seconds <= 3:
            # time_label.config(font=('Comic Sans MS', 25, 'bold'))
            time_label.config(fg='red')
        else:
            time_label.config(fg='#C8BFE7')

        # Start timer
        window._after_id = window.after(1000, lambda: update_timer(window, canvas, end_time, win_count, time_label, gover_label, score_label, play_again_button, clear_button, new_word_button, game_over_button_frame))

def game_over(canvas, win_count, time_label, gover_label, score_label, play_again_button, clear_button, new_word_button, game_over_button_frame):
    # Adjust site
    time_label.config(text='0:00', fg='#C8BFE7', font=('Comic Sans MS', 20, 'bold'))
    score_label.config(text=f'Your score is: {win_count[0]}')

    canvas.create_window(canvas.winfo_width() // 2, canvas.winfo_height() // 2, window=game_over_button_frame, anchor='center')


    clear_button.config(state=tk.DISABLED)
    new_word_button.config(state=tk.DISABLED)        

    # Unbind mouse events to prevent drawing
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind("<ButtonRelease-1>")
        
def winning(event, canvas, window, win_count, match_label, word_label, match_button_frame):
    win_count[0] += 1

    # Unbind mouse events to prevent drawing
    canvas.unbind('<Button-1>')
    canvas.unbind('<B1-Motion>')
    canvas.unbind("<ButtonRelease-1>")
    
    # Adjust site
    canvas.create_window(canvas.winfo_width() // 2, canvas.winfo_height() // 2, window=match_button_frame, anchor='center')

    match_label.update()

    # Wait for 1 second
    window.after(1000)

    # Actions to come back to game

    clear_canvas(canvas)
    draw_new_word(word_label, canvas)
    canvas.bind('<Button-1>', lambda event: start_drawing(event, canvas))
    canvas.bind('<B1-Motion>', lambda event: draw(event, canvas))
    canvas.bind("<ButtonRelease-1>", lambda event: classify_image(event, window, canvas, win_count, match_label, word_label, match_button_frame))

def settings(window, canvas, back_button, set_timing_label, timing_entry, word_label, game_button_frame, settings_button_frame, first_button_frame, setting_button_button_frame, game_over_button_frame):
    # Stop timer
    if hasattr(window, '_after_id'):
        window.after_cancel(window._after_id)

    if first_button_frame.winfo_ismapped():
        first_button_frame.pack_forget()
    # Forget previous site

    if game_button_frame.winfo_ismapped():
        game_button_frame.pack_forget()
    # game_button_frame.pack_forget()
    
    setting_button_button_frame.pack_forget()
    settings_button_frame.pack(pady=50)
    # Adjust new site


def back_to_main_menu(window, start_game_button, setting_button, settings_button_frame, first_button_frame, setting_button_button_frame):
    # Forget previous site

    settings_button_frame.pack_forget()
    # Adjust new site
    first_button_frame.pack()
    setting_button_button_frame.pack(anchor=tk.NE)

# ------------------- WIDGET FUNCTIONS -------------------

def entry_condition(timing_entry):
    if float(timing_entry.get()) < 0.2:
        timing_entry.delete(0, 'end')
        timing_entry.insert(0, "0.5")
