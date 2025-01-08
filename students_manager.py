
import sqlite3
from tkinter import *
from tkinter import messagebox

conn = sqlite3.connect('students_manager.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FNAME TEXT NOT NULL,
    LNAME TEXT NOT NULL,
    GRADE INTEGER,
    STATUS INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS grades (
    STUDENT_ID INTEGER,
    SUBJECT TEXT NOT NULL,
    GRADE INTEGER,
    FOREIGN KEY (STUDENT_ID) REFERENCES students(ID)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    STUDENT_ID INTEGER,
    DATE TEXT NOT NULL,
    STATUS TEXT NOT NULL,
    FOREIGN KEY (STUDENT_ID) REFERENCES students(ID)
)
''')


class Students_Manager:






    def __init__(self, root):
        self.root = root
        self.root.title('Student Manager')
        self.root.geometry('800x800')
        self.root.resizable(False, False)

        self.entries = []

        self.create_widgets()







    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack(pady=10)

        Label(self.frame, text="First Name", font=('Arial', 12)).grid(row=0, column=0)
        Label(self.frame, text="Last Name", font=('Arial', 12)).grid(row=1, column=0)
        Label(self.frame, text="Grade", font=('Arial', 12)).grid(row=2, column=0)
        Label(self.frame, text="Status", font=('Arial', 12)).grid(row=3, column=0)

        self.fname_entry = Entry(self.frame, font=('Arial', 12))
        self.fname_entry.grid(row=0, column=1)

        self.lname_entry = Entry(self.frame, font=('Arial', 12))
        self.lname_entry.grid(row=1, column=1)

        self.grade_entry = Entry(self.frame, font=('Arial', 12))
        self.grade_entry.grid(row=2, column=1)

        self.status_entry = Entry(self.frame, font=('Arial', 12))
        self.status_entry.grid(row=3, column=1)

        Button(self.root, text="Add Student", command=self.add_student, font=('Arial', 12)).pack(pady=10)
        Button(self.root, text="View Students", command=self.view_students, font=('Arial', 12)).pack(pady=10)














    def add_student(self):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        grade = self.grade_entry.get()
        status = self.status_entry.get()

        if fname and lname and grade and status:
            cursor.execute('''INSERT INTO students(FNAME, LNAME, GRADE, STATUS) VALUES(?,?,?,?)''',(fname, lname, grade, status))
            conn.commit()

            messagebox.showinfo("Success", "Student added successfully")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")









    def view_students(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("View Students")
        self.new_window.geometry("600x400")

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        for idx, student in enumerate(students, start=1):
            Label(self.new_window,
                  text=f"ID: {student[0]}, Name: {student[1]} {student[2]}, Grade: {student[3]}, Status: {student[4]}",
                  font=('Arial', 12)).grid(row=idx, column=0, sticky="w", pady=5)
            Button(self.new_window, text="Edit", command=lambda id=student[0]: self.edit_student(id),
                   font=('Arial', 12)).grid(row=idx, column=1)
            Button(self.new_window, text="Delete", command=lambda id=student[0]: self.delete_student(id),
                   font=('Arial', 12)).grid(row=idx, column=2)











    def edit_student(self, student_id):
        cursor.execute("SELECT * FROM students WHERE ID=?", (student_id,))
        student = cursor.fetchone()

        self.edit_window = Toplevel(self.root)
        self.edit_window.title(f"Edit Student {student_id}")
        self.edit_window.geometry("400x300")

        Label(self.edit_window, text="First Name", font=('Arial', 12)).grid(row=0, column=0)
        Label(self.edit_window, text="Last Name", font=('Arial', 12)).grid(row=1, column=0)
        Label(self.edit_window, text="Grade", font=('Arial', 12)).grid(row=2, column=0)
        Label(self.edit_window, text="Status", font=('Arial', 12)).grid(row=3, column=0)

        self.edit_fname_entry = Entry(self.edit_window, font=('Arial', 12))
        self.edit_fname_entry.grid(row=0, column=1)
        self.edit_fname_entry.insert(0, "Placeholder")

        self.edit_lname_entry = Entry(self.edit_window, font=('Arial', 12))
        self.edit_lname_entry.grid(row=1, column=1)
        self.edit_lname_entry.insert(0, "Placeholder")

        self.edit_grade_entry = Entry(self.edit_window, font=('Arial', 12))
        self.edit_grade_entry.grid(row=2, column=1)
        self.edit_grade_entry.insert(0, "Placeholder")

        self.edit_status_entry = Entry(self.edit_window, font=('Arial', 12))
        self.edit_status_entry.grid(row=3, column=1)
        self.edit_status_entry.insert(0, "Placeholder")

        Button(self.edit_window, text="Save Changes", command=lambda: self.save_changes(student_id),
               font=('Arial', 12)).grid(row=4, column=1, pady=10)












    def save_changes(self, student_id):
        fname = self.edit_fname_entry.get()
        lname = self.edit_lname_entry.get()
        grade = self.edit_grade_entry.get()
        status = self.edit_status_entry.get()

        if fname and lname and grade and status:
            cursor.execute('''UPDATE students SET FNAME=?, LNAME=?, GRADE=?, STATUS=? WHERE ID = ?''', (fname, lname, grade, status , student_id))
            conn.commit()
            messagebox.showinfo("Success", "Changes saved successfully")
            self.edit_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")










    def delete_student(self, student_id):
        cursor.execute('''DELETE FROM students WHERE ID = ?''', (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully")
        self.view_students()








    def clear_entries(self):
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.grade_entry.delete(0, END)
        self.status_entry.delete(0, END)


















if __name__ == '__main__':
    root = Tk()
    app = Students_Manager(root)
    root.mainloop()
