# Import the speech recognition library
import speech_recognition as sr

# Import the Tkinter library for GUI components
import tkinter as tk

# Import the messagebox module from Tkinter for displaying error messages
from tkinter import messagebox


# Define the function for recognizing speech
def recognize_speech():
    # Create a Recognizer object for speech recognition
    recognizer = sr.Recognizer()

    # Use the default system microphone as the audio source
    with sr.Microphone() as source:
        print("Please speak...")  # Inform the user to start speaking

        # Capture the audio from the microphone
        audio = recognizer.listen(source)

        try:
            # Recognize the captured audio using Google Web Speech API
            text = recognizer.recognize_google(audio, language="en-us") # en-us

            # Update the label to display the recognized text
            result_label.config(text=f"Recognized text: \n{text}")

        # Handle cases where speech is not recognized
        except sr.UnknownValueError:
            # Show an error message if the audio cannot be understood
            messagebox.showerror("Error", "Sorry, could not understand the audio.")

        # Handle network-related errors (e.g., no internet connection)
        except sr.RequestError as e:
            # Show an error message for request-related issues
            messagebox.showerror("Error", f"Request error: {e}")


# Create the main application window
root = tk.Tk()

# Set the title of the application window
root.title("Speech to Text")

# Create a button to start speech recognition and attach the function
start_button = tk.Button(root, text="Start Recognition", command=recognize_speech)

# Add the button to the application window with padding
start_button.pack(pady=10)

# Create a label to display the recognized text
result_label = tk.Label(root, text="Recognized text will appear here.", wraplength=400)

# Add the label to the application window with padding
result_label.pack(pady=10)

# Start the Tkinter main event loop
root.mainloop()
