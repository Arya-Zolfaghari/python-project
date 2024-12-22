import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from datetime import datetime
import jdatetime
import json
import os
import shutil




class Project_Manager_App:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Manager")
        self.data_file = "projects.json"
        self.users = self.load_data()
        self.current_user = None

        self.show_login_screen()







    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}





    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.users, file, indent=4, ensure_ascii=False, default=str)







    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=50)

        tk.Label(login_frame, text="Are you a Teacher or a Student?").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(login_frame, text="Teacher", command=self.teacher_login).grid(row=1, column=0, padx=10)
        tk.Button(login_frame, text="Student", command=self.student_login).grid(row=1, column=1, padx=10)








    def teacher_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        teacher_frame = tk.Frame(self.root)
        teacher_frame.pack(pady=50)

        tk.Label(teacher_frame, text="Enter Password:").pack(pady=5)
        self.password_entry = tk.Entry(teacher_frame, show="*", width=20)
        self.password_entry.pack(pady=5)

        tk.Button(teacher_frame, text="Login", command=self.verify_teacher).pack(pady=10)






    def verify_teacher(self):
        password = self.password_entry.get()
        if password == "123456":
            self.current_user = "teacher"
            self.show_teacher_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect password!")
            self.show_login_screen()






    def student_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        student_frame = tk.Frame(self.root)
        student_frame.pack(pady=50)

        tk.Label(student_frame, text="Enter your Name:").pack(pady=5)
        self.name_entry = tk.Entry(student_frame, width=20)
        self.name_entry.pack(pady=5)

        tk.Button(student_frame, text="Login", command=self.verify_student).pack(pady=10)





    def verify_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name!")
            return

        self.current_user = name
        if name not in self.users:
            self.users[name] = {"projects": []}

        self.show_student_dashboard()








    def show_teacher_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Teacher Dashboard").pack(pady=10)
        self.project_list = tk.Listbox(self.root, width=80, height=15)
        self.project_list.pack(pady=10)

        for user, data in self.users.items():
            for project in data["projects"]:
                upload_time = project.get("upload_time", "N/A")
                self.project_list.insert(
                    tk.END,
                    f"{user}: {project['name']} - Due: {project['due_date']} - Upload: {upload_time} - Grade: {project.get('grade', 'Not Graded')}"
                )

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Download File", command=self.download_file).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Grade Project", command=self.grade_project).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Logout", command=self.show_login_screen).grid(row=0, column=2, padx=10)








    def download_file(self):
        selected = self.project_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a project to download!")
            return

        index = selected[0]
        user_project = self.project_list.get(index)
        user, project_name = user_project.split(":")[0], user_project.split(":")[1].split("-")[0].strip()

        for project in self.users[user]["projects"]:
            if project["name"] == project_name:
                file_path = project.get("file_path")
                if not file_path or not os.path.exists(file_path):
                    messagebox.showerror("File Error", "File not found!")
                    return
                save_path = filedialog.asksaveasfilename(
                    initialfile=os.path.basename(file_path),
                    title="Save File As"
                )
                if save_path:
                    shutil.copy(file_path, save_path)
                    messagebox.showinfo("Success", "File downloaded successfully!")
                return









    def grade_project(self):
        selected = self.project_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a project to grade!")
            return

        index = selected[0]
        user_project = self.project_list.get(index)
        user, project_name = user_project.split(":")[0], user_project.split(":")[1].split("-")[0].strip()

        grade = simpledialog.askstring("Grade Project", "Enter Grade (0-100):")
        if not grade or not grade.isdigit() or not (0 <= int(grade) <= 100):
            messagebox.showerror("Invalid Grade", "Please enter a valid grade between 0 and 100.")
            return

        for project in self.users[user]["projects"]:
            if project["name"] == project_name:
                project["grade"] = int(grade)
                break

        self.save_data()
        self.show_teacher_dashboard()






    def show_student_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Welcome, {self.current_user}!").pack(pady=10)

        self.project_list = tk.Listbox(self.root, width=80, height=15)
        self.project_list.pack(pady=10)

        self.update_student_projects()

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Project Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=20)
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(input_frame, text="Upload Project", command=self.upload_project).grid(row=2, column=0, columnspan=2, pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Logout", command=self.show_login_screen).pack(pady=10)








    def update_student_projects(self):
        self.project_list.delete(0, tk.END)
        for project in self.users[self.current_user]["projects"]:
            self.project_list.insert(
                tk.END,
                f"{project['name']} - Due: {project['due_date']} - Upload: {project.get('upload_time', 'N/A')} - Grade: {project.get('grade', 'Not Graded')}"
            )








    def upload_project(self):
        name = self.name_entry.get().strip()
        due_date = self.date_entry.get().strip()

        if not name or not due_date:
            messagebox.showwarning("Input Error", "Please enter both project name and due date!")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        file_path = filedialog.askopenfilename(title="Select Project File")
        if not file_path:
            messagebox.showwarning("File Error", "No file selected!")
            return

        upload_time = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.users[self.current_user]["projects"].append({
            "name": name,
            "due_date": due_date,
            "file_path": file_path,
            "upload_time": upload_time,
        })

        self.save_data()
        self.update_student_projects()














if __name__ == "__main__":
    root = tk.Tk()
    app = Project_Manager_App(root)
    root.mainloop()
