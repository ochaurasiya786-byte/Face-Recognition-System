from tkinter import *
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import sqlite3
import hashlib
import re
import os
import json

# PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "users.db")
SESSION_FILE = os.path.join(BASE_DIR, "session.json")

# DATABASE
def create_database():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            email TEXT NOT NULL,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# PASSWORD HASH
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# LOGIN / REGISTER
class Login_Register:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Attendance System - Login")
        self.root.resizable(False, False)
        self.root.configure(bg="#071426")
        create_database()
        self.start_app()

    # WINDOW CLEAR
    def clear_window(self):
        try:
            self.root.unbind("<Return>")
        except:
            pass
        for w in self.root.winfo_children():
            w.destroy()

    # SESSION MANAGEMENT
    def save_session(self, username):
        session_data = {"logged_in": True, "username": username}
        try:
            with open(SESSION_FILE, "w") as file:
                json.dump(session_data, file)
        except Exception as e:
            print("Session save error:", e)

    def get_session(self):
        if not os.path.exists(SESSION_FILE):
            return None
        try:
            with open(SESSION_FILE, "r") as file:
                session = json.load(file)
            username = session.get("username")
            if session.get("logged_in") and username:
                conn = sqlite3.connect(DB_NAME)
                cur = conn.cursor()
                cur.execute("SELECT username FROM users WHERE username=?", (username,))
                user = cur.fetchone()
                conn.close()
                if user:
                    return session
        except Exception as e:
            print("Session read error:", e)
        return None

    def clear_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except Exception as e:
                print("Session delete error:", e)

    def start_app(self):
        session = self.get_session()
        if session:
            self.open_main_system()
        else:
            self.show_login()

    # LOGIN PAGE
    def show_login(self):
        self.clear_window()
        self.root.title("Face Recognition Attendance System - Login")

        # HEADER
        header = Frame(self.root, bg="#dbeafe")
        header.place(x=0, y=0, width=1366, height=90)

        Label(header, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("Cambria", 29, "bold"), bg="#dbeafe", fg="#18385f").pack(pady=(17, 0))
        Label(header, text="Secure Login Portal", font=("Segoe UI", 10), bg="#dbeafe", fg="#4f6f95").pack()

        # LOGIN CARD
        card = Frame(self.root, bg="#0c1c31", bd=1, relief=SOLID, highlightbackground="#31577f", highlightthickness=1)
        card.place(x=493, y=145, width=380, height=485)

        # BLUE USER ICON
        icon_path = os.path.join(BASE_DIR, "College_images", "user.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path).convert("RGBA")
            pixels = img.load()
            for x in range(img.width):
                for y in range(img.height):
                    r, g, b, a = pixels[x, y]
                    if r > 150 and g < 100 and b < 120:
                        pixels[x, y] = (37, 99, 235, a)
            img = img.resize((55, 55), Image.Resampling.LANCZOS)
            self.user_icon = ImageTk.PhotoImage(img)
            Label(card, image=self.user_icon, bg="#0c1c31").pack(pady=(18, 0))
        else:
            Label(card, text="●", font=("Segoe UI", 42, "bold"), bg="#0c1c31", fg="#55c7ff").pack(pady=(20, 0))

        # LOGIN TITLE
        Label(card, text="WELCOME BACK", font=("Cambria", 22, "bold"), bg="#0c1c31", fg="white").pack()
        Label(card, text="Sign in to continue", font=("Segoe UI", 10), bg="#0c1c31", fg="#9db4cf").pack(pady=(2, 25))

        # USERNAME
        Label(card, text="Username", font=("Segoe UI", 10, "bold"), bg="#0c1c31", fg="white").place(x=40, y=145)
        self.login_username = Entry(card, font=("Segoe UI", 11), bd=0, relief=FLAT)
        self.login_username.place(x=40, y=175, width=300, height=36)

        # PASSWORD
        Label(card, text="Password", font=("Segoe UI", 10, "bold"), bg="#0c1c31", fg="white").place(x=40, y=225)
        self.login_password = Entry(card, font=("Segoe UI", 11), bd=0, relief=FLAT, show="*")
        self.login_password.place(x=40, y=255, width=300, height=36)

        # SHOW PASSWORD
        self.show_password_var = BooleanVar()
        Checkbutton(card, text="Show Password", variable=self.show_password_var, command=self.toggle_login_password, font=("Segoe UI", 9), bg="#0c1c31", fg="#9db4cf", activebackground="#0c1c31", activeforeground="white", selectcolor="#0c1c31").place(x=40, y=300)

        # LOGIN BUTTON
        Button(card, text="LOGIN", command=self.login, font=("Segoe UI", 11, "bold"), bg="#18385f", fg="white", activebackground="#245582", activeforeground="white", bd=0, cursor="hand2").place(x=40, y=340, width=300, height=42)

        # REGISTER BUTTON
        Button(card, text="New User Register", command=self.show_register, font=("Segoe UI", 9, "bold"), bg="#0c1c31", fg="#55c7ff", activebackground="#0c1c31", activeforeground="white", bd=0, cursor="hand2").place(x=40, y=395, width=145, height=25)

        # FORGOT PASSWORD
        Button(card, text="Forgot Password?", command=self.forgot_password, font=("Segoe UI", 9, "bold"), bg="#0c1c31", fg="#55c7ff", activebackground="#0c1c31", activeforeground="white", bd=0, cursor="hand2").place(x=195, y=395, width=145, height=25)

        # FOOTER
        Label(card, text="Secure • Smart • Reliable", font=("Segoe UI", 9, "bold"), bg="#0c1c31", fg="#66809c").place(x=40, y=440, width=300)

        self.login_username.focus()
        self.root.bind("<Return>", lambda e: self.login())

    # TOGGLE LOGIN PASSWORD
    def toggle_login_password(self):
        self.login_password.config(show="" if self.show_password_var.get() else "*")

    # LOGIN
    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter Username and Password.", parent=self.root)
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
        user = cur.fetchone()
        conn.close()

        if user:
            self.save_session(username)
            messagebox.showinfo("Login Successful", f"Welcome, {user[2]} {user[3]}!", parent=self.root)
            self.open_main_system()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password.", parent=self.root)

    # MAIN SYSTEM
    def open_main_system(self):
        self.clear_window()
        try:
            from main import Face_Recognition_System
            Face_Recognition_System(self.root, logout_callback=self.logout)
        except Exception as e:
            messagebox.showerror("System Error", f"Unable to open main system.\n\n{e}", parent=self.root)

    # LOGOUT
    def logout(self):
        answer = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root)
        if not answer:
            return

        self.clear_session()

        for window in self.root.winfo_children():
            if isinstance(window, Toplevel):
                window.destroy()

        self.show_login()

    # REGISTER PAGE
    def show_register(self):
        self.clear_window()
        self.root.title("Face Recognition Attendance System - Register")

        # HEADER
        header = Frame(self.root, bg="#dbeafe")
        header.place(x=0, y=0, width=1366, height=80)

        Label(header, text="CREATE YOUR ACCOUNT", font=("Cambria", 27, "bold"), bg="#dbeafe", fg="#18385f").pack(pady=(18, 0))

        # CARD
        card = Frame(self.root, bg="white", bd=1, relief=SOLID, highlightbackground="#31577f", highlightthickness=1)
        card.place(x=220, y=105, width=926, height=600)

        # LEFT SIDE
        left = Frame(card, bg="#071426")
        left.place(x=0, y=0, width=300, height=598)

        Label(left, text="REGISTER", font=("Cambria", 30, "bold"), bg="#071426", fg="#55c7ff").place(x=40, y=100, width=220)
        Label(left, text="YOUR ACCOUNT", font=("Cambria", 19, "bold"), bg="#071426", fg="white").place(x=40, y=150, width=220)
        Label(left, text="Face Recognition\nAttendance System", font=("Segoe UI", 15, "bold"), bg="#071426", fg="#9db4cf", justify=CENTER).place(x=35, y=240, width=230, height=65)
        Label(left, text="SECURE • SMART • RELIABLE", font=("Segoe UI", 9, "bold"), bg="#071426", fg="#55c7ff").place(x=35, y=350, width=230)

        # FORM
        form = Frame(card, bg="white")
        form.place(x=300, y=0, width=624, height=598)

        self.reg_username = self.create_entry(form, "Username", 30, 60)
        self.reg_first_name = self.create_entry(form, "First Name", 330, 60)
        self.reg_last_name = self.create_entry(form, "Last Name", 30, 135)
        self.reg_contact = self.create_entry(form, "Contact Number", 330, 135)
        self.reg_email = self.create_entry(form, "Email Address", 30, 210)

        # SECURITY QUESTION
        Label(form, text="Security Question", font=("Segoe UI", 10, "bold"), bg="white", fg="#222").place(x=330, y=210)
        self.security_question = StringVar(value="Select Question")

        ttk.Combobox(form, textvariable=self.security_question, state="readonly", font=("Segoe UI", 10), values=("Your Birth Place", "Your Pet Name", "Your Favourite Teacher", "Your Favourite Color")).place(x=330, y=235, width=260, height=32)

        self.reg_answer = self.create_entry(form, "Security Answer", 30, 285)
        self.reg_password = self.create_entry(form, "Password", 330, 285, True)
        self.reg_confirm = self.create_entry(form, "Confirm Password", 30, 360, True)

        # SHOW PASSWORD
        self.show_reg_password = BooleanVar()
        Checkbutton(form, text="Show Password", variable=self.show_reg_password, command=self.toggle_register_password, font=("Segoe UI", 9), bg="white", activebackground="white").place(x=330, y=360)

        # TERMS
        self.agree = IntVar()
        Checkbutton(form, text="I Agree to the Terms & Conditions", variable=self.agree, font=("Segoe UI", 9, "bold"), bg="white", activebackground="white").place(x=330, y=395)

        # REGISTER BUTTON
        Button(form, text="REGISTER NOW", command=self.register, font=("Segoe UI", 11, "bold"), bg="#d92323", fg="white", activebackground="#a91515", activeforeground="white", bd=0, cursor="hand2").place(x=30, y=440, width=260, height=42)

        # LOGIN NOW
        Button(form, text="LOGIN NOW", command=self.show_login, font=("Segoe UI", 11, "bold"), bg="#18385f", fg="white", activebackground="#245582", activeforeground="white", bd=0, cursor="hand2").place(x=330, y=440, width=260, height=42)

        self.reg_username.focus()

    # CREATE ENTRY
    def create_entry(self, parent, text, x, y, password=False):
        Label(parent, text=text, font=("Segoe UI", 10, "bold"), bg="white", fg="#222").place(x=x, y=y)
        entry = Entry(parent, font=("Segoe UI", 10), bd=1, relief=SOLID, show="*" if password else "")
        entry.place(x=x, y=y + 25, width=260, height=32)
        return entry

    # TOGGLE REGISTER PASSWORD
    def toggle_register_password(self):
        value = "" if self.show_reg_password.get() else "*"
        self.reg_password.config(show=value)
        self.reg_confirm.config(show=value)

    # REGISTER
    def register(self):
        username = self.reg_username.get().strip()
        first_name = self.reg_first_name.get().strip()
        last_name = self.reg_last_name.get().strip()
        contact = self.reg_contact.get().strip()
        email = self.reg_email.get().strip()
        question = self.security_question.get()
        answer = self.reg_answer.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        # REQUIRED FIELDS
        if not all([username, first_name, last_name, contact, email, answer, password, confirm]):
            messagebox.showerror("Validation Error", "Please fill all the required fields.", parent=self.root)
            return

        # USERNAME
        if not re.match(r"^[A-Za-z0-9_]{4,20}$", username):
            messagebox.showerror("Invalid Username", "Username must contain 4-20 characters.\nOnly letters, numbers and underscore are allowed.", parent=self.root)
            return

        # FIRST NAME
        if not re.match(r"^[A-Za-z ]+$", first_name):
            messagebox.showerror("Invalid First Name", "First Name should contain letters only.", parent=self.root)
            return

        # LAST NAME
        if not re.match(r"^[A-Za-z ]+$", last_name):
            messagebox.showerror("Invalid Last Name", "Last Name should contain letters only.", parent=self.root)
            return

        # CONTACT
        if not re.match(r"^[0-9]{10}$", contact):
            messagebox.showerror("Invalid Contact", "Contact number must contain exactly 10 digits.", parent=self.root)
            return

        # EMAIL
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.", parent=self.root)
            return

        # SECURITY QUESTION
        if question == "Select Question":
            messagebox.showerror("Validation Error", "Please select a security question.", parent=self.root)
            return

        # PASSWORD LENGTH
        if len(password) < 8:
            messagebox.showerror("Weak Password", "Password must contain at least 8 characters.", parent=self.root)
            return

        # UPPERCASE
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Weak Password", "Password must contain an uppercase letter.", parent=self.root)
            return

        # LOWERCASE
        if not re.search(r"[a-z]", password):
            messagebox.showerror("Weak Password", "Password must contain a lowercase letter.", parent=self.root)
            return

        # NUMBER
        if not re.search(r"[0-9]", password):
            messagebox.showerror("Weak Password", "Password must contain a number.", parent=self.root)
            return

        # CONFIRM PASSWORD
        if password != confirm:
            messagebox.showerror("Password Error", "Password and Confirm Password do not match.", parent=self.root)
            return

        # TERMS
        if self.agree.get() != 1:
            messagebox.showerror("Terms & Conditions", "Please accept the Terms & Conditions.", parent=self.root)
            return

        # DATABASE INSERT
        try:
            conn = sqlite3.connect(DB_NAME)
            conn.execute("""
                INSERT INTO users(
                    username,
                    first_name,
                    last_name,
                    contact,
                    email,
                    security_question,
                    security_answer,
                    password
                )
                VALUES(?,?,?,?,?,?,?,?)
            """, (username, first_name, last_name, contact, email, question, answer, hash_password(password)))
            conn.commit()
            conn.close()

            messagebox.showinfo("Registration Successful", "Your account has been created successfully!", parent=self.root)
            self.show_login()

        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Error", "Username already exists.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Database Error", f"Something went wrong.\n\n{e}", parent=self.root)

    # FORGOT PASSWORD
    def forgot_password(self):
        username = self.login_username.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter your username first.", parent=self.root)
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT security_question,security_answer FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Error", "Username not found.", parent=self.root)
            return

        answer = simpledialog.askstring("Security Verification", user[0], parent=self.root)

        if answer is None:
            return

        if answer.lower().strip() != user[1].lower().strip():
            messagebox.showerror("Verification Failed", "Incorrect security answer.", parent=self.root)
            return

        messagebox.showinfo("Password Recovery", "Security verification successful.", parent=self.root)

# START
if __name__ == "__main__":
    root = Tk()
    app = Login_Register(root)
    root.mainloop()

