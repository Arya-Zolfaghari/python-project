import sqlite3
import tkinter as tk
from tkinter import messagebox

from click import command

conn = sqlite3.connect('bookstor.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS humans(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
FNAME TEXT NOT NULL,
LNAME TEXT NOT NULL,
BOOK TEXT NOT NULL)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME TEXT NOT NULL,
NUMBER INTEGER NOT NULL)
''')

conn.commit()






class Bookstor:
    def __init__(self, root):
        self.root = root
        self.root.title('Bookstor')
        self.root.geometry('800x900')
        self.root.resizable(False, False)

        self.add_book_name = tk.Entry(root, bg='white', fg='black', font=('Helvetica', 15))
        self.add_book_name.pack(pady=10)

        self.add_book_number = tk.Entry(root, bg='white', fg='black', font=('Helvetica', 15))
        self.add_book_number.pack(pady=10)

        add_button = tk.Button(root, bg="darkblue", fg="white", font=('Helvetica', 15), text='Add', command=self.add_book)
        add_button.pack(pady=30)
        update_button = tk.Button(root,bg="red", fg="white", font=('Helvetica', 15), text='Update', command=self.update)
        update_button.pack(pady=30)

        h_fname_l = tk.Label(root, text="first name :", font=('Helventica', 15))
        h_fname_l.pack(pady=5)
        self.h_fname = tk.Entry(root, bg='white', fg='black', font=('Helvetica', 15))
        self.h_fname.pack(pady=10)

        h_lname_l = tk.Label(root, text="last name :", font=('Helventica', 15))
        h_lname_l.pack(pady=5)
        self.h_lname = tk.Entry(root, bg='white', fg='black', font=('Helvetica', 15))
        self.h_lname.pack(pady=10)

        h_name_book_l = tk.Label(root, text='Book name : ', font=('Helvetica', 15))
        h_name_book_l.pack(pady=5)
        self.h_name_book = tk.Entry(root, bg='white', fg='black', font=('Helvetica', 15))
        self.h_name_book.pack(pady=10)

        h_add_button = tk.Button(root, bg="darkblue", fg="white", font=('Helvetica', 15), text= 'give book', command=self.give)
        h_add_button.pack(pady=30)

        h_remove_button = tk.Button(root, bg="red", fg="white", font=('Helvetica', 15), text= 'returned', command=self.remove)
        h_remove_button.pack(pady=30)



        reserved_books = tk.Button(root,bg='black', fg='white', font=('Helvetica', 15), text = 'reserved books' , command = self.show)
        reserved_books.pack(pady=30)









#
    def give(self):
        name = self.h_fname.get()
        lname = self.h_lname.get()
        book_name = self.h_name_book.get()

        cursor.execute('SELECT NUMBER FROM books WHERE NAME = ?', (book_name,))
        book_result = cursor.fetchone()

        if not book_result or book_result == 0:
            messagebox.showerror('Error', 'This book is not available in the library.')
            return
        elif book_result[0] <= 0:
            messagebox.showerror('Error', 'This book is out of stock.')
            return

        cursor.execute('SELECT * FROM humans WHERE FNAME = ? AND LNAME = ?', (name, lname))
        result = cursor.fetchall()

        if result:
            messagebox.showerror('Error', 'You already have a book. Please return it first.')
        else:
            cursor.execute('INSERT INTO humans(FNAME, LNAME, BOOK) VALUES(?, ?, ?)', (name, lname, book_name))
            conn.commit()

            new_number = book_result[0] - 1
            cursor.execute('UPDATE books SET NUMBER = ? WHERE NAME = ?', (new_number, book_name))
            conn.commit()

            messagebox.showinfo('Give Book', 'Book has been issued successfully.')

    #








    def remove(self):
        name = self.h_fname.get()
        lname = self.h_lname.get()
        book_name = self.h_name_book.get()

        cursor.execute('SELECT * FROM humans WHERE FNAME = ? AND LNAME = ? AND BOOK = ?', (name, lname, book_name))
        result = cursor.fetchone()

        if result:
            cursor.execute('DELETE FROM humans WHERE FNAME = ? AND LNAME = ? AND BOOK = ?', (name, lname, book_name))
            conn.commit()




            cursor.execute('SELECT NUMBER FROM books WHERE NAME = ?', (book_name,))
            book_result = cursor.fetchone()
            new_number = book_result[0] + 1
            cursor.execute('UPDATE books SET NUMBER = ? WHERE NAME = ?', (new_number, book_name))
            conn.commit()



            messagebox.showinfo('Success', 'The book has been returned, and your record has been removed.')

        else:
            messagebox.showerror('Error', 'No matching record found. Please check the details.')

















    def add_book(self):
        name = self.add_book_name.get()
        try:
            number = int(self.add_book_number.get())
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid number.')


        cursor.execute('SELECT NUMBER FROM books WHERE NAME = ?', (name,))
        result = cursor.fetchone()

        if result:
            current_number = result[0]
            new_number = current_number + number
            cursor.execute('UPDATE books SET NUMBER = ? WHERE NAME = ?', (new_number, name))
            conn.commit()
            messagebox.showinfo('Success', 'Book was updated successfully.')




        else:

            try:
                cursor.execute('INSERT INTO books (NAME, NUMBER) VALUES (?, ?)', (name, number))
                conn.commit()
                messagebox.showinfo('Success', 'Book was added successfully.')
            except ValueError:
                print("Invalid number. Please enter a valid integer.")














    def update(self):
        name = self.add_book_name.get()
        try:
            number = int(self.add_book_number.get())
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid number.')

        cursor.execute('SELECT NUMBER FROM books WHERE NAME = ?', (name,))
        result = cursor.fetchone()

        if result:

            new_number = number
            cursor.execute('UPDATE books SET NUMBER = ? WHERE NAME = ?', (new_number, name))
            conn.commit()
            messagebox.showinfo('Success', 'Book was updated successfully.')

    def show(self):
        cursor.execute('SELECT FNAME, LNAME, BOOK FROM humans')
        result = cursor.fetchall()

        if result:
            message = "The list of reserved books is:\n\n"
            for record in result:
                fname, lname, book = record
                message += f"{fname} {lname} - {book}\n"

            messagebox.showinfo('Reserved Books', message)
        else:
            messagebox.showinfo('Reserved Books', 'No books have been reserved yet.')


if __name__ == "__main__":
    root = tk.Tk()
    app = Bookstor(root)
    root.mainloop()















