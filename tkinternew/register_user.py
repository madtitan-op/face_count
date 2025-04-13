import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import re  # For email validation
from datetime import datetime
import requests  # Add this import for HTTP requests
from login import get_token  # Assuming you have a function to get the token
from Face import Face
import shutil

from face_encode import encodings


# from face_data.face_encode import encodings

class ModernEntry(tk.Frame):
    def __init__(self, parent, placeholder="", show=None):
        super().__init__(parent, bg="#ffffff")
        
        self.placeholder = placeholder  # Store placeholder text
        self.entry = tk.Entry(self,
                            font=("Helvetica", 11),
                            bg="#ffffff",
                            fg="#333333",
                            bd=1,
                            relief=tk.SOLID,
                            show=show)
        self.entry.pack(fill=tk.X, ipady=8)
        
        # Configure border color
        self.entry.configure(highlightthickness=1,
                           highlightbackground="#e0e0e0",
                           highlightcolor="#4CAF50")
        
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(fg="#999999")
            
            def on_focus_in(e):
                if self.entry.get() == self.placeholder:
                    self.entry.delete(0, tk.END)
                    self.entry.config(fg="#333333")
                    
            def on_focus_out(e):
                if not self.entry.get():
                    self.entry.insert(0, self.placeholder)
                    self.entry.config(fg="#999999")
                    
            self.entry.bind("<FocusIn>", on_focus_in)
            self.entry.bind("<FocusOut>", on_focus_out)
    
    def get_value(self):
        """Get the actual value, returning empty string if it's just placeholder"""
        value = self.entry.get()
        if value == self.placeholder:
            return ""
        return value

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_id(user_id):
    """Validate user ID format"""
    if not user_id:
        return False, "User ID is required!"
    if not user_id.isdigit():
        return False, "User ID must contain only numbers!"
    if len(user_id) != 11:
        return False, "User ID must be 11 digits!"
    return True, ""

def validate_name(name):
    """Validate full name"""
    if not name:
        return False, "Full name is required!"
    if len(name) < 3:
        return False, "Name must be at least 3 characters long!"
    if not all(x.isalpha() or x.isspace() for x in name):
        return False, "Name can only contain letters and spaces!"
    return True, ""

def validate_department(dept):
    """Validate department selection"""
    if dept == "Select Department":
        return False, "Please select a department!"
    return True, ""

def validate_year(year):
    """Validate year of passing"""
    if year == "Select Year":
        return False, "Please select year of passing!"
    return True, ""

def validate_password(password, confirm_password):
    """Validate password"""
    if not password:
        return False, "Password is required!"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long!"
    if password != confirm_password:
        return False, "Passwords do not match!"
    return True, ""

def validate_photo(photo_path):
    """Validate photo selection"""
    if not photo_path:
        return False, "Please select a photo!"
    return True, ""

def handle_photo_upload(photo_label):
    """Handle photo upload functionality"""
    # Directory where images should be stored
    image_dir = "user_photos"
    
    # Create directory if it doesn't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # Define allowed file types
    file_types = [('Image files', '*.png *.jpg *.jpeg *.gif *.bmp')]
    
    # Open file dialog to select photo
    file_path = filedialog.askopenfilename(filetypes=file_types)
    
    if file_path:
        try:
            # Get just the filename from the full path
            filename = os.path.basename(file_path)
            
            # Create destination path
            dest_path = os.path.join(image_dir, filename)
            
            # Copy the file to the directory
            shutil.copy2(file_path, dest_path)
            
            # Update the label with just the filename
            photo_label.config(text=filename)
            
            # Return just the filename
            return filename
            
        except Exception as e:
            # Show error message if something goes wrong
            messagebox.showerror("Error", f"Failed to save photo: {str(e)}")
            return None
            
    return None
def validate_all_inputs(user_data, photo_path, confirm_pwd):
    """Validate all inputs before submission"""
    # Validate User ID
    valid, message = validate_user_id(user_data['userid'])
    if not valid:
        return False, message
        
    # Validate Name
    valid, message = validate_name(user_data['name'])
    if not valid:
        return False, message
        
    # Validate Department
    valid, message = validate_department(user_data['department'])
    if not valid:
        return False, message
        
    # Validate Year
    valid, message = validate_year(str(user_data['yop']))
    if not valid:
        return False, message
        
    # Validate Email
    if not validate_email(user_data['email']):
        return False, "Please enter a valid email address!"
        
    # Validate Password
    valid, message = validate_password(user_data['password'], confirm_pwd)
    if not valid:
        return False, message
        
    # Validate Photo
    valid, message = validate_photo(photo_path)
    if not valid:
        return False, message
        
    return True, ""

