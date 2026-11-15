from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from time import strftime
from College_images.student import Student
from face_recognition import Face_Recognition
from train import Train
from attendence import Attendance
from developer import Developer
from chat import Chatbot
from admin import Admin
import os


# MAIN SYSTEM

class Face_Recognition_System:

    def __init__(self, root, logout_callback=None):

        self.root = root
        self.logout_callback = logout_callback
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")
        self.root.resizable(False, False)

        # IMAGE DIRECTORY

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(base_dir, "College_images")

        # TOP IMAGES

        paths = [
            (
                os.path.join(image_dir, "home1.jpg"),
                440,
                0,
                440
            ),
            (
                os.path.join(image_dir, "img2.png"),
                480,
                440,
                468
            ),
            (
                os.path.join(image_dir, "face.png"),
                455,
                908,
                456
            )
        ]

        # TOP IMAGES WITH HOVER EFFECT

        for i, (path, size, x, width) in enumerate(paths, 1):

            img = Image.open(path).resize(
                (size, 130),
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(img)

            setattr(self, f"photoimg{i}", photo)

            top_img = Label(
                self.root,
                image=photo,
                bd=0,
                relief=FLAT,
                highlightthickness=1,
                highlightbackground="#18385f"
            )

            top_img.place(
                x=x,
                y=0,
                width=width,
                height=130
            )

            def image_enter(event, widget=top_img):
                widget.config(
                    relief=RAISED,
                    bd=2,
                    highlightbackground="#55c7ff",
                    highlightcolor="#55c7ff",
                    highlightthickness=2
                )

            def image_leave(event, widget=top_img):
                widget.config(
                    relief=FLAT,
                    bd=0,
                    highlightbackground="#18385f",
                    highlightcolor="#18385f",
                    highlightthickness=1
                )

            def image_press(event, widget=top_img):
                widget.config(
                    relief=SUNKEN,
                    bd=3,
                    highlightbackground="#0d5bb5",
                    highlightcolor="#0d5bb5"
                )

            def image_release(event, widget=top_img):
                widget.config(
                    relief=RAISED,
                    bd=2,
                    highlightbackground="#55c7ff",
                    highlightcolor="#55c7ff"
                )

            top_img.bind("<Enter>", image_enter)
            top_img.bind("<Leave>", image_leave)
            top_img.bind("<ButtonPress-1>", image_press)
            top_img.bind("<ButtonRelease-1>", image_release)

        # TITLE AREA

        title_frame = Frame(
            self.root,
            bg="#dbeafe"
        )

        title_frame.place(
            x=0,
            y=130,
            width=1366,
            height=100
        )

        title_label = Label(
            title_frame,
            text=" AI-BASED FACE RECOGNITION ATTENDANCE SYSTEM",
            font=("Cambria", 30, "bold"),
            bg="#dbeafe",
            fg="#18385f"
        )

        title_label.pack(
            pady=(10, 0)
        )

        subtitle_label = Label(
            title_frame,
            text="Smart Attendance Management System  •  Student Information  •  Attendance  •  Records Management",
            font=("Segoe UI", 11),
            bg="#dbeafe",
            fg="#4f6f95"
        )

        subtitle_label.pack()

        # TITLE HOVER EFFECT

        def title_enter(event):
            title_label.config(
                fg="#0d5bb5"
            )

        def title_leave(event):
            title_label.config(
                fg="#18385f"
            )

        title_label.bind("<Enter>", title_enter)
        title_label.bind("<Leave>", title_leave)

        # TIME

        lbl = Label(
            title_frame,
            font=("times new roman", 20, "bold"),
            bg="#dbeafe",
            fg="#1a6bd6"
        )

        lbl.place(
            x=1160,
            y=20,
            width=180,
            height=35
        )

        def time():
            lbl.config(
                text=strftime("%I:%M:%S %p")
            )

            lbl.after(
                1000,
                time
            )

        time()

        # BACKGROUND IMAGE

        bg_path = os.path.join(
            image_dir,
            "Base2.png"
        )

        bg_img = Image.open(
            bg_path
        ).resize(
            (1366, 538),
            Image.Resampling.LANCZOS
        )

        self.photoimg_bg = ImageTk.PhotoImage(
            bg_img
        )

        Label(
            self.root,
            image=self.photoimg_bg,
            bd=0
        ).place(
            x=0,
            y=230,
            width=1366,
            height=538
        )

        # DASHBOARD

        dashboard_frame = Frame(
            self.root,
            bg="#071426",
            bd=1,
            relief=SOLID,
            highlightbackground="#31577f",
            highlightthickness=1
        )

        dashboard_frame.place(
            x=14,
            y=230,
            width=1310,
            height=490
        )

        # DASHBOARD ICON

        Label(
            dashboard_frame,
            text="▦",
            font=("Segoe UI", 20, "bold"),
            bg="#071426",
            fg="#55c7ff"
        ).place(
            x=10,
            y=13,
            width=25,
            height=30
        )

        # DASHBOARD TITLE

        dashboard_title = Label(
            dashboard_frame,
            text="Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg="#071426",
            fg="white",
            anchor="nw"
        )

        dashboard_title.place(
            x=62,
            y=10,
            width=250,
            height=38
        )

        dashboard_subtitle = Label(
            dashboard_frame,
            text="Select an option to continue",
            font=("Segoe UI", 10),
            bg="#071426",
            fg="#9db4cf",
            anchor="nw"
        )

        dashboard_subtitle.place(
            x=64,
            y=48,
            width=250,
            height=20
        )

        # LOGOUT BUTTON

        logout_button = Button(
            dashboard_frame,
            text="Logout",
            command=self.logout,
            font=("Segoe UI", 10, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            bd=0,
            cursor="hand2"
        )

        logout_button.place(
            x=1170,
            y=10,
            width=110,
            height=35
        )

        # LOGOUT HOVER

        def logout_enter(event):
            logout_button.config(
                bg="#b91c1c"
            )

        def logout_leave(event):
            logout_button.config(
                bg="#dc2626"
            )

        logout_button.bind(
            "<Enter>",
            logout_enter
        )

        logout_button.bind(
            "<Leave>",
            logout_leave
        )

        # DASHBOARD TITLE HOVER

        def dashboard_enter(event):
            dashboard_title.config(
                fg="#55c7ff"
            )

        def dashboard_leave(event):
            dashboard_title.config(
                fg="white"
            )

        dashboard_title.bind(
            "<Enter>",
            dashboard_enter
        )

        dashboard_title.bind(
            "<Leave>",
            dashboard_leave
        )

        self._dashboard_parent = dashboard_frame

        # DASHBOARD CARDS

        cards = [
            (
                "img4",
                os.path.join(image_dir, "11.png"),
                "Student Details",
                self.student_details,
                (48, 84, 290, 205),
                (270, 145)
            ),
            (
                "img5",
                os.path.join(image_dir, "2.png"),
                "Face Recognition",
                self.face_detector,
                (373, 84, 290, 205),
                (270, 145)
            ),
            (
                "img6",
                os.path.join(image_dir, "333.png"),
                "Attendance",
                self.attendance,
                (698, 84, 290, 205),
                (270, 145)
            ),
            (
                "img7",
                os.path.join(image_dir, "4.png"),
                "AI Help Desk",
                self.help_desk,
                (1023, 84, 250, 205),
                (220, 145)
            ),
            (
                "img8",
                os.path.join(image_dir, "5.png"),
                "Train Data",
                self.train_data,
                (48, 304, 240, 155),
                (220, 105)
            ),
            (
                "img9",
                os.path.join(image_dir, "6.png"),
                "Photos",
                self.open_img,
                (303, 304, 240, 155),
                (220, 105)
            ),
            (
                "img10",
                os.path.join(image_dir, "Devloper11.png"),
                "Developer11",
                self.developer,
                (558, 304, 240, 155),
                (220, 105)
            ),
            (
                "img11",
                os.path.join(image_dir, "panel.png"),
                "Admin Panel",
                self.admin_panel,
                (813, 304, 240, 155),
                (220, 105)
            ),
            (
                "img12",
                os.path.join(image_dir, "8.png"),
                "Exit",
                self.exit_system,
                (1068, 304, 215, 155),
                (195, 105)
            )
        ]

        for card in cards:
            self._create_card(*card)

        # FOOTER

        footer_frame = Frame(
            dashboard_frame,
            bg="#071426",
            bd=1,
            relief=SOLID,
            highlightbackground="#1d456d",
            highlightthickness=1
        )

        footer_frame.place(
            x=165,
            y=462,
            width=980,
            height=27
        )

        footer = [
            ("♜  Secure System", 40, 150),
            ("|", 245, 20),
            ("⚙  AI Powered", 285, 150),
            ("|", 480, 20),
            ("◉  Real-time Recognition", 520, 190),
            ("|", 750, 20),
            ("✓  Smart & Reliable", 790, 160)
        ]

        for text, x, width in footer:

            footer_label = Label(
                footer_frame,
                text=text,
                font=(
                    "Segoe UI",
                    10 if text == "|" else 9,
                    "bold"
                ),
                bg="#071426",
                fg="#66809c" if text == "|" else "#55c7ff"
            )

            footer_label.place(
                x=x,
                y=0 if text == "|" else 1,
                width=width,
                height=22
            )

            if text != "|":

                def footer_enter(
                    event,
                    widget=footer_label
                ):
                    widget.config(
                        fg="#ffffff"
                    )

                def footer_leave(
                    event,
                    widget=footer_label
                ):
                    widget.config(
                        fg="#55c7ff"
                    )

                footer_label.bind(
                    "<Enter>",
                    footer_enter
                )

                footer_label.bind(
                    "<Leave>",
                    footer_leave
                )

    # CARD

    def _create_card(
        self,
        image_name,
        image_path,
        title,
        command,
        geometry,
        image_size
    ):

        x, y, width, height = geometry
        img_w, img_h = image_size

        # LOAD IMAGE

        img = Image.open(
            image_path
        ).resize(
            (img_w, img_h),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(
            img
        )

        setattr(
            self,
            f"photo{image_name}",
            photo
        )

        # CARD FRAME

        card = Frame(
            self._dashboard_parent,
            bg="#0c1c31",
            bd=2,
            relief=RAISED,
            highlightbackground="#7891aa",
            highlightcolor="#7891aa",
            highlightthickness=1
        )

        card.place(
            x=x,
            y=y,
            width=width,
            height=height
        )

        # IMAGE BUTTON

        image_button = Button(
            card,
            image=photo,
            command=command,
            cursor="hand2",
            bd=1,
            relief=FLAT,
            bg="#0c1c31",
            activebackground="#0c1c31",
            highlightthickness=0
        )

        image_button.place(
            x=9,
            y=9,
            width=img_w,
            height=img_h
        )

        # TITLE BUTTON

        title_button = Button(
            card,
            text=title,
            cursor="hand2",
            command=command,
            font=("Segoe UI", 13, "bold"),
            bg="#18385f",
            fg="white",
            activebackground="#245582",
            activeforeground="white",
            bd=1,
            relief=RAISED,
            highlightthickness=0
        )

        title_button.place(
            x=9,
            y=161 if height == 205 else 119,
            width=img_w,
            height=32 if height == 205 else 30
        )

        setattr(
            self,
            image_name,
            card
        )

        # HOVER EFFECT

        def hover_enter(event):

            card.config(
                relief=RAISED,
                bd=3,
                bg="#122b48",
                highlightbackground="#55c7ff",
                highlightcolor="#55c7ff",
                highlightthickness=2
            )

            image_button.config(
                relief=RAISED,
                bd=2,
                bg="#10243b",
                activebackground="#10243b"
            )

            title_button.config(
                relief=RAISED,
                bd=2,
                bg="#245582",
                fg="white"
            )

        def hover_leave(event):

            card.config(
                relief=SOLID,
                bd=1,
                bg="#0c1c31",
                highlightbackground="#7891aa",
                highlightcolor="#9ab0c5",
                highlightthickness=1
            )

            image_button.config(
                relief=FLAT,
                bd=1,
                bg="#0c1c31",
                activebackground="#0c1c31"
            )

            title_button.config(
                relief=RAISED,
                bd=1,
                bg="#18385f",
                fg="white"
            )

        # CLICK EFFECT

        def mouse_press(event):

            card.config(
                relief=SUNKEN,
                bd=3
            )

            image_button.config(
                relief=SUNKEN,
                bd=2
            )

            title_button.config(
                relief=SUNKEN,
                bd=2,
                bg="#163c62"
            )

        def mouse_release(event):

            card.config(
                relief=RAISED,
                bd=3
            )

            image_button.config(
                relief=RAISED,
                bd=2
            )

            title_button.config(
                relief=RAISED,
                bd=2,
                bg="#245582"
            )

        # CARD EVENTS

        card.bind(
            "<Enter>",
            hover_enter
        )

        card.bind(
            "<Leave>",
            hover_leave
        )

        card.bind(
            "<ButtonPress-1>",
            mouse_press
        )

        card.bind(
            "<ButtonRelease-1>",
            mouse_release
        )

        # IMAGE EVENTS

        image_button.bind(
            "<Enter>",
            hover_enter
        )

        image_button.bind(
            "<Leave>",
            hover_leave
        )

        image_button.bind(
            "<ButtonPress-1>",
            mouse_press
        )

        image_button.bind(
            "<ButtonRelease-1>",
            mouse_release
        )

        # TITLE EVENTS

        title_button.bind(
            "<Enter>",
            hover_enter
        )

        title_button.bind(
            "<Leave>",
            hover_leave
        )

        title_button.bind(
            "<ButtonPress-1>",
            mouse_press
        )

        title_button.bind(
            "<ButtonRelease-1>",
            mouse_release
        )

    # OPEN PHOTOS

    def open_img(self):

        folder_path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "data"
        )

        if os.path.exists(folder_path):

            os.startfile(
                folder_path
            )

        else:

            messagebox.showerror(
                "Error",
                "Data folder not found:\n" + folder_path,
                parent=self.root
            )

    # STUDENT DETAILS

    def student_details(self):

        self.new_window = Toplevel(
            self.root
        )

        self.app = Student(
            self.new_window
        )

    # TRAIN DATA

    def train_data(self):

        self.new_window = Toplevel(
            self.root
        )

        self.app = Train(
            self.new_window
        )

    # FACE DETECTOR

    def face_detector(self):

        self.new_window = Toplevel(
            self.root
        )

        self.app = Face_Recognition(
            self.new_window
        )

    # ATTENDANCE

    def attendance(self):

        self.new_window = Toplevel(
            self.root
        )

        self.app = Attendance(
            self.new_window
        )

    # DEVELOPER

    def developer(self):

        self.new_window = Toplevel(
            self.root
        )

        self.app = Developer(
            self.new_window
        )

    # AI HELP DESK

    def help_desk(self):

        self.new_window = Toplevel(
            self.root
        )

        self.app = Chatbot(
            self.new_window
        )

    # ADMIN PANEL

    def admin_panel(self):

        self.new_window = Toplevel(
            self.root
        )

        self.app = Admin(
            self.new_window
        )

    # LOGOUT SYSTEM

    def logout(self):

        if self.logout_callback:
            self.logout_callback()
        else:
            answer = messagebox.askyesno(
                "Logout",
                "Are you sure you want to logout?",
                parent=self.root
            )

            if answer:
                self.root.destroy()

    # EXIT SYSTEM

    def exit_system(self):

        answer = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to completely exit the application?",
            parent=self.root
        )

        if answer:
            try:
                self.root.destroy()
            except Exception:
                pass
            import sys, os
            sys.exit(0)
            os._exit(0)


# START SYSTEM

if __name__ == "__main__":

    root = Tk()

    app = Face_Recognition_System(
        root
    )

    root.mainloop()