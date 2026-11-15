from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import csv

mydata = []

class Attendance:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Recognition System")
        self.root.geometry("1366x750+0+0")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # TITLE

        title = Label(
            self.root,
            text="ATTENDANCE MANAGEMENT SYSTEM",
            font=("times new roman", 35, "bold"),
            bg="#020D25",
            fg="#00E5FF",
            bd=2,
            relief=RAISED
        )

        title.place(
            x=0,
            y=0,
            width=1366,
            height=80
        )

        # TITLE HOVER

        def title_enter(event):
            title.config(
                bg="#06183d",
                fg="#39efff",
                relief=RAISED,
                bd=3
            )

        def title_leave(event):
            title.config(
                bg="#020D25",
                fg="#00E5FF",
                relief=RAISED,
                bd=2
            )

        title.bind("<Enter>", title_enter)
        title.bind("<Leave>", title_leave)

        # LEFT FRAME

        left_frame = LabelFrame(
            self.root,
            text="Attendance Details",
            font=("times new roman", 15, "bold"),
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        left_frame.place(
            x=15,
            y=90,
            width=650,
            height=640
        )

        # LEFT IMAGE

        try:
            img = Image.open(
                os.path.join(
                    self.base_dir,
                    "College_images",
                    "leftattend.png"
                )
            )

            img = img.resize(
                (640, 200),
                Image.Resampling.LANCZOS
            )

            self.photoimg_left = ImageTk.PhotoImage(img)

            left_image = Label(
                left_frame,
                image=self.photoimg_left,
                bd=1,
                relief=RAISED
            )

            left_image.place(
                x=4,
                y=4,
                width=640,
                height=200
            )

        except Exception as e:
            messagebox.showerror(
                "Image Error",
                f"leftattend.png not found!\n\n{e}",
                parent=self.root
            )

        # INSIDE FRAME

        inside = Frame(
            left_frame,
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        inside.place(
            x=4,
            y=210,
            width=640,
            height=370
        )

        # ENTRY HELPER

        def make_entry(label, x1, y1, x2, y2, width=155):

            Label(
                inside,
                text=label,
                font=("times new roman", 12, "bold"),
                bg="white"
            ).place(
                x=x1,
                y=y1
            )

            entry = Entry(
                inside,
                font=("times new roman", 12, "bold"),
                bg="white",
                bd=2,
                relief=SOLID,
                highlightthickness=1,
                highlightbackground="#c7c7c7",
                highlightcolor="#087f23"
            )

            entry.place(
                x=x2,
                y=y2,
                width=width
            )

            entry.bind(
                "<FocusIn>",
                lambda e: entry.config(
                    highlightbackground="#087f23",
                    highlightcolor="#087f23"
                )
            )

            entry.bind(
                "<FocusOut>",
                lambda e: entry.config(
                    highlightbackground="#c7c7c7",
                    highlightcolor="#087f23"
                )
            )

            return entry

        # ATTENDANCE DETAILS

        self.attendance_id_entry = make_entry(
            "Student ID:",
            10,
            10,
            120,
            10
        )

        self.name_entry = make_entry(
            "Name:",
            30,
            45,
            120,
            45
        )

        self.time_entry = make_entry(
            "Time:",
            30,
            80,
            120,
            80
        )

        self.roll_entry = make_entry(
            "Roll:",
            367,
            10,
            422,
            10
        )

        self.department_entry = make_entry(
            "Department:",
            337,
            45,
            437,
            45,
            140
        )

        self.date_entry = make_entry(
            "Date:",
            367,
            80,
            422,
            80
        )

        # ATTENDANCE STATUS

        Label(
            inside,
            text="Attendance Status:",
            font=("times new roman", 12, "bold"),
            bg="white"
        ).place(
            x=5,
            y=115
        )

        self.status_combo = ttk.Combobox(
            inside,
            font=("times new roman", 11, "bold"),
            state="readonly",
            values=(
                "Status",
                "Present",
                "Absent"
            )
        )

        self.status_combo.current(0)

        self.status_combo.place(
            x=145,
            y=115,
            width=130
        )

        # BUTTON FRAME

        btn_frame = Frame(
            inside,
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        btn_frame.place(
            x=0,
            y=235,
            width=635,
            height=45
        )

        # BUTTONS

        buttons = [
            ("Import csv", self.importCsv, 0, 150),
            ("Export csv", self.exportCsv, 150, 160),
            ("Update", self.updateData, 305, 160),
            ("Reset", self.resetData, 465, 165)
        ]

        for text, command, x, width in buttons:

            button = Button(
                btn_frame,
                text=text,
                command=command,
                font=("times new roman", 12, "bold"),
                bg="blue",
                fg="white",
                activebackground="#0056d6",
                activeforeground="white",
                cursor="hand2",
                bd=2,
                relief=RAISED
            )

            button.place(
                x=x,
                y=0,
                width=width,
                height=43
            )

            button.bind(
                "<Enter>",
                lambda e, b=button: b.config(
                    bg="#006eff",
                    bd=3
                )
            )

            button.bind(
                "<Leave>",
                lambda e, b=button: b.config(
                    bg="blue",
                    bd=2
                )
            )

            button.bind(
                "<ButtonPress-1>",
                lambda e, b=button: b.config(
                    bg="#003d99",
                    relief=SUNKEN,
                    bd=4
                )
            )

            button.bind(
                "<ButtonRelease-1>",
                lambda e, b=button: b.config(
                    bg="#006eff",
                    relief=RAISED,
                    bd=3
                )
            )

        # RIGHT FRAME

        right_frame = LabelFrame(
            self.root,
            text="Student Information",
            font=("times new roman", 15, "bold"),
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        right_frame.place(
            x=680,
            y=90,
            width=670,
            height=640
        )

        # TABLE FRAME

        table_frame = Frame(
            right_frame,
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        table_frame.place(
            x=5,
            y=5,
            width=655,
            height=600
        )

        # TABLE STYLE

        style = ttk.Style()

        style.configure(
            "Treeview.Heading",
            font=("times new roman", 10, "bold")
        )

        style.configure(
            "Treeview",
            font=("times new roman", 9),
            rowheight=28
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#0078d7")
            ],
            foreground=[
                ("selected", "white")
            ]
        )

        # SCROLLBARS

        scroll_x = ttk.Scrollbar(
            table_frame,
            orient=HORIZONTAL
        )

        scroll_y = ttk.Scrollbar(
            table_frame,
            orient=VERTICAL
        )

        # TABLE

        columns = (
            "id",
            "roll",
            "name",
            "department",
            "time",
            "date",
            "latitude",
            "longitude",
            "distance",
            "face_status",
            "location_status",
            "time_status",
            "attendance"
        )

        self.AttendanceReportTable = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        # HEADINGS

        headings = {
            "id": "Student ID",
            "roll": "Roll",
            "name": "Name",
            "department": "Department",
            "time": "Time",
            "date": "Date",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "distance": "Distance",
            "face_status": "Face Status",
            "location_status": "Location Status",
            "time_status": "Time Status",
            "attendance": "Attendance"
        }

        # COLUMN WIDTH

        widths = {
            "id": 80,
            "roll": 60,
            "name": 150,
            "department": 140,
            "time": 85,
            "date": 90,
            "latitude": 125,
            "longitude": 125,
            "distance": 100,
            "face_status": 100,
            "location_status": 120,
            "time_status": 100,
            "attendance": 100
        }

        # SET COLUMNS

        for col in columns:

            self.AttendanceReportTable.heading(
                col,
                text=headings[col]
            )

            self.AttendanceReportTable.column(
                col,
                width=widths[col],
                minwidth=widths[col],
                stretch=False,
                anchor="center"
            )

        # SCROLLBAR

        scroll_x.config(
            command=self.AttendanceReportTable.xview
        )

        scroll_y.config(
            command=self.AttendanceReportTable.yview
        )

        self.AttendanceReportTable.place(
            x=0,
            y=0,
            width=635,
            height=580
        )

        scroll_y.place(
            x=635,
            y=0,
            width=18,
            height=580
        )

        scroll_x.place(
            x=0,
            y=580,
            width=635,
            height=18
        )

        # ROW HOVER

        self.hovered_item = None

        self.AttendanceReportTable.tag_configure(
            "hover",
            background="#dff6ff",
            foreground="#020D25",
            font=("times new roman", 9, "bold")
        )

        def row_hover(event):

            item = self.AttendanceReportTable.identify_row(
                event.y
            )

            if self.hovered_item and self.hovered_item != item:

                try:
                    self.AttendanceReportTable.item(
                        self.hovered_item,
                        tags=()
                    )
                except:
                    pass

            if item:

                self.AttendanceReportTable.item(
                    item,
                    tags=("hover",)
                )

                self.hovered_item = item

            else:
                self.hovered_item = None

        def row_leave(event):

            if self.hovered_item:

                try:
                    self.AttendanceReportTable.item(
                        self.hovered_item,
                        tags=()
                    )
                except:
                    pass

                self.hovered_item = None

        self.AttendanceReportTable.bind(
            "<Motion>",
            row_hover
        )

        self.AttendanceReportTable.bind(
            "<Leave>",
            row_leave
        )

        self.AttendanceReportTable.bind(
            "<ButtonRelease-1>",
            self.get_cursor
        )

    # GET SELECTED ROW

    def get_cursor(self, event=""):

        selected = self.AttendanceReportTable.focus()

        if not selected:
            return

        data = self.AttendanceReportTable.item(
            selected,
            "values"
        )

        if len(data) != 13:
            return

        # FIRST 6 COLUMNS TO LEFT FORM

        entries = [
            self.attendance_id_entry,
            self.roll_entry,
            self.name_entry,
            self.department_entry,
            self.time_entry,
            self.date_entry
        ]

        for entry, value in zip(
            entries,
            data[:6]
        ):

            entry.delete(
                0,
                END
            )

            entry.insert(
                0,
                value
            )

        # ATTENDANCE

        attendance_value = str(
            data[12]
        ).strip()

        if attendance_value in (
            "Present",
            "Absent"
        ):

            self.status_combo.set(
                attendance_value
            )

        else:
            self.status_combo.current(0)

    # NORMALIZE ROW

    def normalize_row(self, row):

        row = [
            str(value).strip()
            for value in row
        ]

        # 13 COLUMN FORMAT

        if len(row) >= 13:
            return row[:13]

        # 7 COLUMN OLD FORMAT

        if len(row) == 7:

            return [
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                "",
                "",
                "",
                "",
                "",
                "",
                row[6]
            ]

        # 6 COLUMN OLD FORMAT

        if len(row) == 6:

            return [
                row[0],
                "",
                row[1],
                row[2],
                row[3],
                row[4],
                "",
                "",
                "",
                "",
                "",
                "",
                row[5]
            ]

        return None

    # FETCH DATA

    def fetchData(self, rows):

        self.AttendanceReportTable.delete(
            *self.AttendanceReportTable.get_children()
        )

        normalized_rows = []

        for row in rows:

            if not row:
                continue

            # REMOVE BOM FROM FIRST VALUE

            if row:

                row[0] = str(
                    row[0]
                ).replace(
                    "\ufeff",
                    ""
                ).strip()

            # SKIP HEADER

            first_value = str(
                row[0]
            ).strip().lower()

            if first_value in (
                "student_id",
                "student id",
                "attendanceid",
                "attendance id",
                "attendence id",
                "id"
            ):
                continue

            # NORMALIZE

            normalized_row = self.normalize_row(
                row
            )

            if normalized_row is None:
                continue

            # ALWAYS EXACTLY 13 COLUMNS

            if len(normalized_row) < 13:

                normalized_row += [
                    ""
                ] * (
                    13 - len(normalized_row)
                )

            normalized_row = normalized_row[:13]

            normalized_rows.append(
                normalized_row
            )

        # STORE NORMALIZED DATA

        global mydata

        mydata = normalized_rows

        # DISPLAY

        for row in normalized_rows:

            self.AttendanceReportTable.insert(
                "",
                END,
                values=row,
                tags=()
            )

    # IMPORT CSV

    def importCsv(self):

        global mydata

        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open CSV",
            filetypes=(
                ("CSV File", "*.csv"),
                ("ALL File", "*.*")
            ),
            parent=self.root
        )

        if not fln:
            return

        try:

            rows = []

            with open(
                fln,
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as myfile:

                reader = csv.reader(
                    myfile
                )

                for row in reader:

                    if row:
                        rows.append(row)

            self.fetchData(
                rows
            )

            messagebox.showinfo(
                "Success",
                "CSV file imported successfully!",
                parent=self.root
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Error importing CSV:\n\n{e}",
                parent=self.root
            )

    # EXPORT CSV

    def exportCsv(self):

        global mydata

        if not mydata:

            messagebox.showerror(
                "Error",
                "No data available to export!",
                parent=self.root
            )

            return

        file = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Save CSV",
            defaultextension=".csv",
            filetypes=(
                ("CSV File", "*.csv"),
                ("ALL File", "*.*")
            ),
            parent=self.root
        )

        if not file:
            return

        try:

            with open(
                file,
                "w",
                newline="",
                encoding="utf-8"
            ) as myfile:

                writer = csv.writer(
                    myfile
                )

                # PROPER 13 COLUMN HEADER

                writer.writerow([
                    "Student_ID",
                    "Roll",
                    "Name",
                    "Department",
                    "Time",
                    "Date",
                    "Latitude",
                    "Longitude",
                    "Distance",
                    "Face_Status",
                    "Location_Status",
                    "Time_Status",
                    "Attendance_Status"
                ])

                for row in mydata:

                    writer.writerow(
                        row
                    )

            messagebox.showinfo(
                "Success",
                "Attendance CSV exported successfully!",
                parent=self.root
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Error exporting CSV:\n\n{e}",
                parent=self.root
            )

    # UPDATE

    def updateData(self):

        selected = self.AttendanceReportTable.focus()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a record first!",
                parent=self.root
            )

            return

        old_data = list(
            self.AttendanceReportTable.item(
                selected,
                "values"
            )
        )

        if len(old_data) != 13:

            messagebox.showerror(
                "Error",
                "Invalid attendance record.",
                parent=self.root
            )

            return

        new_data = old_data[:]

        # UPDATE BASIC INFORMATION ONLY

        new_data[0] = self.attendance_id_entry.get()
        new_data[1] = self.roll_entry.get()
        new_data[2] = self.name_entry.get()
        new_data[3] = self.department_entry.get()
        new_data[4] = self.time_entry.get()
        new_data[5] = self.date_entry.get()
        new_data[12] = self.status_combo.get()

        # VALIDATION

        if (
            "" in new_data[:6]
            or
            new_data[12] == "Status"
        ):

            messagebox.showerror(
                "Error",
                "Please fill all fields!",
                parent=self.root
            )

            return

        # UPDATE TABLE

        self.AttendanceReportTable.item(
            selected,
            values=new_data
        )

        # UPDATE mydata

        try:

            item_index = (
                self.AttendanceReportTable.index(
                    selected
                )
            )

            if (
                0 <= item_index < len(mydata)
            ):

                mydata[item_index] = new_data

        except:

            pass

        messagebox.showinfo(
            "Success",
            "Attendance data updated successfully!",
            parent=self.root
        )

    # RESET

    def resetData(self):

        global mydata

        mydata = []

        self.AttendanceReportTable.delete(
            *self.AttendanceReportTable.get_children()
        )

        for entry in (
            self.attendance_id_entry,
            self.roll_entry,
            self.name_entry,
            self.department_entry,
            self.time_entry,
            self.date_entry
        ):

            entry.delete(
                0,
                END
            )

        self.status_combo.current(0)


# MAIN

if __name__ == "__main__":

    root = Tk()

    obj = Attendance(
        root
    )

    root.mainloop()