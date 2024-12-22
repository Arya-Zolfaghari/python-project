import tkinter as tk
from tkinter import ttk
import pyttsx3 as tts

def speak_text():
    text = entry.get()  # Get the text from the input field
    if text:  # Check if the input field is not empty
        engin.setProperty("voice", voices[voice_combobox.current()].id)  # Select the speaker's voice
        engin.say(text)
        engin.runAndWait()

# Create the main window
screen = tk.Tk()
screen.config(bg="lightgreen")
screen.minsize(300, 200)

# Label
label = tk.Label(screen, bg="white", text="Text to Speech (EN)")
label.pack()

# Spacer
spase = tk.Label(screen, bg="lightgreen", text=" ")
spase.pack()

# Input field
entry = tk.Entry(screen, bg="white")
entry.pack()

# Dropdown menu for selecting voice
voices = tts.init().getProperty('voices')
voice_names = [voice.name for voice in voices]

voice_combobox = ttk.Combobox(screen, values=voice_names)
voice_combobox.set("Select Voice")  # Default option
voice_combobox.pack(pady=5)

# Button to convert text to speech
btn = tk.Button(screen, text="Speak", command=speak_text)
btn.pack()

# Speech engine settings
engin = tts.init()
engin.setProperty("rate", 150)
engin.setProperty("volume", 0.1)

# Run the main loop of the program
screen.mainloop()