def create_register_window(parent):
    register_window = tk.Toplevel(parent)
    register_window.title("Create New Account")
    register_window.geometry("1000x700")  # Wider window for two-column layout
    register_window.configure(bg="#ffffff")
    
    # Enable minimize and maximize buttons
    register_window.resizable(True, True)
    register_window.minsize(1000, 700)
    
    # Make the window modal
    register_window.transient(parent)
    register_window.grab_set()
    
    # Main container with two columns
    main_container = tk.Frame(register_window, bg="#ffffff")
    main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
    
    # Left column - Form
    form_column = tk.Frame(main_container, bg="#ffffff")
    form_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Welcome text
    tk.Label(form_column,
            text="Welcome",
            font=("Helvetica", 32, "bold"),
            fg="#4CAF50",
            bg="#ffffff").pack(anchor=tk.W)
            
    tk.Label(form_column,
            text="Register new account",
            font=("Helvetica", 14),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 30))
    
    # Form frame
    form_frame = tk.Frame(form_column, bg="#ffffff")
    form_frame.pack(fill=tk.X, pady=10)
    
    # User ID and Name row
    id_name_frame = tk.Frame(form_frame, bg="#ffffff")
    id_name_frame.pack(fill=tk.X, pady=(0, 15))
    
    # User ID
    userid_frame = tk.Frame(id_name_frame, bg="#ffffff")
    userid_frame.pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(userid_frame,
            text="User ID",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
    userid = ModernEntry(userid_frame, "")
    userid.pack()
    
    # Name
    name_frame = tk.Frame(id_name_frame, bg="#ffffff")
    name_frame.pack(side=tk.LEFT)
    tk.Label(name_frame,
            text="Full Name",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
    name = ModernEntry(name_frame, "")
    name.pack()
    
    # Department and YOP row
    dept_yop_frame = tk.Frame(form_frame, bg="#ffffff")
    dept_yop_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Department
    dept_frame = tk.Frame(dept_yop_frame, bg="#ffffff")
    dept_frame.pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(dept_frame,
            text="Department",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
    
    departments = ['CE', 'CSE', 'IT', 'ECE', 'EE', 'ME']
    department_var = tk.StringVar(value='Select Department')
    department_menu = ttk.Combobox(dept_frame, 
                                 textvariable=department_var,
                                 values=departments,
                                 width=23,
                                 state='readonly')
    department_menu.pack()
    
    # Year of Passing
    yop_frame = tk.Frame(dept_yop_frame, bg="#ffffff")
    yop_frame.pack(side=tk.LEFT)
    tk.Label(yop_frame,
            text="Year of Passing",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
    
    current_year = datetime.now().year
    years = list(range(current_year, current_year + 6))
    yop_var = tk.StringVar(value='Select Year')
    yop_menu = ttk.Combobox(yop_frame,
                           textvariable=yop_var,
                           values=years,
                           width=23,
                           state='readonly')
    yop_menu.pack()
    
    # Email
    email_frame = tk.Frame(form_frame, bg="#ffffff")
    email_frame.pack(fill=tk.X, pady=(0, 15))
    tk.Label(email_frame,
            text="Email Account",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
    email = ModernEntry(email_frame, "")
    email.pack(fill=tk.X)
    
    # Password fields row
    passwords_frame = tk.Frame(form_frame, bg="#ffffff")
    passwords_frame.pack(fill=tk.X, pady=(0, 25))
    
    # Password
    password_frame = tk.Frame(passwords_frame, bg="#ffffff")
    password_frame.pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(password_frame,
            text="Password",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
    password = ModernEntry(password_frame, "", show="●")
    password.pack()
    
    # Confirm Password
    confirm_frame = tk.Frame(passwords_frame, bg="#ffffff")
    confirm_frame.pack(side=tk.LEFT)
    tk.Label(confirm_frame,
            text="Confirm Password",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
    confirm_password = ModernEntry(confirm_frame, "", show="●")
    confirm_password.pack()
    
    # Photo upload section
    photo_frame = tk.Frame(form_frame, bg="#ffffff")
    photo_frame.pack(fill=tk.X, pady=(0, 15))
    tk.Label(photo_frame,
            text="Profile Photo",
            font=("Helvetica", 10),
            fg="#666666",
            bg="#ffffff").pack(side=tk.LEFT, pady=(0, 5))
    
    photo_label = tk.Label(photo_frame,
                          text="No photo selected",
                          font=("Helvetica", 10),
                          fg="#666666",
                          bg="#ffffff")
    photo_label.pack(side=tk.LEFT, padx=(10, 10))
    
    photo_path = [None]  # Using list to store path as a mutable object
    
    def choose_photo():
        photo_path[0] = handle_photo_upload(photo_label)
            
    photo_btn = tk.Button(photo_frame,
                         text="Choose Photo",
                         font=("Helvetica", 10),
                         bg="#4CAF50",
                         fg="white",
                         bd=0,
                         padx=15,
                         pady=5,
                         cursor="hand2",
                         command=choose_photo)
    photo_btn.pack(side=tk.LEFT)
    
    # Error label for displaying validation messages
    error_label = tk.Label(form_frame,
                          text="",
                          font=("Helvetica", 10),
                          fg="#FF4444",
                          bg="#ffffff")
    error_label.pack(pady=(0, 10))

    def send_user_data_to_server(user_data, photo_path):
        """
        Send user data to server via HTTP POST request
        """
        try:
            # Prepare the data for the server
            server_data = {
                'userid': user_data['userid'],
                'name': user_data['name'],
                'yop': user_data['yop'],
                'department': user_data['department'],
                'email': user_data['email'],
                'password': user_data['password'],
                'role': 'STUDENT'
            }
            
            # Convert photo to base64 if needed
            if photo_path:
              filename = os.path.basename(photo_path)
              server_data['photo'] = filename  # Send only filename instead of full path 
            
            # Correct server URL format with http:// prefix
            server_url = "http://localhost:8080/api/users/register"
            bearer_token = get_token()

            # Send POST request to server with proper headers and timeout
            response = requests.post(
                server_url,
                json=server_data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {bearer_token}'
                }
                # timeout=10  # 10 seconds timeout
            )
            
            # Check response status
            if response.status_code == 200:
                return True, "Data successfully sent to server"
            else:
                return False, f"Server error: {response.status_code} - {response.text}"
            
        except requests.exceptions.ConnectionError:
            return False, "Connection failed: Please check if the server is running at localhost:8080"
        except requests.exceptions.Timeout:
            return False, "Request timed out: Server took too long to respond"
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"Error sending data to server: {str(e)}"

    def submit_to_server():
         
        try:
            # Get values with error checking
            user_data = {
                'userid': userid.get_value().strip(),
                'name': name.get_value().strip(),
                'department': department_var.get(),
                'yop': yop_var.get(),
                'email': email.get_value().strip(),
                'password': password.get_value()
            }
            
            # Debug print
            
            
            # Check for empty fields
            for key, value in user_data.items():
                if not value or value in ['Select Department', 'Select Year']:
                    error_label.config(text=f"{key.capitalize()} is required!")
                
                    return
            
            # Validate all inputs
            valid, message = validate_all_inputs(user_data, photo_path[0], confirm_password.get_value())
            if not valid:
                error_label.config(text=message)
                return
            
            # Send data to server
            server_success, server_message = send_user_data_to_server(user_data, photo_path[0])
            encodings.face_encoding(photo_path[0], user_data['name'], user_data['userid'])
            # Face.encode(photo_path[0], user_data['name'], user_data['userid'])
            
            if server_success:
                messagebox.showinfo("Success", "Account created successfully!")
                register_window.destroy()
            else:
                error_label.config(text=server_message)
            
        except Exception as e:
            error_msg = f"Error during submission: {str(e)}"
            print(error_msg)  # Debug print
            error_label.config(text=error_msg)

    # Submit button with modern style
    submit_btn = tk.Button(form_frame,
                          text="SUBMIT",
                          font=("Helvetica", 12, "bold"),
                          bg="#4CAF50",
                          fg="white",
                          padx=30,
                          pady=12,
                          bd=0,
                          cursor="hand2",
                          relief=tk.FLAT,
                          command=submit_to_server)
    submit_btn.pack(pady=20)
    
    def on_submit_hover(e):
        submit_btn['bg'] = '#45a049'
    
    def on_submit_leave(e):
        submit_btn['bg'] = '#4CAF50'
    
    submit_btn.bind('<Enter>', on_submit_hover)
    submit_btn.bind('<Leave>', on_submit_leave)
    
    # Right column - Illustration
    illustration_column = tk.Frame(main_container, bg="#ffffff", width=400)
    illustration_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(40, 0))
    
    # Load and display the illustration image
    try:
        # Load the image
        illustration_image = tk.PhotoImage(file="2.png")
        
        # Calculate scaling to fit the frame while maintaining aspect ratio
        img_width = illustration_image.width()
        img_height = illustration_image.height()
        frame_width = 400
        frame_height = 600
        
        # Calculate scaling factor
        width_ratio = frame_width / img_width
        height_ratio = frame_height / img_height
        scale_factor = min(width_ratio, height_ratio)
        
        # Scale the image
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        illustration_image = illustration_image.subsample(
            max(1, int(img_width / new_width)),
            max(1, int(img_height / new_height))
        )
        
        # Create and pack the image label
        illustration_label = tk.Label(
            illustration_column,
            image=illustration_image,
            bg="#ffffff"
        )
        illustration_label.image = illustration_image  # Keep a reference!
        illustration_label.pack(expand=True, pady=20)
        
    except Exception as e:
        print(f"Error loading illustration: {e}")
        # Fallback - show empty frame
        pass
    
    def on_closing():
        register_window.grab_release()
        register_window.destroy()
    
    register_window.protocol("WM_DELETE_WINDOW", on_closing)
    
    return register_window 