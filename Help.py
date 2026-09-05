from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import smtplib
from email.message import EmailMessage


class Help:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")
        self.root.resizable(False, False)

        # ================= GMAIL SETTINGS =================
        self.sender_email = "ochaurasiya786@gmail.com"
        self.app_password = "yhmi lvak gbyy wgkl"
        self.receiver_email = "ochaurasiya786@gmail.com"

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # ================= BACKGROUND =================
        img = Image.open(os.path.join(base_dir, "College_images", "helpdesk2.png"))
        img = img.resize((1366, 690), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        Label(root, image=self.photoimg, bd=0).place(x=0, y=40, width=1366, height=690)

        # ================= EMAIL BOX =================
        email_box = Canvas(root, width=330, height=52, bg="#061a35", highlightthickness=0, bd=0, cursor="hand2")
        email_box.place(x=55, y=440)

        # ================= EMAIL BORDER =================
        email_box.create_arc(2, 2, 27, 50, start=90, extent=180, outline="#00aaff", width=2, tags="border_arc")
        email_box.create_arc(303, 2, 328, 50, start=270, extent=180, outline="#00aaff", width=2, tags="border_arc")
        email_box.create_line(14, 2, 316, 2, fill="#00aaff", width=2, tags="border_line")
        email_box.create_line(14, 50, 316, 50, fill="#00aaff", width=2, tags="border_line")

        # ================= EMAIL ICON =================
        email_box.create_oval(10, 8, 48, 46, fill="#0875d1", outline="#00c8ff", width=2, tags="circle")
        email_box.create_rectangle(19, 19, 39, 35, outline="white", width=2)
        email_box.create_line(19, 19, 29, 28, 39, 19, fill="white", width=2)

        # ================= EMAIL LABEL =================
        email_box.create_text(60, 27, text="Email :", anchor="w", font=("Segoe UI", 11, "bold"), fill="white")
        email_box.create_text(108, 27, text="ochaurasiya786@gmail.com", anchor="w", font=("Segoe UI", 11, "bold"), fill="#00c8ff", tags="email")

        # ================= EMAIL EVENTS =================
        email_box.bind("<Button-1>", self.email_support)
        email_box.bind("<Enter>", self.email_hover)
        email_box.bind("<Leave>", self.email_leave)

        # ================= HELP BUTTONS =================
        button_y = 599
        button_height = 45
        gap = 8
        button_width = (1366 - (gap * 5)) // 6

        Button(root, text="FAQ", command=self.faq, font=("Segoe UI", 12, "bold"), bg="#123b68", fg="white", activebackground="#1d5b91", activeforeground="white", bd=0, cursor="hand2").place(x=0, y=button_y, width=button_width, height=button_height)

        Button(root, text="Email Support", command=self.email_support, font=("Segoe UI", 12, "bold"), bg="#123b68", fg="white", activebackground="#1d5b91", activeforeground="white", bd=0, cursor="hand2").place(x=button_width + gap, y=button_y, width=button_width, height=button_height)

        Button(root, text="Raise Complaint", command=self.complaint, font=("Segoe UI", 12, "bold"), bg="#123b68", fg="white", activebackground="#1d5b91", activeforeground="white", bd=0, cursor="hand2").place(x=(button_width + gap) * 2, y=button_y, width=button_width, height=button_height)

        Button(root, text="Contact Admin", command=self.contact_admin, font=("Segoe UI", 12, "bold"), bg="#123b68", fg="white", activebackground="#1d5b91", activeforeground="white", bd=0, cursor="hand2").place(x=(button_width + gap) * 3, y=button_y, width=button_width, height=button_height)

        Button(root, text="Face Recognition Help", command=self.face_help, font=("Segoe UI", 12, "bold"), bg="#123b68", fg="white", activebackground="#1d5b91", activeforeground="white", bd=0, cursor="hand2").place(x=(button_width + gap) * 4, y=button_y, width=button_width, height=button_height)

        Button(root, text="Attendance Help", command=self.attendance_help, font=("Segoe UI", 12, "bold"), bg="#123b68", fg="white", activebackground="#1d5b91", activeforeground="white", bd=0, cursor="hand2").place(x=(button_width + gap) * 5, y=button_y, width=button_width, height=button_height)

    # ================= SEND EMAIL =================
    def send_email(self, subject, body):
        try:
            if self.app_password == "PASTE_YOUR_APP_PASSWORD_HERE":
                messagebox.showwarning("App Password Required", "Please paste your Gmail App Password in Help.py.")
                return False

            msg = EmailMessage()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            msg["Subject"] = subject
            msg.set_content(body)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            return True

        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Gmail Login Error", "Gmail authentication failed.\n\nPlease check your Gmail App Password.")
            return False

        except smtplib.SMTPException as e:
            messagebox.showerror("Email Error", f"Email could not be sent.\n\n{e}")
            return False

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong.\n\n{e}")
            return False

    # ================= EMAIL HOVER =================
    def email_hover(self, event):
        email_box = event.widget
        email_box.itemconfig("border_arc", outline="#00ffff")
        email_box.itemconfig("border_line", fill="#00ffff")
        email_box.itemconfig("circle", fill="#00aaff")
        email_box.itemconfig("email", fill="#00ffff")

    # ================= EMAIL LEAVE =================
    def email_leave(self, event):
        email_box = event.widget
        email_box.itemconfig("border_arc", outline="#00aaff")
        email_box.itemconfig("border_line", fill="#00aaff")
        email_box.itemconfig("circle", fill="#0875d1")
        email_box.itemconfig("email", fill="#00c8ff")

    # ================= EMAIL SUPPORT =================
    def email_support(self, event=None):
        win = Toplevel(self.root)
        win.geometry("600x450+380+150")
        win.title("Email Support")
        win.resizable(False, False)

        Label(win, text="Email Support", font=("Segoe UI", 20, "bold"), fg="darkgreen").place(x=0, y=15, width=600, height=40)

        Label(win, text="Enter your message:", font=("Segoe UI", 12, "bold"), anchor="w").place(x=20, y=65, width=560, height=25)

        message_box = Text(win, font=("Segoe UI", 11), bd=2, relief=RIDGE)
        message_box.place(x=20, y=100, width=560, height=220)

        def send():
            message = message_box.get("1.0", END).strip()

            if message == "":
                messagebox.showwarning("Warning", "Please enter your message.")
                return

            success = self.send_email("Face Recognition System Support", message)

            if success:
                messagebox.showinfo("Success", "Your message has been sent successfully.")
                win.destroy()

        Button(win, text="Send Message", command=send, font=("Segoe UI", 12, "bold"), bg="darkgreen", fg="white", activebackground="#145214", activeforeground="white", bd=0, cursor="hand2").place(x=220, y=350, width=160, height=45)

    # ================= FAQ =================
    def faq(self):
        win = Toplevel(self.root)
        win.geometry("600x450+380+150")
        win.title("FAQ")
        win.resizable(False, False)

        Label(win, text="Frequently Asked Questions", font=("Segoe UI", 20, "bold"), fg="darkgreen").pack(pady=15)

        faq_text = (
            "1. How to add a student?\n"
            "Open Student Details and fill all required information.\n\n"
            "2. How to capture face data?\n"
            "Open Face Detector and enter the Student ID.\n\n"
            "3. How to train the data?\n"
            "Open Train Data after collecting face images.\n\n"
            "4. How to mark attendance?\n"
            "Open Attendance and start face recognition.\n\n"
            "5. Where are photos stored?\n"
            "Photos are stored inside the data folder."
        )

        Label(win, text=faq_text, font=("Segoe UI", 11), justify=LEFT, anchor="w").pack(padx=30, pady=10, fill=BOTH)

    # ================= COMPLAINT =================
    def complaint(self):
        win = Toplevel(self.root)
        win.geometry("600x450+380+150")
        win.title("Raise Complaint")
        win.resizable(False, False)

        Label(win, text="Raise Complaint", font=("Segoe UI", 20, "bold"), fg="darkgreen", anchor="center").place(x=0, y=15, width=600, height=40)

        Label(win, text="Enter your complaint:", font=("Segoe UI", 12, "bold"), anchor="w").place(x=20, y=65, width=560, height=28)

        complaint_box = Text(win, font=("Segoe UI", 11), bd=2, relief=RIDGE)
        complaint_box.place(x=20, y=100, width=560, height=220)

        def submit():
            complaint_text = complaint_box.get("1.0", END).strip()

            if complaint_text == "":
                messagebox.showwarning("Warning", "Please enter your complaint.")
                return

            success = self.send_email("Face Recognition System Complaint", complaint_text)

            if success:
                messagebox.showinfo("Success", "Your complaint has been sent successfully.")
                win.destroy()

        Button(win, text="Submit", command=submit, font=("Segoe UI", 12, "bold"), bg="darkgreen", fg="white", activebackground="#145214", activeforeground="white", bd=0, cursor="hand2").place(x=240, y=350, width=120, height=40)

    # ================= CONTACT ADMIN =================
    def contact_admin(self):
        win = Toplevel(self.root)
        win.geometry("500x300+430+220")
        win.title("Contact Admin")
        win.resizable(False, False)

        Label(win, text="Contact Administrator", font=("Segoe UI", 20, "bold"), fg="darkgreen").pack(pady=20)

        Label(win, text="Email : ochaurasiya786@gmail.com", font=("Segoe UI", 13, "bold"), fg="blue").pack(pady=10)

        Label(win, text="For system support and technical assistance.", font=("Segoe UI", 11)).pack(pady=10)

        Button(win, text="Send Email", command=self.email_support, font=("Segoe UI", 12, "bold"), bg="#18385f", fg="white", bd=0, cursor="hand2").pack(pady=20, ipadx=20, ipady=8)

    # ================= FACE RECOGNITION HELP =================
    def face_help(self):
        win = Toplevel(self.root)
        win.geometry("600x400+380+180")
        win.title("Face Recognition Help")
        win.resizable(False, False)

        Label(win, text="Face Recognition Help", font=("Segoe UI", 20, "bold"), fg="darkgreen").pack(pady=15)

        text = (
            "• First add the student in Student Details.\n\n"
            "• Open Face Detector and enter the Student ID.\n\n"
            "• Capture multiple face images with good lighting.\n\n"
            "• Train the collected face data using Train Data.\n\n"
            "• After training, use Attendance for recognition."
        )

        Label(win, text=text, font=("Segoe UI", 12), justify=LEFT, anchor="w").pack(padx=40, pady=15, fill=BOTH)

    # ================= ATTENDANCE HELP =================
    def attendance_help(self):
        win = Toplevel(self.root)
        win.geometry("600x400+380+180")
        win.title("Attendance Help")
        win.resizable(False, False)

        Label(win, text="Attendance Help", font=("Segoe UI", 20, "bold"), fg="darkgreen").pack(pady=15)

        text = (
            "• Make sure face data has been trained.\n\n"
            "• Open the Attendance section.\n\n"
            "• Start the face recognition process.\n\n"
            "• The recognized student's attendance will be recorded.\n\n"
            "• Check the attendance records after recognition."
        )

        Label(win, text=text, font=("Segoe UI", 12), justify=LEFT, anchor="w").pack(padx=40, pady=15, fill=BOTH)

    # ================= EXIT PROJECT =================
    def exit_project(self):
        answer = messagebox.askyesno("Exit", "Are you sure to exit this project?")

        if answer:
            self.root.destroy()


# ================= MAIN =================
if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()