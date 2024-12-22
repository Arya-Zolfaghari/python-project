import tkinter as tk

entry = ""

def show_value(value):
    global entry
    entry += value
    display_entry.delete(0, tk.END)
    display_entry.insert(tk.END, entry)
    # display_entry.config(text=entry)

def clear_entry():
    global entry
    entry = ""
    display_entry.delete(0, tk.END)

    # display_entry.config(text=entry)

def calculate():
    global entry
    result = "" 
    if entry != "":
        result = eval(entry)
        display_entry.delete(0, tk.END)
        display_entry.insert(tk.END, str(result))
        entry = str(result)
    else:
        display_entry.delete(0, tk.END)
        display_entry.insert(tk.END, "error")

    #     result = "error"
    # display_entry.config(text=result)

# mona = '2+4-3*4'

root = tk.Tk()
root.title("Calculator")
root.iconbitmap(r"C:\Users\Arya\OneDrive\Dokumente\python\image\calculate.ico")

label1 = tk.Label(text="Standard", font=("Arial", 20, "bold"))
label1.grid(row=0, columnspan=4)

display_entry = tk.Entry(root,
                         font=("Arial", 20, "bold"),
                         border=2, background="lightblue", foreground="black",
                         justify="right"
                         )
display_entry.grid(row=1, columnspan=4)

btn7 = tk.Button(text="7", font=("Arial", 18), width=4, command=lambda: show_value("7"))
btn7.grid(row=2, column=0)
btn8 = tk.Button(text="8", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("8"))
btn8.grid(row=2, column=1)
btn9 = tk.Button(text="9", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("9"))
btn9.grid(row=2, column=2)
btn_plus = tk.Button(text="+", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("+"))
btn_plus.grid(row=2, column=3)
btn4 = tk.Button(text="4", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("4"))
btn4.grid(row=3, column=0)
btn5 = tk.Button(text="5", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("5"))
btn5.grid(row=3, column=1)
btn6 = tk.Button(text="6", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("6"))
btn6.grid(row=3, column=2)
btn_minus = tk.Button(text="-", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("-"))
btn_minus.grid(row=3, column=3)
btn1 = tk.Button(text="1", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("1"))
btn1.grid(row=4, column=0)
btn2 = tk.Button(text="2", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("2"))
btn2.grid(row=4, column=1)
btn3 = tk.Button(text="3", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("3"))
btn3.grid(row=4, column=2)
btn_zarb = tk.Button(text="x", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("*"))
btn_zarb.grid(row=4, column=3)
btn_c = tk.Button(text="c", font=("Arial", 18, "bold"), width=4, command=clear_entry)
btn_c.grid(row=5, column=0)
btn0 = tk.Button(text="0", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("0"))
btn0.grid(row=5, column=1)
btn_mosavi = tk.Button(text="=", font=("Arial", 18, "bold"), width=4, command=calculate)
btn_mosavi.grid(row=5, column=2)
btn_taghsim = tk.Button(text="/", font=("Arial", 18, "bold"), width=4, command=lambda: show_value("/"))
btn_taghsim.grid(row=5, column=3)

root.mainloop()




