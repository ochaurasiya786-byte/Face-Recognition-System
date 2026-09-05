from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from time import strftime
from College_images.student import Student
from face_recognition import Face_Recognition
from train import Train
from attendence import Attendance
from developer import Developer
from Help import Help
from login import Login_Register
import os


# ================= MAIN SYSTEM =================
class Face_Recognition_System:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")
        self.root.resizable(False, False)

        # ================= TOP IMAGE 1 =================
        img1 = Image.open(r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\home1.jpg")
        img1 = img1.resize((440, 130), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1, bd=0).place(x=0, y=0, width=440, height=130)

        # ================= TOP IMAGE 2 =================
        img2 = Image.open(r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\img2.png")
        img2 = img2.resize((480, 130), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2, bd=0).place(x=440, y=0, width=468, height=130)

        # ================= TOP IMAGE 3 =================
        img3 = Image.open(r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\face.png")
        img3 = img3.resize((455, 130), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        Label(self.root, image=self.photoimg3, bd=0).place(x=908, y=0, width=456, height=130)

        # ================= TITLE AREA =================
        title_frame = Frame(self.root, bg="#dbeafe")
        title_frame.place(x=0, y=130, width=1366, height=100)

        Label(title_frame, text="FACE RECOGNITION ATTENDANCE SYSTEM",
              font=("Cambria", 30, "bold"),
              bg="#dbeafe", fg="#18385f").pack(pady=(10, 0))

        Label(title_frame,
              text="Smart Attendance Management System  •  Student Information  •  Attendance  •  Records Management",
              font=("Segoe UI", 11),
              bg="#dbeafe", fg="#4f6f95").pack()

        # ================= TIME =================
        lbl = Label(title_frame, font=("times new roman", 20, "bold"),
                    bg="#dbeafe", fg="#1a6bd6")
        lbl.place(x=1160, y=20, width=180, height=35)

        def time():
            lbl.config(text=strftime("%I:%M:%S %p"))
            lbl.after(1000, time)

        time()

        # ================= BACKGROUND IMAGE =================
        bg_img = Image.open(r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\Base2.png")
        bg_img = bg_img.resize((1366, 538), Image.Resampling.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(bg_img)
        Label(self.root, image=self.photoimg_bg, bd=0).place(x=0, y=230, width=1366, height=538)

        # ================= DASHBOARD =================
        dashboard_frame = Frame(self.root, bg="#071426", bd=1, relief=SOLID,
                                highlightbackground="#31577f", highlightthickness=1)
        dashboard_frame.place(x=14, y=230, width=1310, height=490)

        Label(dashboard_frame, text="▦", font=("Segoe UI", 20, "bold"),
              bg="#071426", fg="#55c7ff").place(x=10, y=13, width=25, height=30)

        Label(dashboard_frame, text="Dashboard", font=("Segoe UI", 22, "bold"),
              bg="#071426", fg="white", anchor="nw").place(x=62, y=10, width=250, height=38)

        Label(dashboard_frame, text="Select an option to continue",
              font=("Segoe UI", 10), bg="#071426", fg="#9db4cf",
              anchor="nw").place(x=64, y=48, width=250, height=20)

        self._dashboard_parent = dashboard_frame

        # ================= DASHBOARD CARDS =================
        self._create_card(
            "img4",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\11.png",
            "Student Details",
            self.student_details,
            (48, 84, 290, 205),
            (270, 145)
        )

        self._create_card(
            "img5",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\2.png",
            "Face Recognition",
            self.face_detector,
            (373, 84, 290, 205),
            (270, 145)
        )

        self._create_card(
            "img6",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\333.png",
            "Attendance",
            self.attendance,
            (698, 84, 290, 205),
            (270, 145)
        )

        self._create_card(
            "img7",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\4.png",
            "Help Desk",
            self.help_desk,
            (1023, 84, 250, 205),
            (220, 145)
        )

        self._create_card(
            "img8",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\5.png",
            "Train Data",
            self.train_data,
            (48, 304, 290, 155),
            (270, 105)
        )

        self._create_card(
            "img9",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\6.png",
            "Photos",
            self.open_img,
            (373, 304, 290, 155),
            (270, 105)
        )

        self._create_card(
            "img10",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\Devloper11.png",
            "Developer11",
            self.developer,
            (698, 304, 290, 155),
            (270, 105)
        )

        self._create_card(
            "img11",
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\8.png",
            "Exit",
            self.exit_system,
            (1023, 304, 240, 155),
            (220, 105)
        )

        # ================= FOOTER =================
        footer_frame = Frame(dashboard_frame, bg="#071426", bd=1,
                             relief=SOLID, highlightbackground="#1d456d",
                             highlightthickness=1)
        footer_frame.place(x=165, y=462, width=980, height=27)

        Label(footer_frame, text="♜  Secure System",
              font=("Segoe UI", 9, "bold"), bg="#071426",
              fg="#55c7ff").place(x=40, y=1, width=150, height=22)

        Label(footer_frame, text="|", font=("Segoe UI", 10, "bold"),
              bg="#071426", fg="#66809c").place(x=245, y=0, width=20, height=22)

        Label(footer_frame, text="⚙  AI Powered",
              font=("Segoe UI", 9, "bold"), bg="#071426",
              fg="#55c7ff").place(x=285, y=1, width=150, height=22)

        Label(footer_frame, text="|", font=("Segoe UI", 10, "bold"),
              bg="#071426", fg="#66809c").place(x=480, y=0, width=20, height=22)

        Label(footer_frame, text="◉  Real-time Recognition",
              font=("Segoe UI", 9, "bold"), bg="#071426",
              fg="#55c7ff").place(x=520, y=1, width=190, height=22)

        Label(footer_frame, text="|", font=("Segoe UI", 10, "bold"),
              bg="#071426", fg="#66809c").place(x=750, y=0, width=20, height=22)

        Label(footer_frame, text="✓  Smart & Reliable",
              font=("Segoe UI", 9, "bold"), bg="#071426",
              fg="#55c7ff").place(x=790, y=1, width=160, height=22)


    # ================= CARD =================
    def _create_card(self, image_name, image_path, title, command, geometry, image_size):
        x, y, width, height = geometry
        img_w, img_h = image_size

        img = Image.open(image_path).resize(
            (img_w, img_h), Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(img)
        setattr(self, f"photo{image_name}", photo)

        card = Frame(
            self._dashboard_parent,
            bg="#0c1c31",
            bd=1,
            relief=SOLID,
            highlightbackground="#7891aa",
            highlightcolor="#9ab0c5",
            highlightthickness=1
        )

        card.place(x=x, y=y, width=width, height=height)

        Button(
            card,
            image=photo,
            command=command,
            cursor="hand2",
            bd=0,
            relief=FLAT,
            bg="#0c1c31",
            activebackground="#0c1c31"
        ).place(x=9, y=9, width=img_w, height=img_h)

        text_h = 32 if height == 205 else 30
        text_y = 161 if height == 205 else 119

        Button(
            card,
            text=title,
            cursor="hand2",
            command=command,
            font=("Segoe UI", 13, "bold"),
            bg="#18385f",
            fg="white",
            activebackground="#245582",
            activeforeground="white",
            bd=0
        ).place(x=9, y=text_y, width=img_w, height=text_h)

        setattr(self, image_name, card)


    # ================= OPEN PHOTOS =================
    def open_img(self):
        folder_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data"
        )

        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print("Data folder not found:", folder_path)


    # ================= STUDENT DETAILS =================
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)


    # ================= TRAIN DATA =================
    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)


    # ================= FACE DETECTOR =================
    def face_detector(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)


    # ================= ATTENDANCE =================
    def attendance(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)


    # ================= DEVELOPER =================
    def developer(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)


    # ================= HELP DESK =================
    def help_desk(self):
        self.new_window = Toplevel(self.root)
        self.app = Help(self.new_window)


    # ================= EXIT SYSTEM =================
    def exit_system(self):
        answer = messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit?"
        )

        if answer:
            self.root.destroy()


# ================= START WITH LOGIN =================
if __name__ == "__main__":
    root = Tk()
    app = Login_Register(root)
    root.mainloop()

