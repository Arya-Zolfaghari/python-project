
def check_file_exists(file_name):
    """Check if a file exists by attempting to open it."""
    try:
        with open(file_name, 'r'):  
            return True
    except FileNotFoundError:
        print("Your file does not exist. Please check the file name.")
        return False


def new_file():
    while True:
        name_file = input("Enter the name of your file (file.txt): ")
        
        if not check_file_exists(name_file):
            with open(f"{name_file}", "w") as file:
                file.write("") 
            print(f"File '{name_file}' created successfully.")
            break 
        else:
            print("File already exists. Please choose another name.")


def show():
    while True:
        name_file = input("Enter the name of your file (file.txt): ")
        
        if check_file_exists(name_file): 
            with open(f"{name_file}", "r") as file:
                print(file.read())  
            break  
        else:
            print("File does not exist. Try again.")


def edit():
    while True:
        name_file = input("Enter the name of your file (file.txt): ")
        
        if check_file_exists(name_file): 
            text = input("What do you want to write: ")
            a_w = input("Do you want to erase the history (yes/no): ").upper()

            if a_w == "YES": 
                with open(f"{name_file}", "w") as file:
                    file.write(text) 
            elif a_w == "NO":
                with open(f"{name_file}", "a") as file:
                    file.write(text) 
            print(f"File '{name_file}' updated successfully.")
            break 
        else:
            print("File does not exist. Try again.")


def coppy():
    while True:
        f_file = input("Enter the first file name (your file.format): ")
        
        if check_file_exists(f_file):  
            s_file = input("Enter the second file name (your file.format): ")
            
            with open(f"{f_file}", "r") as f_file, open(f"{s_file}", "w") as s_file:
                s_file.write(f_file.read())  
            print(f"Content copied to '{s_file}' successfully.")
            break 
        else:
            print("Source file does not exist. Try again.")


def clear():
    while True:
        name_file = input("Enter the name of your file (file.txt): ")
        
        if check_file_exists(name_file): 
            isclear = input("Do you want to clear the file? (y/n): ").upper()

            if isclear == "Y":
                with open(name_file, "w") as file:
                    file.write("")  
                print(f"File '{name_file}' cleared successfully.")
            break
        else:
            print("File does not exist. Try again.")


def number_of_works():
    while True:
        name_file = input("Enter the name of your file (file.txt): ")
        
        if check_file_exists(name_file): 
            with open(name_file, "r") as file:
                print(f"Number of lines in the file: {len(file.readlines())}")
            break  
        else:
            print("File does not exist. Try again.")


while True:
    answer = int(input("""
1. Create new file
2. Show file
3. Edit file
4. Copy file content
5. Clear file
6. Number of works
7. Exit
                       
Choose an option: """))

    if answer == 1:
        new_file()
    elif answer == 2:
        show()
    elif answer == 3:
        edit()
    elif answer == 4:
        coppy()
    elif answer == 5:
        clear()
    elif answer == 6:
        number_of_works()
    elif answer == 7:
        print("Goodbye!")
        break
