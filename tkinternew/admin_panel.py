import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from register_user import create_register_window

def create_button(parent, text, color_code, command=None):
    bg_color = color_code
    # Create slightly darker hover color
    r = int(color_code[1:3], 16)
    g = int(color_code[3:5], 16)
    b = int(color_code[5:7], 16)
    hover_color = f'#{max(0, r-30):02x}{max(0, g-30):02x}{max(0, b-30):02x}'
        
    btn = tk.Button(parent,
                   text=text,
                   font=("Helvetica", 12, "bold"),
                   bg=bg_color,
                   fg="white",
                   bd=1,
                   width=18,
                   pady=12,
                   padx=20,
                   cursor="hand2",
                   relief="flat",
                   command=command)
    
    def on_enter(e):
        btn['bg'] = hover_color
            
    def on_leave(e):
        btn['bg'] = bg_color
        
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    return btn

def create_admin_panel(main_window):
    admin_window = tk.Toplevel(main_window)
    admin_window.title("Admin Panel")
    admin_window.geometry("1400x800")
    admin_window.configure(bg="#E6F9F9")  # Light turquoise background
    
    # Enable minimize and maximize buttons
    admin_window.resizable(True, True)
    admin_window.minsize(1300, 800)  # Set minimum window size
    
    # Make the admin window modal but allow minimize/maximize
    admin_window.transient(main_window)
    admin_window.grab_set()
    
    def register_user():
        create_register_window(admin_window)

    def manual_attendance():
        messagebox.showinfo("Manual Attendance", "Manual Attendance functionality will be implemented here")

    def delete_user():
        messagebox.showinfo("Delete User", "Delete User functionality will be implemented here")

    def get_attendance_record():
        messagebox.showinfo("Get Attendance Record", "Get Attendance Record functionality will be implemented here")

    def modify_user():
        messagebox.showinfo("Modify User", "Modify User functionality will be implemented here")
    
    # Main content area with curved white background
    main_frame = tk.Frame(admin_window, bg="white")
    main_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
    
    # Content area with dynamic resizing
    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
    
    # Left side content
    left_frame = tk.Frame(content_frame, bg="white")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    title = tk.Label(left_frame, 
                    text="Admin Panel", 
                    font=("Helvetica", 48, "bold"),
                    bg="white",
                    fg="#002B5B",
                    justify=tk.LEFT,
                    )
    title.pack(anchor=tk.W)
    
    description = tk.Label(left_frame,
                         text="Manage users and attendance records\nwith advanced admin controls",
                         font=("Helvetica", 18),
                         bg="white",
                         fg="#666666",
                         justify=tk.LEFT)
    description.pack(anchor=tk.W, pady=(20, 40))
    
    # Buttons with modern styling - arranged in pairs
    buttons_frame = tk.Frame(left_frame, bg="white")
    buttons_frame.pack(anchor=tk.W)
    
    # First row of buttons
    row1_frame = tk.Frame(buttons_frame, bg="white")
    row1_frame.pack(anchor=tk.W, pady=(0, 15))
    
    register_btn = create_button(row1_frame, "Register User", "#FF6B6B", register_user)  # Coral Red
    register_btn.pack(side=tk.LEFT, padx=(0, 15))
    
    manual_btn = create_button(row1_frame, "Manual Attendance", "#4ECDC4", manual_attendance)  # Turquoise
    manual_btn.pack(side=tk.LEFT)
    
    # Second row of buttons
    row2_frame = tk.Frame(buttons_frame, bg="white")
    row2_frame.pack(anchor=tk.W, pady=(0, 15))
    
    delete_btn = create_button(row2_frame, "Delete User", "#45B7D1", delete_user)  # Sky Blue
    delete_btn.pack(side=tk.LEFT, padx=(0, 15))
    
    record_btn = create_button(row2_frame, "Get Attendance Record", "#96CEB4", get_attendance_record)  # Sage Green
    record_btn.pack(side=tk.LEFT)
    
    # Last button centered
    row3_frame = tk.Frame(buttons_frame, bg="white")
    row3_frame.pack(anchor=tk.W)
    
    modify_btn = create_button(row3_frame, "Modify User", "#9B59B6", modify_user)  # Purple
    modify_btn.pack()
    
    # Right side illustration
    try:
        img = Image.open("adminimage.png")
        img = img.resize((600, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(content_frame, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(side=tk.RIGHT, padx=(50, 0))
    except:
        # Create a decorative wave shape instead
        wave_frame = tk.Frame(content_frame, bg="#00B4B4", width=500, height=500)
        wave_frame.pack(side=tk.RIGHT, padx=(50, 0))
        wave_frame.pack_propagate(False)
    
    # Handle window close
    def on_closing():
        admin_window.grab_release()
        admin_window.destroy()
    
    admin_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    return admin_window 