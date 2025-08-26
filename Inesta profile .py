from tkinter import *
import instaloader
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO

def get_image():
    try:
        # Initialize Instaloader and log in
        L = instaloader.Instaloader()
        L.login("YOUR USER NAME ", "YOUR PASSWORD ")
        
        # Get profile details
        profile = instaloader.Profile.from_username(L.context, username.get())

        # Download profile picture
        a = urlopen(profile.get_profile_pic_url())
        data = a.read()
        a.close()
        
        # Process and display image
        image = Image.open(BytesIO(data))
        image = image.resize((200, 200))
        pic = ImageTk.PhotoImage(image)
        picture.config(image=pic)
        picture.image = pic
        
        # Update followers and following
        followers.config(text=f"Followers: {profile.followers}")
        followees.config(text=f"Followees: {profile.followees}")
        
    except instaloader.exceptions.LoginRequiredException:
        error_label.config(text="Login required or failed!")
    except instaloader.exceptions.ProfileNotExistsException:
        error_label.config(text="Profile does not exist!")
    except Exception as e:
        error_label.config(text=f"Error: {str(e)}")

# Initialize window
window = Tk()
window.title("Instagram Profile Downloader")
window.geometry("600x600")

# Widgets
l1 = Label(window, text="Enter the username", font=("Arial", 20, "bold"))
username = Entry(window, font=("Arial", 18, "bold"))
button = Button(window, text="Download", font=("Arial", 16, "bold"), bg="darkblue", fg="white", command=get_image)

picture = Label(window)
followers = Label(window, text="Followers: ", font=("Arial", 16, "bold"))
followees = Label(window, text="Followees: ", font=("Arial", 16, "bold"))
error_label = Label(window, text="", font=("Arial", 12, "bold"), fg="red")

# Pack widgets
l1.pack()
username.pack()
button.pack()
picture.pack()
followers.pack()
followees.pack()
error_label.pack()

# Run the app
window.mainloop()

