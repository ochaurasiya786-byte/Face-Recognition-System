from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
from datetime import datetime, date


class Student:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Recognition System")
        self.root.geometry("1366x750+0+0")
        self.root.resizable(False, False)

        # PATHS
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.dirname(CURRENT_DIR)

        self.image_dir = CURRENT_DIR
        self.data_dir = os.path.join(BASE_DIR, "data")

        self.cascade_path = os.path.join(
            BASE_DIR,
            "haarcascade_frontalface_default.xml"
        )

        # COLORS
        bg_color = "#f4f7fb"
        white = "#ffffff"
        header_color = "#dbeafe"
        header_text = "#17365d"
        subtitle_color = "#4b6b88"
        frame_color = "#ffffff"
        border_color = "#b8c7d9"
        button_color = "#4f81bd"
        button_hover = "#3d6fa8"
        button_press = "#315d8d"
        search_color = "#5b9bd5"
        table_heading = "#d9eaf7"
        table_selected = "#cfe2f3"
        table_hover = "#eaf4ff"
        text_color = "#263746"

        self.root.configure(bg=bg_color)

        # VARIABLES
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_radio = StringVar()

        # MYSQL CONNECTION
        try:

            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Omkar@7518",
                database="student"
            )

            self.my_cursor = self.conn.cursor()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to connect with MySQL\n\n{e}",
                parent=self.root
            )

            return

        # STYLE
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "TCombobox",
            fieldbackground=white,
            background=white,
            foreground=text_color,
            bordercolor=border_color,
            lightcolor=border_color,
            darkcolor=border_color,
            padding=4,
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", white)],
            selectbackground=[("readonly", "#dbeafe")],
            selectforeground=[("readonly", text_color)]
        )

        style.configure(
            "TEntry",
            fieldbackground=white,
            foreground=text_color,
            bordercolor=border_color,
            lightcolor=border_color,
            padding=5,
            font=("Segoe UI", 10)
        )

        style.configure(
            "TRadiobutton",
            background=white,
            foreground=text_color,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Bold.TRadiobutton",
            background=white,
            foreground=text_color,
            font=("Segoe UI", 9, "bold")
        )

        style.configure(
            "Vertical.TScrollbar",
            width=18
        )

        style.configure(
            "Horizontal.TScrollbar",
            height=18
        )

        style.configure(
            "Treeview",
            background=white,
            foreground=text_color,
            fieldbackground=white,
            rowheight=28,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background=table_heading,
            foreground=header_text,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", table_selected)],
            foreground=[("selected", header_text)]
        )

        # BUTTON HOVER EFFECT
        def add_button_hover(button):

            button.bind(
                "<Enter>",
                lambda e, b=button: b.config(
                    bg=button_hover,
                    relief=RAISED
                )
            )

            button.bind(
                "<Leave>",
                lambda e, b=button: b.config(
                    bg=button_color,
                    relief=FLAT
                )
            )

            button.bind(
                "<ButtonPress-1>",
                lambda e, b=button: b.config(
                    bg=button_press,
                    relief=SUNKEN
                )
            )

            button.bind(
                "<ButtonRelease-1>",
                lambda e, b=button: b.config(
                    bg=button_hover,
                    relief=RAISED
                )
            )

        # IMAGE HOVER EFFECT
        def add_image_hover(label):

            label.bind(
                "<Enter>",
                lambda e, l=label: l.config(
                    highlightthickness=2,
                    highlightbackground=button_hover
                )
            )

            label.bind(
                "<Leave>",
                lambda e, l=label: l.config(
                    highlightthickness=0
                )
            )

        # TOP IMAGE 1
        img1 = Image.open(
            os.path.join(self.image_dir, "stu1.png")
        )

        img1 = img1.resize(
            (455, 120),
            Image.Resampling.LANCZOS
        )

        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(
            self.root,
            image=self.photoimg1,
            bd=0
        )

        f_lbl1.place(
            x=0,
            y=0,
            width=455,
            height=120
        )

        add_image_hover(f_lbl1)

        # TOP IMAGE 2
        img2 = Image.open(
            os.path.join(self.image_dir, "st2.png")
        )

        img2 = img2.resize(
            (455, 120),
            Image.Resampling.LANCZOS
        )

        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl2 = Label(
            self.root,
            image=self.photoimg2,
            bd=0
        )

        f_lbl2.place(
            x=455,
            y=0,
            width=455,
            height=120
        )

        add_image_hover(f_lbl2)

        # TOP IMAGE 3
        img3 = Image.open(
            os.path.join(self.image_dir, "stu3.png")
        )

        img3 = img3.resize(
            (456, 120),
            Image.Resampling.LANCZOS
        )

        self.photoimg3 = ImageTk.PhotoImage(img3)

        f_lbl3 = Label(
            self.root,
            image=self.photoimg3,
            bd=0
        )

        f_lbl3.place(
            x=910,
            y=0,
            width=456,
            height=120
        )

        add_image_hover(f_lbl3)

        # HEADER
        header_frame = Frame(
            self.root,
            bg=header_color,
            bd=0
        )

        header_frame.place(
            x=0,
            y=120,
            width=1366,
            height=65
        )

        # TITLE
        title_lbl = Label(
            header_frame,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Segoe UI", 26, "bold"),
            bg=header_color,
            fg=header_text
        )

        title_lbl.place(
            x=0,
            y=3,
            width=1366,
            height=38
        )

        title_lbl.bind(
            "<Enter>",
            lambda e: title_lbl.config(
                bg="#c7ddf5",
                fg="#102a43"
            )
        )

        title_lbl.bind(
            "<Leave>",
            lambda e: title_lbl.config(
                bg=header_color,
                fg=header_text
            )
        )

        # SUBTITLE
        subtitle_lbl = Label(
            header_frame,
            text="Student Information  •  Attendance  •  Records Management",
            font=("Segoe UI", 10),
            bg=header_color,
            fg=subtitle_color
        )

        subtitle_lbl.place(
            x=0,
            y=42,
            width=1366,
            height=20
        )

        # MAIN FRAME
        main_frame = Frame(
            self.root,
            bd=1,
            relief=SOLID,
            bg=bg_color,
            highlightthickness=0
        )

        main_frame.place(
            x=5,
            y=190,
            width=1356,
            height=550
        )

        # LEFT FRAME
        left_frame = LabelFrame(
            main_frame,
            bd=1,
            bg=frame_color,
            fg=header_text,
            relief=SOLID,
            text=" Student Details ",
            font=("Segoe UI", 11, "bold"),
            labelanchor="nw"
        )

        left_frame.place(
            x=10,
            y=5,
            width=665,
            height=540
        )

        # LEFT IMAGE
        img_left = Image.open(
            os.path.join(self.image_dir, "stuleft1.png")
        )

        img_left = img_left.resize(
            (650, 110),
            Image.Resampling.LANCZOS
        )

        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl_left = Label(
            left_frame,
            image=self.photoimg_left,
            bg=white,
            bd=0
        )

        f_lbl_left.place(
            x=5,
            y=0,
            width=650,
            height=110
        )

        add_image_hover(f_lbl_left)

        # CURRENT COURSE INFORMATION
        current_course_frame = LabelFrame(
            left_frame,
            bd=1,
            bg=white,
            fg=header_text,
            relief=SOLID,
            text=" Current Course Information ",
            font=("Segoe UI", 10, "bold")
        )

        current_course_frame.place(
            x=5,
            y=110,
            width=650,
            height=100
        )

        # DEPARTMENT
        department_label = Label(
            current_course_frame,
            text="Department",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        department_label.grid(
            row=0,
            column=0,
            padx=8,
            pady=5,
            sticky=W
        )

        department_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_dep,
            font=("Segoe UI", 10),
            state="readonly",
            width=20
        )

        department_combo["values"] = (
            "Select Department",
            "Computer Science",
            "Information Technology",
            "Electronics",
            "Mechanical",
            "Civil"
        )

        department_combo.grid(
            row=0,
            column=1,
            padx=4,
            pady=5,
            sticky=W
        )

        department_combo.current(0)

        # COURSE
        course_label = Label(
            current_course_frame,
            text="Course",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        course_label.grid(
            row=0,
            column=2,
            padx=8,
            pady=5,
            sticky=W
        )

        course_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_course,
            font=("Segoe UI", 10),
            state="readonly",
            width=20
        )

        course_combo["values"] = (
            "Select Course",
            "B.Tech",
            "M.Tech"
        )

        course_combo.grid(
            row=0,
            column=3,
            padx=4,
            pady=5,
            sticky=W
        )

        course_combo.current(0)

        # YEAR
        year_label = Label(
            current_course_frame,
            text="Year",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        year_label.grid(
            row=1,
            column=0,
            padx=8,
            pady=5,
            sticky=W
        )

        year_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_year,
            font=("Segoe UI", 10),
            state="readonly",
            width=20
        )

        year_combo["values"] = (
            "Select Year",
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        )

        year_combo.grid(
            row=1,
            column=1,
            padx=4,
            pady=5,
            sticky=W
        )

        year_combo.current(0)

        # SEMESTER
        semester_label = Label(
            current_course_frame,
            text="Semester",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        semester_label.grid(
            row=1,
            column=2,
            padx=8,
            pady=5,
            sticky=W
        )

        semester_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_semester,
            font=("Segoe UI", 10),
            state="readonly",
            width=20
        )

        semester_combo["values"] = (
            "Select Semester",
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th",
            "6th",
            "7th",
            "8th"
        )

        semester_combo.grid(
            row=1,
            column=3,
            padx=4,
            pady=5,
            sticky=W
        )

        semester_combo.current(0)

        # CLASS STUDENT INFORMATION
        class_student_frame = LabelFrame(
            left_frame,
            bd=1,
            bg=white,
            fg=header_text,
            relief=SOLID,
            text=" Class Student Information ",
            font=("Segoe UI", 10, "bold")
        )

        class_student_frame.place(
            x=5,
            y=207,
            width=650,
            height=245
        )

        # STUDENT ID
        student_id_label = Label(
            class_student_frame,
            text="Student ID:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        student_id_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky=W
        )

        student_id_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_std_id,
            width=22,
            font=("Segoe UI", 10)
        )

        student_id_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # STUDENT NAME
        student_name_label = Label(
            class_student_frame,
            text="Student Name:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        student_name_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=5,
            sticky=W
        )

        student_name_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_std_name,
            width=22,
            font=("Segoe UI", 10)
        )

        student_name_entry.grid(
            row=0,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # CLASS DIVISION
        class_division_label = Label(
            class_student_frame,
            text="Class Division:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        class_division_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky=W
        )

        class_division_combo = ttk.Combobox(
            class_student_frame,
            textvariable=self.var_div,
            font=("Segoe UI", 10),
            state="readonly",
            width=20
        )

        class_division_combo["values"] = (
            "Select Division",
            "A",
            "B",
            "C"
        )

        class_division_combo.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        class_division_combo.current(0)

        # ROLL NUMBER
        roll_number_label = Label(
            class_student_frame,
            text="Roll No:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        roll_number_label.grid(
            row=1,
            column=2,
            padx=10,
            pady=5,
            sticky=W
        )

        roll_number_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_roll,
            width=22,
            font=("Segoe UI", 10)
        )

        roll_number_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # GENDER
        gender_label = Label(
            class_student_frame,
            text="Gender:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        gender_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky=W
        )

        gender_combo = ttk.Combobox(
            class_student_frame,
            textvariable=self.var_gender,
            font=("Segoe UI", 10),
            state="readonly",
            width=20
        )

        gender_combo["values"] = (
            "Select Gender",
            "Male",
            "Female",
            "Other"
        )

        gender_combo.grid(
            row=2,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        gender_combo.current(0)

        # DOB
        dob_label = Label(
            class_student_frame,
            text="DOB:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        dob_label.grid(
            row=2,
            column=2,
            padx=10,
            pady=5,
            sticky=W
        )

        dob_frame = Frame(
            class_student_frame,
            bg=white
        )

        dob_frame.grid(
            row=2,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        self.dob_entry = Entry(
            dob_frame,
            textvariable=self.var_dob,
            width=17,
            font=("Segoe UI", 10),
            bg="white",
            fg=text_color,
            relief=SOLID,
            bd=1
        )

        self.dob_entry.pack(
            side=LEFT,
            ipady=4
        )

        # CALENDAR BUTTON
        calendar_btn = Button(
            dob_frame,
            text="📅",
            command=self.open_dob_calendar,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            width=3
        )

        calendar_btn.pack(
            side=LEFT,
            padx=(3, 0),
            ipady=3
        )

        add_button_hover(calendar_btn)

        # EMAIL
        email_label = Label(
            class_student_frame,
            text="Email:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        email_label.grid(
            row=3,
            column=0,
            padx=10,
            pady=5,
            sticky=W
        )

        email_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_email,
            width=22,
            font=("Segoe UI", 10)
        )

        email_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # PHONE NUMBER
        phone_number_label = Label(
            class_student_frame,
            text="Phone No:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        phone_number_label.grid(
            row=3,
            column=2,
            padx=10,
            pady=5,
            sticky=W
        )

        phone_number_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_phone,
            width=22,
            font=("Segoe UI", 10)
        )

        phone_number_entry.grid(
            row=3,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # ADDRESS
        address_label = Label(
            class_student_frame,
            text="Address:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        address_label.grid(
            row=4,
            column=0,
            padx=10,
            pady=5,
            sticky=W
        )

        address_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_address,
            width=22,
            font=("Segoe UI", 10)
        )

        address_entry.grid(
            row=4,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # TEACHER NAME
        teacher_name_label = Label(
            class_student_frame,
            text="Teacher Name:",
            font=("Segoe UI", 10, "bold"),
            bg=white,
            fg=text_color
        )

        teacher_name_label.grid(
            row=4,
            column=2,
            padx=10,
            pady=5,
            sticky=W
        )

        teacher_name_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_teacher,
            width=22,
            font=("Segoe UI", 10)
        )

        teacher_name_entry.grid(
            row=4,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # RADIO BUTTONS
        radiobtn1 = ttk.Radiobutton(
            class_student_frame,
            text="Take Photo Sample",
            variable=self.var_radio,
            value="yes",
            style="Bold.TRadiobutton"
        )

        radiobtn1.grid(
            row=5,
            column=0,
            padx=10,
            pady=(0, 8),
            sticky=W
        )

        radiobtn2 = ttk.Radiobutton(
            class_student_frame,
            text="No Photo Sample",
            variable=self.var_radio,
            value="no",
            style="Bold.TRadiobutton"
        )

        radiobtn2.grid(
            row=5,
            column=1,
            padx=10,
            pady=(0, 8),
            sticky=W
        )

        # BUTTON FRAME
        btn_frame = Frame(
            left_frame,
            bd=1,
            relief=SOLID,
            bg=white
        )

        btn_frame.place(
            x=5,
            y=455,
            width=650,
            height=83
        )

        for i in range(4):

            btn_frame.grid_columnconfigure(
                i,
                weight=1
            )

        # SAVE
        save_btn = Button(
            btn_frame,
            text="Save",
            command=self.add_data,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )

        save_btn.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky="ew"
        )

        add_button_hover(save_btn)

        # UPDATE
        update_btn = Button(
            btn_frame,
            text="Update",
            command=self.update_data,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )

        update_btn.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            sticky="ew"
        )

        add_button_hover(update_btn)

        # DELETE
        delete_btn = Button(
            btn_frame,
            text="Delete",
            command=self.delete_data,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )

        delete_btn.grid(
            row=0,
            column=2,
            padx=2,
            pady=2,
            sticky="ew"
        )

        add_button_hover(delete_btn)

        # RESET
        reset_btn = Button(
            btn_frame,
            text="Reset",
            command=self.reset_data,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )

        reset_btn.grid(
            row=0,
            column=3,
            padx=2,
            pady=2,
            sticky="ew"
        )

        add_button_hover(reset_btn)

        # TAKE PHOTO SAMPLE
        take_photo_btn = Button(
            btn_frame,
            text="Take Photo Sample",
            command=self.generate_dataset,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )

        take_photo_btn.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=2,
            pady=4,
            sticky="ew"
        )

        add_button_hover(take_photo_btn)

        # UPDATE PHOTO SAMPLE
        update_photo_btn = Button(
            btn_frame,
            text="Update Photo Sample",
            command=self.generate_dataset,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )

        update_photo_btn.grid(
            row=1,
            column=2,
            columnspan=2,
            padx=2,
            pady=2,
            sticky="ew"
        )

        add_button_hover(update_photo_btn)

        # RIGHT FRAME
        right_frame = LabelFrame(
            main_frame,
            bd=1,
            bg=frame_color,
            fg=header_text,
            relief=SOLID,
            text=" Student Records ",
            font=("Segoe UI", 11, "bold"),
            labelanchor="nw"
        )

        right_frame.place(
            x=685,
            y=5,
            width=660,
            height=540
        )

        # RIGHT IMAGE
        img_right = Image.open(
            os.path.join(self.image_dir, "righ2.png")
        )

        img_right = img_right.resize(
            (650, 145),
            Image.Resampling.LANCZOS
        )

        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl_right = Label(
            right_frame,
            image=self.photoimg_right,
            bg=white,
            bd=0
        )

        f_lbl_right.place(
            x=5,
            y=0,
            width=650,
            height=110
        )

        add_image_hover(f_lbl_right)

        # SEARCH SYSTEM
        Search_frame = LabelFrame(
            right_frame,
            bd=1,
            bg=white,
            fg=header_text,
            relief=SOLID,
            text=" Search System ",
            font=("Segoe UI", 10, "bold")
        )

        Search_frame.place(
            x=5,
            y=110,
            width=650,
            height=65
        )

        search_label_ = Label(
            Search_frame,
            text="Search By:",
            font=("Segoe UI", 10, "bold"),
            bg=search_color,
            fg=white,
            padx=6,
            pady=3
        )

        search_label_.grid(
            row=0,
            column=0,
            padx=8,
            pady=9,
            sticky=W
        )

        self.search_combo = ttk.Combobox(
            Search_frame,
            font=("Segoe UI", 10),
            state="readonly",
            width=16
        )

        self.search_combo["values"] = (
            "Select",
            "Name",
            "Roll Number",
            "Phone Number",
            "ID"
        )

        self.search_combo.current(0)

        self.search_combo.grid(
            row=0,
            column=1,
            padx=4,
            pady=9
        )

        self.search_entry = ttk.Entry(
            Search_frame,
            width=18,
            font=("Segoe UI", 10)
        )

        self.search_entry.grid(
            row=0,
            column=2,
            padx=4,
            pady=9
        )

        # SEARCH BUTTON
        search_btn = Button(
            Search_frame,
            text="Search",
            command=self.search_data,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            padx=8
        )

        search_btn.grid(
            row=0,
            column=3,
            padx=4,
            pady=8
        )

        add_button_hover(search_btn)

        # SHOW ALL BUTTON
        showAll_btn = Button(
            Search_frame,
            text="Show All",
            command=self.fetch_data,
            font=("Segoe UI", 10, "bold"),
            bg=button_color,
            fg=white,
            activebackground=button_hover,
            activeforeground=white,
            bd=0,
            relief=FLAT,
            cursor="hand2",
            padx=8
        )

        showAll_btn.grid(
            row=0,
            column=4,
            padx=4,
            pady=8
        )

        add_button_hover(showAll_btn)

        # TABLE FRAME
        Table_frame = Frame(
            right_frame,
            bd=1,
            bg=white,
            relief=SOLID
        )

        Table_frame.place(
            x=5,
            y=175,
            width=650,
            height=350
        )

        # SCROLLBAR
        scroll_x = ttk.Scrollbar(
            Table_frame,
            orient=HORIZONTAL,
            style="Horizontal.TScrollbar"
        )

        scroll_y = ttk.Scrollbar(
            Table_frame,
            orient=VERTICAL,
            style="Vertical.TScrollbar"
        )

        # TABLE
        self.student_table = ttk.Treeview(
            Table_frame,
            columns=(
                "department",
                "name",
                "division",
                "roll",
                "gender",
                "dob",
                "email",
                "phone",
                "address",
                "teacher",
                "id",
                "course",
                "year",
                "photo",
                "semester"
            ),
            show="headings",
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.config(
            command=self.student_table.xview
        )

        scroll_y.config(
            command=self.student_table.yview
        )

        # HEADINGS
        self.student_table.heading(
            "department",
            text="Department"
        )

        self.student_table.heading(
            "name",
            text="Name"
        )

        self.student_table.heading(
            "division",
            text="Division"
        )

        self.student_table.heading(
            "roll",
            text="Roll"
        )

        self.student_table.heading(
            "gender",
            text="Gender"
        )

        self.student_table.heading(
            "dob",
            text="DOB"
        )

        self.student_table.heading(
            "email",
            text="Email"
        )

        self.student_table.heading(
            "phone",
            text="Phone"
        )

        self.student_table.heading(
            "address",
            text="Address"
        )

        self.student_table.heading(
            "teacher",
            text="Teacher"
        )

        self.student_table.heading(
            "id",
            text="Student ID"
        )

        self.student_table.heading(
            "course",
            text="Course"
        )

        self.student_table.heading(
            "year",
            text="Year"
        )

        self.student_table.heading(
            "photo",
            text="Photo"
        )

        self.student_table.heading(
            "semester",
            text="Semester"
        )

        # COLUMNS
        columns_width = {
            "department": 150,
            "name": 150,
            "division": 100,
            "roll": 100,
            "gender": 100,
            "dob": 100,
            "email": 180,
            "phone": 120,
            "address": 180,
            "teacher": 150,
            "id": 100,
            "course": 100,
            "year": 100,
            "photo": 100,
            "semester": 100
        }

        for column, width in columns_width.items():

            self.student_table.column(
                column,
                width=width,
                minwidth=width
            )

        # TABLE + SCROLLBARS
        Table_frame.grid_rowconfigure(
            1,
            weight=1
        )

        Table_frame.grid_columnconfigure(
            0,
            weight=1
        )

        scroll_x.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.student_table.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        scroll_y.grid(
            row=1,
            column=1,
            sticky="ns"
        )

        # TABLE ROW HOVER
        self.student_table.tag_configure(
            "hover",
            background=table_hover,
            foreground=header_text
        )

        self.hovered_item = None

        def row_hover(event):

            item = self.student_table.identify_row(event.y)

            if self.hovered_item and self.hovered_item != item:

                try:
                    self.student_table.item(
                        self.hovered_item,
                        tags=()
                    )
                except:
                    pass

            if item:

                self.student_table.item(
                    item,
                    tags=("hover",)
                )

                self.hovered_item = item

            else:

                self.hovered_item = None

        def row_leave(event):

            if self.hovered_item:

                try:
                    self.student_table.item(
                        self.hovered_item,
                        tags=()
                    )
                except:
                    pass

                self.hovered_item = None

        self.student_table.bind(
            "<Motion>",
            row_hover
        )

        self.student_table.bind(
            "<Leave>",
            row_leave
        )

        # SELECT TABLE DATA
        self.student_table.bind(
            "<ButtonRelease>",
            self.get_cursor
        )

        # FETCH DATA
        self.fetch_data()

        # CLOSE WINDOW
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_window
        )

    # DOB CALENDAR
    def open_dob_calendar(self):

        if hasattr(self, "dob_popup"):

            try:

                if self.dob_popup.winfo_exists():
                    self.dob_popup.destroy()

            except:
                pass

        self.dob_popup = Toplevel(self.root)

        self.dob_popup.title(
            "Select Date of Birth"
        )

        self.dob_popup.geometry(
            "350x430"
        )

        self.dob_popup.resizable(
            False,
            False
        )

        self.dob_popup.configure(
            bg="white"
        )

        self.dob_popup.transient(
            self.root
        )

        self.dob_popup.grab_set()

        self.root.update_idletasks()

        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()

        self.dob_popup.geometry(
            f"+{root_x+500}+{root_y+170}"
        )

        title = Label(
            self.dob_popup,
            text="Select Date of Birth",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#17365d"
        )

        title.pack(
            pady=(12, 8)
        )

        year_frame = Frame(
            self.dob_popup,
            bg="white"
        )

        year_frame.pack(
            pady=5
        )

        year_label = Label(
            year_frame,
            text="Select Year:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#263746"
        )

        year_label.pack(
            side=LEFT,
            padx=(0, 8)
        )

        current_year = date.today().year

        self.dob_year_combo = ttk.Combobox(
            year_frame,
            state="readonly",
            width=15,
            font=("Segoe UI", 10, "bold")
        )

        self.dob_year_combo["values"] = tuple(
            str(year)
            for year in range(
                1950,
                current_year + 1
            )
        )

        self.dob_year_combo.pack(
            side=LEFT
        )

        selected_year = 2000
        selected_month = 1
        selected_day = 1

        dob_value = self.var_dob.get().strip()

        if dob_value:

            try:

                selected_date = datetime.strptime(
                    dob_value,
                    "%d-%m-%Y"
                )

                selected_year = selected_date.year
                selected_month = selected_date.month
                selected_day = selected_date.day

            except:
                pass

        if (
            selected_year < 1950
            or selected_year > current_year
        ):

            selected_year = 2000

        self.dob_year_combo.set(
            str(selected_year)
        )

        self.dob_calendar = Calendar(
            self.dob_popup,
            selectmode="day",
            year=selected_year,
            month=selected_month,
            day=selected_day,
            date_pattern="dd-mm-yyyy",
            background="white",
            foreground="#17365d",
            headersbackground="#dbeafe",
            headersforeground="#17365d",
            selectbackground="#4f81bd",
            selectforeground="white",
            normalbackground="white",
            normalforeground="#263746",
            weekendbackground="#f4f7fb",
            weekendforeground="#263746",
            othermonthbackground="#f4f7fb",
            othermonthforeground="#9aa9b8",
            borderwidth=1
        )

        self.dob_calendar.pack(
            padx=15,
            pady=10
        )

        self.dob_year_combo.bind(
            "<<ComboboxSelected>>",
            self.change_dob_year
        )

        select_btn = Button(
            self.dob_popup,
            text="Select Date",
            command=self.select_dob_date,
            font=("Segoe UI", 10, "bold"),
            bg="#4f81bd",
            fg="white",
            activebackground="#3d6fa8",
            activeforeground="white",
            bd=0,
            relief=FLAT,
            cursor="hand2"
        )

        select_btn.pack(
            pady=(3, 12),
            ipadx=25,
            ipady=6
        )

        select_btn.bind(
            "<Enter>",
            lambda e: select_btn.config(
                bg="#3d6fa8",
                relief=RAISED
            )
        )

        select_btn.bind(
            "<Leave>",
            lambda e: select_btn.config(
                bg="#4f81bd",
                relief=FLAT
            )
        )

        select_btn.bind(
            "<ButtonPress-1>",
            lambda e: select_btn.config(
                bg="#315d8d",
                relief=SUNKEN
            )
        )

        select_btn.bind(
            "<ButtonRelease-1>",
            lambda e: select_btn.config(
                bg="#3d6fa8",
                relief=RAISED
            )
        )

    # CHANGE DOB YEAR
    def change_dob_year(self, event=None):

        try:

            selected_year = int(
                self.dob_year_combo.get()
            )

            current_date = self.dob_calendar.selection_get()

            month = current_date.month
            day = current_date.day

            try:

                new_date = date(
                    selected_year,
                    month,
                    day
                )

            except ValueError:

                new_date = date(
                    selected_year,
                    month,
                    1
                )

            self.dob_calendar.selection_set(
                new_date
            )

            self.dob_calendar.see(
                new_date
            )

        except Exception:
            pass

    # SELECT DOB DATE
    def select_dob_date(self):

        try:

            selected_date = (
                self.dob_calendar.selection_get()
            )

            formatted_date = selected_date.strftime(
                "%d-%m-%Y"
            )

            self.var_dob.set(
                formatted_date
            )

            self.dob_popup.destroy()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to select date.\n\n{e}",
                parent=self.root
            )

    # CHECK APPROVED STUDENT ID
    def check_student_id(self, student_id):

        try:

            self.my_cursor.execute(
                """
                SELECT Student_ID, Student_Name, Dep
                FROM student
                WHERE Student_ID=%s
                """,
                (student_id,)
            )

            result = self.my_cursor.fetchone()

            if result:
                return result

            return None

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to verify Student ID.\n\n{e}",
                parent=self.root
            )

            return None

    # ADD DATA
    def add_data(self):

        if (
            self.var_dep.get() == "Select Department"
            or self.var_course.get() == "Select Course"
            or self.var_year.get() == "Select Year"
            or self.var_semester.get() == "Select Semester"
            or self.var_div.get() == "Select Division"
            or self.var_gender.get() == "Select Gender"
            or self.var_std_name.get().strip() == ""
            or self.var_std_id.get().strip() == ""
        ):

            messagebox.showerror(
                "Error",
                "All required fields are required",
                parent=self.root
            )

            return

        student_id_text = (
            self.var_std_id.get().strip()
        )

        if not student_id_text.isdigit():

            messagebox.showerror(
                "Error",
                "Student ID must contain numbers only.",
                parent=self.root
            )

            return

        try:

            student_id = int(
                student_id_text
            )

            # CHECK APPROVED STUDENT
            existing_student = self.check_student_id(
                student_id
            )

            if existing_student:

                messagebox.showerror(
                    "Error",
                    "Student ID already exists in approved student database.",
                    parent=self.root
                )

                return

            # CHECK PENDING REQUEST
            self.my_cursor.execute(
                """
                SELECT Request_ID, Status
                FROM student_requests
                WHERE Student_ID=%s
                AND Status='Pending'
                """,
                (student_id,)
            )

            pending_request = self.my_cursor.fetchone()

            if pending_request:

                messagebox.showwarning(
                    "Already Submitted",
                    "This student registration request is already pending.\n\n"
                    "Please wait for Admin approval.",
                    parent=self.root
                )

                return

            # INSERT REGISTRATION REQUEST
            sql = """
                INSERT INTO student_requests
                (
                    Dep,
                    Course,
                    Year,
                    Semester,
                    Student_ID,
                    Student_Name,
                    Division,
                    Roll,
                    Gender,
                    DOB,
                    Email,
                    Phone,
                    Address,
                    Teacher,
                    PhotoSample,
                    Status
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s
                )
            """

            values = (
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                student_id,
                self.var_std_name.get().strip(),
                self.var_div.get(),
                self.var_roll.get().strip(),
                self.var_gender.get(),
                self.var_dob.get().strip(),
                self.var_email.get().strip(),
                self.var_phone.get().strip(),
                self.var_address.get().strip(),
                self.var_teacher.get().strip(),
                self.var_radio.get()
                if self.var_radio.get()
                else "No",
                "Pending"
            )

            self.my_cursor.execute(
                sql,
                values
            )

            self.conn.commit()
            new_request_id = self.my_cursor.lastrowid

            # Trigger immediate email notification to Admin in background
            try:
                import threading
                from approval_service import send_approval_email, get_request_by_id

                def notify_admin_async(rid):
                    try:
                        req_data = get_request_by_id(rid)
                        if req_data:
                            send_approval_email(req_data)
                    except Exception as ex:
                        print("Background email dispatch error:", ex)

                threading.Thread(target=notify_admin_async, args=(new_request_id,), daemon=True).start()
            except Exception as ex:
                print("Could not launch email notification thread:", ex)

            messagebox.showinfo(
                "Registration Submitted",
                "Student registration request submitted successfully.\n\n"
                "Status: Pending\n\n"
                "Please wait for Admin approval.",
                parent=self.root
            )

            self.clear_fields()

        except mysql.connector.Error as e:

            try:
                self.conn.rollback()
            except:
                pass

            messagebox.showerror(
                "Database Error",
                f"Unable to submit registration request.\n\n{e}",
                parent=self.root
            )

    # FETCH APPROVED STUDENTS
    def fetch_data(self):

        try:

            self.my_cursor.execute(
                """
                SELECT
                    Dep,
                    Student_Name,
                    Division,
                    Roll,
                    Gender,
                    DOB,
                    Email,
                    Phone,
                    Address,
                    Teacher,
                    Student_ID,
                    Course,
                    Year,
                    PhotoSample,
                    Semester
                FROM student
                """
            )

            data = self.my_cursor.fetchall()

            self.student_table.delete(
                *self.student_table.get_children()
            )

            for row in data:

                self.student_table.insert(
                    "",
                    END,
                    values=row
                )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Error",
                f"Due To: {e}",
                parent=self.root
            )

    # GET CURSOR
    def get_cursor(self, event=""):

        cursor_row = self.student_table.focus()

        content = self.student_table.item(
            cursor_row
        )

        row = content.get("values")

        if row:

            self.var_dep.set(row[0])
            self.var_std_name.set(row[1])
            self.var_div.set(row[2])
            self.var_roll.set(row[3])
            self.var_gender.set(row[4])
            self.var_dob.set(row[5])
            self.var_email.set(row[6])
            self.var_phone.set(row[7])
            self.var_address.set(row[8])
            self.var_teacher.set(row[9])
            self.var_std_id.set(row[10])
            self.var_course.set(row[11])
            self.var_year.set(row[12])
            self.var_radio.set(row[13])
            self.var_semester.set(row[14])

    # UPDATE DATA
    def update_data(self):

        if self.var_std_id.get() == "":

            messagebox.showerror(
                "Error",
                "Please select student data first",
                parent=self.root
            )

            return

        try:

            update = messagebox.askyesno(
                "Update",
                "Do you want to update this student data?",
                parent=self.root
            )

            if update:

                sql = """
                    UPDATE student SET
                    Dep=%s,
                    Course=%s,
                    Year=%s,
                    Semester=%s,
                    Student_Name=%s,
                    Division=%s,
                    Roll=%s,
                    Gender=%s,
                    DOB=%s,
                    Email=%s,
                    Phone=%s,
                    Address=%s,
                    Teacher=%s,
                    PhotoSample=%s
                    WHERE Student_ID=%s
                """

                values = (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio.get(),
                    self.var_std_id.get()
                )

                self.my_cursor.execute(
                    sql,
                    values
                )

                self.conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Student details updated successfully",
                    parent=self.root
                )

                self.fetch_data()
                self.clear_fields()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Error",
                f"Due To: {e}",
                parent=self.root
            )

    # DELETE DATA
    def delete_data(self):

        if self.var_std_id.get() == "":

            messagebox.showerror(
                "Error",
                "Student ID is required",
                parent=self.root
            )

            return

        try:

            delete = messagebox.askyesno(
                "Delete",
                "Do you want to delete this student data?",
                parent=self.root
            )

            if delete:

                sql = """
                    DELETE FROM student
                    WHERE Student_ID=%s
                """

                value = (
                    self.var_std_id.get(),
                )

                self.my_cursor.execute(
                    sql,
                    value
                )

                self.conn.commit()

                messagebox.showinfo(
                    "Delete",
                    "Student data deleted successfully",
                    parent=self.root
                )

                self.fetch_data()
                self.clear_fields()

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Error",
                f"Due To: {e}",
                parent=self.root
            )

    # SEARCH DATA
    def search_data(self):

        if self.search_combo.get() == "Select":

            messagebox.showerror(
                "Error",
                "Please select search option",
                parent=self.root
            )

            return

        if self.search_entry.get() == "":

            messagebox.showerror(
                "Error",
                "Please enter search value",
                parent=self.root
            )

            return

        try:

            selected = self.search_combo.get()
            value = self.search_entry.get()

            sql = """
                SELECT
                    Dep,
                    Student_Name,
                    Division,
                    Roll,
                    Gender,
                    DOB,
                    Email,
                    Phone,
                    Address,
                    Teacher,
                    Student_ID,
                    Course,
                    Year,
                    PhotoSample,
                    Semester
                FROM student
            """

            if selected == "Name":

                sql += """
                    WHERE Student_Name LIKE %s
                """

            elif selected == "Roll Number":

                sql += """
                    WHERE Roll LIKE %s
                """

            elif selected == "Phone Number":

                sql += """
                    WHERE Phone LIKE %s
                """

            elif selected == "ID":

                sql += """
                    WHERE Student_ID LIKE %s
                """

            else:
                return

            self.my_cursor.execute(
                sql,
                ("%" + value + "%",)
            )

            data = self.my_cursor.fetchall()

            self.student_table.delete(
                *self.student_table.get_children()
            )

            for row in data:

                self.student_table.insert(
                    "",
                    END,
                    values=row
                )

        except mysql.connector.Error as e:

            messagebox.showerror(
                "Error",
                f"Due To: {e}",
                parent=self.root
            )

    # RESET DATA
    def reset_data(self):

        self.clear_fields()

        self.search_combo.current(0)

        self.search_entry.delete(
            0,
            END
        )

        self.fetch_data()

    # CLEAR FIELDS
    def clear_fields(self):

        self.var_dep.set(
            "Select Department"
        )

        self.var_course.set(
            "Select Course"
        )

        self.var_year.set(
            "Select Year"
        )

        self.var_semester.set(
            "Select Semester"
        )

        self.var_std_id.set("")

        self.var_std_name.set("")

        self.var_div.set(
            "Select Division"
        )

        self.var_roll.set("")

        self.var_gender.set(
            "Select Gender"
        )

        self.var_dob.set("")

        self.var_email.set("")

        self.var_phone.set("")

        self.var_address.set("")

        self.var_teacher.set("")

        self.var_radio.set("")

    # GENERATE DATASET
    def generate_dataset(self):

        if (
            self.var_std_id.get() == ""
            or self.var_std_name.get() == ""
        ):

            messagebox.showerror(
                "Error",
                "Student ID and Student Name are required",
                parent=self.root
            )

            return

        student_id_text = (
            self.var_std_id.get().strip()
        )

        if not student_id_text.isdigit():

            messagebox.showerror(
                "Error",
                "Student ID must contain numbers only.",
                parent=self.root
            )

            return

        student_id = int(
            student_id_text
        )

        cap = None

        try:

            # VERIFY APPROVED STUDENT
            student_data = self.check_student_id(
                student_id
            )

            if student_data is None:

                messagebox.showerror(
                    "Error",
                    "Student ID is not approved yet.\n\n"
                    "Admin approval is required before taking photo samples.",
                    parent=self.root
                )

                return

            # GET DATABASE NAME
            database_name = student_data[1]

            if database_name != self.var_std_name.get().strip():

                messagebox.showerror(
                    "Error",
                    "Student ID and Student Name do not match.",
                    parent=self.root
                )

                return

            # CHECK CASCADE
            if not os.path.exists(
                self.cascade_path
            ):

                messagebox.showerror(
                    "Error",
                    "haarcascade_frontalface_default.xml file not found.",
                    parent=self.root
                )

                return

            face_classifier = cv2.CascadeClassifier(
                self.cascade_path
            )

            if face_classifier.empty():

                messagebox.showerror(
                    "Error",
                    "Unable to load Haar Cascade.",
                    parent=self.root
                )

                return

            # FACE CROPPED FUNCTION
            def face_cropped(img):

                gray = cv2.cvtColor(
                    img,
                    cv2.COLOR_BGR2GRAY
                )

                faces = face_classifier.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=5
                )

                for (x, y, w, h) in faces:

                    face_cropped = img[
                        y:y+h,
                        x:x+w
                    ]

                    return face_cropped

                return None

            # DATA FOLDER
            os.makedirs(
                self.data_dir,
                exist_ok=True
            )

            # OPEN CAMERA
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():

                messagebox.showerror(
                    "Camera Error",
                    "Camera could not be opened.",
                    parent=self.root
                )

                return

            img_id = 0

            window_name = "Cropped Face"

            cv2.namedWindow(
                window_name,
                cv2.WINDOW_NORMAL
            )

            cv2.resizeWindow(
                window_name,
                500,
                500
            )

            # CAMERA LOOP
            while True:

                ret, my_frame = cap.read()

                if not ret:
                    break

                # MIRROR CAMERA
                my_frame = cv2.flip(
                    my_frame,
                    1
                )

                cropped_face = face_cropped(
                    my_frame
                )

                if cropped_face is not None:

                    try:

                        face = cv2.resize(
                            cropped_face,
                            (450, 450)
                        )

                    except cv2.error:

                        continue

                    face = cv2.cvtColor(
                        face,
                        cv2.COLOR_BGR2GRAY
                    )

                    img_id += 1

                    # FILE NAME
                    file_name_path = os.path.join(
                        self.data_dir,
                        f"user.{student_id}.{img_id}.jpg"
                    )

                    cv2.imwrite(
                        file_name_path,
                        face
                    )

                    # DISPLAY
                    display_face = face.copy()

                    cv2.putText(
                        display_face,
                        "Sample: " + str(img_id),
                        (30, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        display_face,
                        "ID: " + str(student_id),
                        (30, 90),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

                    cv2.imshow(
                        window_name,
                        display_face
                    )

                else:

                    display_frame = my_frame.copy()

                    cv2.putText(
                        display_frame,
                        "Face Not Detected",
                        (30, 40),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                    cv2.imshow(
                        window_name,
                        display_frame
                    )

                key = cv2.waitKey(1) & 0xFF

                if key == 13 or key == 27:
                    break

                # 100 IMAGES
                if img_id >= 100:
                    break

            # RELEASE CAMERA
            cap.release()
            cap = None

            cv2.destroyAllWindows()

            # UPDATE PHOTOSAMPLE
            if img_id > 0:

                try:

                    self.my_cursor.execute(
                        """
                        UPDATE student
                        SET PhotoSample=%s
                        WHERE Student_ID=%s
                        """,
                        ("yes", student_id)
                    )

                    self.conn.commit()

                    self.var_radio.set(
                        "yes"
                    )

                except mysql.connector.Error:

                    pass

                messagebox.showinfo(
                    "Result",
                    f"Generating data sets completed!!!\n\n"
                    f"Student ID: {student_id}\n"
                    f"Student Name: {self.var_std_name.get()}\n"
                    f"Total Samples: {img_id}",
                    parent=self.root
                )

            else:

                messagebox.showwarning(
                    "Result",
                    "No face detected.\n"
                    "No dataset was created.",
                    parent=self.root
                )

        except Exception as e:

            if cap is not None:

                try:
                    cap.release()
                except:
                    pass

            cv2.destroyAllWindows()

            messagebox.showerror(
                "Error",
                f"Due To: {e}",
                parent=self.root
            )

    # CLOSE WINDOW
    def close_window(self):

        try:
            self.my_cursor.close()
        except:
            pass

        try:
            self.conn.close()
        except:
            pass

        self.root.destroy()


# MAIN
if __name__ == "__main__":

    root = Tk()

    obj = Student(root)

    root.mainloop()