import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def create_login_window():
    # Functions
    def on_login():
        selected_dept = department_var.get()
        selected_year = year_var.get()
        roll_no = roll_no_entry.get()

        # Check if any of the fields are empty
        if selected_dept == "Select Department" or selected_year == "Select Year" or not roll_no:
            messagebox.showerror("Error", "Please fill all fields!")
        else:
            # If all fields are filled, show success message and close the window
            messagebox.showinfo("Success", "Login successful!")
            print(f"Department: {selected_dept}")
            print(f"Year: {selected_year}")
            print(f"Roll No: {roll_no}")

            root.destroy()


    def on_enter(e):
        login_button.config(style="Hover.TButton")

    def on_leave(e):
        login_button.config(style="TButton")

    # Create main window
    root = tk.Tk()
    root.title("Student Login")
    root.geometry("500x650")
    root.configure(bg="#1E252F")
    root.resizable(False, False)

    # Frame for login box
    frame = tk.Frame(root, bg="#2C343F", padx=20, pady=20, relief="ridge", bd=5)
    frame.pack(pady=30)

    # Icon (lock symbol)
    icon_label = tk.Label(frame, text="🔒", font=("Times New Roman", 30), bg="#2C343F", fg="white")
    icon_label.pack()

    # Title Label
    title_label = tk.Label(frame, text="Student Login", font=("Times New Roman", 18, "bold"), bg="#2C343F", fg="white")
    title_label.pack(pady=10)

    # Department (Dropdown)
    department_label = tk.Label(frame, text="Department", font=("Times New Roman", 10, "bold"), bg="#2C343F", fg="white")
    department_label.pack(anchor="w", pady=2)

    department_var = tk.StringVar()
    department_dropdown = ttk.Combobox(frame, textvariable=department_var, width=28, font=("Times New Roman", 12))
    department_dropdown['values'] = ("Select Department", "Mechanical", "Civil", "Electrical", "Electronics", "Computer Science")
    department_dropdown.set("Select Department")  # Default text
    department_dropdown.pack(pady=5, ipady=3)

    # Passing Year (Dropdown)
    year_label = tk.Label(frame, text="Passing Year", font=("Times New Roman", 10, "bold"), bg="#2C343F", fg="white")
    year_label.pack(anchor="w", pady=2)

    year_var = tk.StringVar()
    year_dropdown = ttk.Combobox(frame, textvariable=year_var, width=28, font=("Times New Roman", 12))
    year_dropdown['values'] = ("Select Year", "2024", "2025", "2026", "2027", "2028", "2029")
    year_dropdown.set("Select Year")  # Default text
    year_dropdown.pack(pady=5, ipady=3)

    # Roll No Entry
    roll_no_label = tk.Label(frame, text="Roll No", font=("Times New Roman", 10, "bold"), bg="#2C343F", fg="white")
    roll_no_label.pack(anchor="w", pady=2)

    roll_no_entry = ttk.Entry(frame, width=30, font=("Times New Roman", 12))
    roll_no_entry.pack(pady=5, ipady=5)

    # Login Button with hover effect
    login_button = ttk.Button(frame, text="Login", command=on_login, style="TButton")
    login_button.pack(pady=10, ipadx=5, ipady=3)

    # Hover effects
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)



    # Horizontal separator
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x', padx=20, pady=10)

    # Progress bar
    progress = ttk.Progressbar(root, length=300, mode='determinate', style="Custom.Horizontal.TProgressbar")
    progress.pack(pady=10)
    progress.start(10)

    # Style Configuration
    style = ttk.Style()
    style.configure("TButton", font=("Times New Roman", 12, "bold"), background="#1DB954", foreground="white", padding=6)
    style.configure("Hover.TButton", font=("Times New Roman", 12, "bold"), background="black", foreground="black", padding=6)
    style.configure("Custom.Horizontal.TProgressbar", troughcolor="#2C343F", background="#1DB954", thickness=5)

    # Run main loop
    root.mainloop()

# Run the function to create the login window
if __name__ == "__main__":
    create_login_window()
