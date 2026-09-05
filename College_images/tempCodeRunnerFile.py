from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector


class Student:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1366x750+0+0")
        self.root.resizable(False, False)

        # Variable declaration

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
                database="face_recognizer"
            )

            self.my_cursor = self.conn.cursor()

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                f"Database connection failed:\n{err}",
                parent=self.root
            )

            return

        # SCROLLBAR STYLE

        style = ttk.Style()

        style.configure(
            "Vertical.TScrollbar",
            width=20
        )

        style.configure(
            "Horizontal.TScrollbar",
            height=20
        )

        # ================= TOP IMAGE 1 =================

        img1 = Image.open(
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\stu1.png"
        )

        img1 = img1.resize(
            (455, 120),
            Image.Resampling.LANCZOS
        )

        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(
            self.root,
            image=self.photoimg1
        )

        f_lbl1.place(
            x=0,
            y=0,
            width=455,
            height=120
        )

        # ================= TOP IMAGE 2 =================

        img2 = Image.open(
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\st2.png"
        )

        img2 = img2.resize(
            (455, 120),
            Image.Resampling.LANCZOS
        )

        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl2 = Label(
            self.root,
            image=self.photoimg2
        )

        f_lbl2.place(
            x=455,
            y=0,
            width=455,
            height=120
        )

        # ================= TOP IMAGE 3 =================

        img3 = Image.open(
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\stu3.png"
        )

        img3 = img3.resize(
            (456, 120),
            Image.Resampling.LANCZOS
        )

        self.photoimg3 = ImageTk.PhotoImage(img3)

        f_lbl3 = Label(
            self.root,
            image=self.photoimg3
        )

        f_lbl3.place(
            x=910,
            y=0,
            width=456,
            height=120
        )

        # ================= TITLE =================

        title_lbl = Label(
            self.root,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Cambria", 28, "bold"),
            bg="white",
            fg="dark green"
        )

        title_lbl.place(
            x=0,
            y=120,
            width=1366,
            height=60
        )

        # ================= MAIN FRAME =================

        main_frame = Frame(
            self.root,
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        main_frame.place(
            x=5,
            y=185,
            width=1356,
            height=555
        )

        # ================= LEFT FRAME =================

        left_frame = LabelFrame(
            main_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Student Details",
            font=("times new roman", 12, "bold")
        )

        left_frame.place(
            x=10,
            y=5,
            width=665,
            height=540
        )

        # ================= LEFT IMAGE =================

        img_left = Image.open(
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\stuleft1.png"
        )

        img_left = img_left.resize(
            (650, 110),
            Image.Resampling.LANCZOS
        )

        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl_left = Label(
            left_frame,
            image=self.photoimg_left,
            bg="white"
        )

        f_lbl_left.place(
            x=5,
            y=0,
            width=650,
            height=110
        )

        # ================= CURRENT COURSE INFORMATION =================

        current_course_frame = LabelFrame(
            left_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Current course information",
            font=("times new roman", 12, "bold")
        )

        current_course_frame.place(
            x=5,
            y=110,
            width=650,
            height=90
        )

        # ================= DEPARTMENT =================

        department_label = Label(
            current_course_frame,
            text="Department",
            font=("times new roman", 12, "bold"),
            bg="white"
        )

        department_label.grid(
            row=0,
            column=0,
            padx=8,
            pady=4,
            sticky=W
        )

        department_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_dep,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
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
            pady=4,
            sticky=W
        )

        department_combo.current(0)

        # ================= COURSE =================

        course_label = Label(
            current_course_frame,
            text="Course",
            font=("times new roman", 12, "bold"),
            bg="white"
        )

        course_label.grid(
            row=0,
            column=2,
            padx=8,
            pady=4,
            sticky=W
        )

        course_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_course,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
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
            pady=4,
            sticky=W
        )

        course_combo.current(0)

        # ================= YEAR =================

        year_label = Label(
            current_course_frame,
            text="Year",
            font=("times new roman", 12, "bold"),
            bg="white"
        )

        year_label.grid(
            row=1,
            column=0,
            padx=8,
            pady=4,
            sticky=W
        )

        year_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_year,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
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
            pady=4,
            sticky=W
        )

        year_combo.current(0)

        # ================= SEMESTER =================

        semester_label = Label(
            current_course_frame,
            text="Semester",
            font=("times new roman", 12, "bold"),
            bg="white"
        )

        semester_label.grid(
            row=1,
            column=2,
            padx=8,
            pady=4,
            sticky=W
        )

        semester_combo = ttk.Combobox(
            current_course_frame,
            textvariable=self.var_semester,
            font=("times new roman", 12, "bold"),
            state="readonly",
            width=18
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
            pady=4,
            sticky=W
        )

        semester_combo.current(0)

        # ================= CLASS STUDENT INFORMATION =================

        class_student_frame = LabelFrame(
            left_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Class Student Information",
            font=("times new roman", 12, "bold")
        )

        class_student_frame.place(
            x=5,
            y=200,
            width=650,
            height=245
        )

        # ================= STUDENT ID =================

        student_id_label = Label(
            class_student_frame,
            text="Student ID:",
            font=("times new roman", 12, "bold"),
            bg="white"
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
            width=20,
            font=("times new roman", 12, "bold")
        )

        student_id_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= STUDENT NAME =================

        student_name_label = Label(
            class_student_frame,
            text="Student Name:",
            font=("times new roman", 12, "bold"),
            bg="white"
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
            width=20,
            font=("times new roman", 12, "bold")
        )

        student_name_entry.grid(
            row=0,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= CLASS DIVISION =================

        class_division_label = Label(
            class_student_frame,
            text="Class Division:",
            font=("times new roman", 12, "bold"),
            bg="white"
        )

        class_division_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky=W
        )

        class_division_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_div,
            width=20,
            font=("times new roman", 12, "bold")
        )

        class_division_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= ROLL NUMBER =================

        roll_number_label = Label(
            class_student_frame,
            text="Roll No:",
            font=("times new roman", 12, "bold"),
            bg="white"
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
            width=20,
            font=("times new roman", 12, "bold")
        )

        roll_number_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= GENDER =================

        gender_label = Label(
            class_student_frame,
            text="Gender:",
            font=("times new roman", 12, "bold"),
            bg="white"
        )

        gender_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky=W
        )

        gender_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_gender,
            width=20,
            font=("times new roman", 12, "bold")
        )

        gender_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= DOB =================

        dob_label = Label(
            class_student_frame,
            text="DOB:",
            font=("times new roman", 12, "bold"),
            bg="white"
        )

        dob_label.grid(
            row=2,
            column=2,
            padx=10,
            pady=5,
            sticky=W
        )

        dob_entry = ttk.Entry(
            class_student_frame,
            textvariable=self.var_dob,
            width=20,
            font=("times new roman", 12, "bold")
        )

        dob_entry.grid(
            row=2,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= EMAIL =================

        email_label = Label(
            class_student_frame,
            text="Email:",
            font=("times new roman", 12, "bold"),
            bg="white"
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
            width=20,
            font=("times new roman", 12, "bold")
        )

        email_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= PHONE NUMBER =================

        phone_number_label = Label(
            class_student_frame,
            text="Phone No:",
            font=("times new roman", 12, "bold"),
            bg="white"
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
            width=20,
            font=("times new roman", 12, "bold")
        )

        phone_number_entry.grid(
            row=3,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= ADDRESS =================

        address_label = Label(
            class_student_frame,
            text="Address:",
            font=("times new roman", 12, "bold"),
            bg="white"
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
            width=20,
            font=("times new roman", 12, "bold")
        )

        address_entry.grid(
            row=4,
            column=1,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= TEACHER NAME =================

        teacher_name_label = Label(
            class_student_frame,
            text="Teacher Name:",
            font=("times new roman", 12, "bold"),
            bg="white"
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
            width=20,
            font=("times new roman", 12, "bold")
        )

        teacher_name_entry.grid(
            row=4,
            column=3,
            padx=10,
            pady=5,
            sticky=W
        )

        # ================= RADIO BUTTONS =================

        radiobtn1 = ttk.Radiobutton(
            class_student_frame,
            text="Take Photo Sample",
            variable=self.var_radio,
            value="yes"
        )

        radiobtn1.grid(
            row=5,
            column=0,
            padx=10,
            pady=3,
            sticky=W
        )

        radiobtn2 = ttk.Radiobutton(
            class_student_frame,
            text="No Photo Sample",
            variable=self.var_radio,
            value="no"
        )

        radiobtn2.grid(
            row=5,
            column=1,
            padx=10,
            pady=3,
            sticky=W
        )

        # ================= BUTTON FRAME =================

        btn_frame = Frame(
            left_frame,
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        btn_frame.place(
            x=5,
            y=445,
            width=650,
            height=83
        )

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)

        # ================= SAVE =================

        save_btn = Button(
            btn_frame,
            text="Save",
            command=self.add_data,
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        save_btn.grid(
            row=0,
            column=0,
            padx=1,
            pady=1,
            sticky="ew"
        )

        # ================= UPDATE =================

        update_btn = Button(
            btn_frame,
            text="Update",
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        update_btn.grid(
            row=0,
            column=1,
            padx=1,
            pady=1,
            sticky="ew"
        )

        # ================= DELETE =================

        delete_btn = Button(
            btn_frame,
            text="Delete",
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        delete_btn.grid(
            row=0,
            column=2,
            padx=1,
            pady=1,
            sticky="ew"
        )

        # ================= RESET =================

        reset_btn = Button(
            btn_frame,
            text="Reset",
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        reset_btn.grid(
            row=0,
            column=3,
            padx=1,
            pady=1,
            sticky="ew"
        )

        # ================= TAKE PHOTO SAMPLE =================

        take_photo_btn = Button(
            btn_frame,
            text="Take Photo Sample",
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        take_photo_btn.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=1,
            pady=1,
            sticky="ew"
        )

        # ================= UPDATE PHOTO SAMPLE =================

        update_photo_btn = Button(
            btn_frame,
            text="Update Photo Sample",
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        update_photo_btn.grid(
            row=1,
            column=2,
            columnspan=2,
            padx=1,
            pady=1,
            sticky="ew"
        )

        # ================= RIGHT FRAME =================

        right_frame = LabelFrame(
            main_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Student Details",
            font=("times new roman", 12, "bold")
        )

        right_frame.place(
            x=685,
            y=5,
            width=660,
            height=540
        )

        # ================= RIGHT IMAGE =================

        img_right = Image.open(
            r"C:\Users\DELL\OneDrive\Desktop\Face Recognition\College_images\stuleft1.png"
        )

        img_right = img_right.resize(
            (650, 110),
            Image.Resampling.LANCZOS
        )

        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl_right = Label(
            right_frame,
            image=self.photoimg_right,
            bg="white"
        )

        f_lbl_right.place(
            x=5,
            y=0,
            width=650,
            height=110
        )

        # ================= SEARCH SYSTEM =================

        Search_frame = LabelFrame(
            right_frame,
            bd=2,
            bg="white",
            relief=RIDGE,
            text="Search System",
            font=("times new roman", 12, "bold")
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
            font=("times new roman", 12, "bold"),
            bg="red",
            fg="white"
        )

        search_label_.grid(
            row=0,
            column=0,
            padx=8,
            pady=10,
            sticky=W
        )

        search_combo = ttk.Combobox(
            Search_frame,
            font=("times new roman", 11, "bold"),
            state="readonly",
            width=16
        )

        search_combo["values"] = (
            "Select",
            "Name",
            "Roll Number",
            "Phone Number",
            "ID"
        )

        search_combo.current(0)

        search_combo.grid(
            row=0,
            column=1,
            padx=4,
            pady=10
        )

        search_entry = ttk.Entry(
            Search_frame,
            width=18,
            font=("times new roman", 11, "bold")
        )

        search_entry.grid(
            row=0,
            column=2,
            padx=4,
            pady=10
        )

        # ================= SEARCH BUTTON =================

        search_btn = Button(
            Search_frame,
            text="Search",
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        search_btn.grid(
            row=0,
            column=3,
            padx=4,
            pady=8
        )

        # ================= SHOW ALL BUTTON =================

        showAll_btn = Button(
            Search_frame,
            text="Show All",
            font=("times new roman", 11, "bold"),
            bg="blue",
            fg="white",
            cursor="hand2"
        )

        showAll_btn.grid(
            row=0,
            column=4,
            padx=4,
            pady=8
        )

        # ================= TABLE FRAME =================

        Table_frame = Frame(
            right_frame,
            bd=2,
            bg="white",
            relief=RIDGE
        )

        Table_frame.place(
            x=5,
            y=175,
            width=650,
            height=350
        )

        # ================= SCROLLBAR =================

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

        # ================= TABLE =================

        self.student_table = ttk.Treeview(
            Table_frame,
            columns=(
                "department",
                "name",
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

        # ================= HEADINGS =================

        self.student_table.heading(
            "department",
            text="Department"
        )

        self.student_table.heading(
            "name",
            text="Name"
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

        # ================= COLUMNS =================

        self.student_table.column(
            "department",
            width=150,
            minwidth=150
        )

        self.student_table.column(
            "name",
            width=150,
            minwidth=150
        )

        self.student_table.column(
            "roll",
            width=100,
            minwidth=100
        )

        self.student_table.column(
            "gender",
            width=100,
            minwidth=100
        )

        self.student_table.column(
            "dob",
            width=100,
            minwidth=100
        )

        self.student_table.column(
            "email",
            width=180,
            minwidth=180
        )

        self.student_table.column(
            "phone",
            width=120,
            minwidth=120
        )

        self.student_table.column(
            "address",
            width=180,
            minwidth=180
        )

        self.student_table.column(
            "teacher",
            width=150,
            minwidth=150
        )

        self.student_table.column(
            "id",
            width=100,
            minwidth=100
        )

        self.student_table.column(
            "course",
            width=100,
            minwidth=100
        )

        self.student_table.column(
            "year",
            width=100,
            minwidth=100
        )

        self.student_table.column(
            "photo",
            width=100,
            minwidth=100
        )

        self.student_table.column(
            "semester",
            width=100,
            minwidth=100
        )

        # ================= TABLE + SCROLLBARS =================

        Table_frame.grid_rowconfigure(
            0,
            weight=1
        )

        Table_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.student_table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scroll_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

    # ================= ADD DATA =================

    def add_data(self):

        if (
            self.var_dep.get() == "Select Department"
            or self.var_course.get() == "Select Course"
            or self.var_year.get() == "Select Year"
            or self.var_semester.get() == "Select Semester"
            or self.var_std_name.get() == ""
            or self.var_std_id.get() == ""
        ):

            messagebox.showerror(
                "Error",
                "All fields are required",
                parent=self.root
            )

        else:

            try:

                self.my_cursor.execute(
                    """
                    INSERT INTO student
                    (
                        student_id,
                        name,
                        department,
                        course,
                        year,
                        semester,
                        division,
                        roll_no,
                        gender,
                        dob,
                        email,
                        phone,
                        address,
                        photo_sample,
                        teacher
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        self.var_std_id.get(),
                        self.var_std_name.get(),
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_div.get(),
                        self.var_roll.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_radio.get(),
                        self.var_teacher.get()
                    )
                )

                self.conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Student details have been added successfully",
                    parent=self.root
                )

            except mysql.connector.Error as e:

                messagebox.showerror(
                    "Database Error",
                    f"Due To: {str(e)}",
                    parent=self.root
                )

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"Due To: {str(e)}",
                    parent=self.root
                )


# ================= MAIN =================

if __name__ == "__main__":

    root = Tk()

    obj = Student(root)

    root.mainloop()