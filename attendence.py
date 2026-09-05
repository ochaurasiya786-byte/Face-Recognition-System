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

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # TITLE
        Label(
            root, text="ATTENDANCE MANAGEMENT SYSTEM",
            font=("times new roman", 35, "bold"),
            bg="#020D25", fg="#00E5FF"
        ).place(x=0, y=0, width=1366, height=80)

        # LEFT FRAME
        left_frame = LabelFrame(
            root, text="Attendance Details",
            font=("times new roman", 15, "bold"),
            bd=2, relief=RIDGE, bg="white"
        )
        left_frame.place(x=15, y=90, width=650, height=640)

        # LEFT IMAGE
        img = Image.open(os.path.join(base_dir, "College_images", "leftattend.png"))
        img = img.resize((640, 200), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img)

        Label(left_frame, image=self.photoimg_left, bd=0).place(
            x=4, y=4, width=640, height=200
        )

        # INSIDE FRAME
        inside = Frame(left_frame, bd=2, relief=RIDGE, bg="white")
        inside.place(x=4, y=210, width=640, height=370)

        # ENTRY HELPER
        def make_entry(label, x1, y1, x2, y2, width=155):
            Label(
                inside, text=label,
                font=("times new roman", 12, "bold"),
                bg="white"
            ).place(x=x1, y=y1)
            entry = Entry(
                inside,
                font=("times new roman", 12, "bold"),
                bg="white"
            )
            entry.place(x=x2, y=y2, width=width)
            return entry

        # ATTENDANCE DETAILS
        self.attendance_id_entry = make_entry(
            "AttendanceId:", 10, 10, 120, 10
        )
        self.name_entry = make_entry(
            "Name:", 30, 45, 120, 45
        )
        self.time_entry = make_entry(
            "Time:", 30, 80, 120, 80
        )
        self.roll_entry = make_entry(
            "Roll:", 367, 10, 422, 10
        )
        self.department_entry = make_entry(
            "Department:", 337, 45, 437, 45, 140
        )
        self.date_entry = make_entry(
            "Date:", 367, 80, 422, 80
        )

        # ATTENDANCE STATUS
        Label(
            inside, text="Attendance Status:",
            font=("times new roman", 12, "bold"),
            bg="white"
        ).place(x=5, y=115)

        self.status_combo = ttk.Combobox(
            inside,
            font=("times new roman", 11, "bold"),
            state="readonly",
            values=("Status", "Present", "Absent")
        )
        self.status_combo.current(0)
        self.status_combo.place(x=145, y=115, width=130)

        # BUTTON FRAME
        btn_frame = Frame(inside, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=235, width=635, height=45)

        buttons = [
            ("Import csv", self.importCsv, 0, 150),
            ("Export csv", self.exportCsv, 150, 160),
            ("Update", self.updateData, 305, 160),
            ("Reset", self.resetData, 465, 165)
        ]

        for text, command, x, width in buttons:
            Button(
                btn_frame,
                text=text,
                command=command,
                font=("times new roman", 12, "bold"),
                bg="blue",
                fg="white",
                cursor="hand2",
                bd=1
            ).place(x=x, y=0, width=width, height=43)

        # MIDDLE SPACE
        Frame(root, bg="white").place(
            x=690, y=90, width=15, height=640
        )

        # RIGHT FRAME
        right_frame = LabelFrame(
            root,
            text="Student Information",
            font=("times new roman", 15, "bold"),
            bd=2,
            relief=RIDGE,
            bg="white"
        )
        right_frame.place(x=680, y=90, width=670, height=640)

        # TABLE FRAME
        table_frame = Frame(
            right_frame, bd=2, relief=RIDGE, bg="white"
        )
        table_frame.place(x=5, y=5, width=655, height=600)

        # TABLE STYLE
        style = ttk.Style()
        style.configure(
            "Treeview.Heading",
            font=("times new roman", 11, "bold")
        )

        # SCROLLBARS
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        # TABLE
        columns = (
            "id", "roll", "name", "department",
            "time", "date", "attendance"
        )

        self.AttendanceReportTable = ttk.Treeview(
            table_frame,
            columns=columns,
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        headings = {
            "id": "Attendence ID",
            "roll": "Roll",
            "name": "Name",
            "department": "Department",
            "time": "Time",
            "date": "Date",
            "attendance": "Attendence"
        }

        widths = {
            "id": 120,
            "roll": 100,
            "name": 150,
            "department": 140,
            "time": 100,
            "date": 100,
            "attendance": 100
        }

        for col in columns:
            self.AttendanceReportTable.heading(
                col, text=headings[col]
            )
            self.AttendanceReportTable.column(
                col, width=widths[col]
            )

        self.AttendanceReportTable["show"] = "headings"

        scroll_x.config(
            command=self.AttendanceReportTable.xview
        )
        scroll_y.config(
            command=self.AttendanceReportTable.yview
        )

        self.AttendanceReportTable.place(
            x=0, y=0, width=635, height=580
        )

        scroll_y.place(
            x=635, y=0, width=18, height=580
        )

        scroll_x.place(
            x=0, y=580, width=635, height=18
        )

        # TABLE CLICK
        self.AttendanceReportTable.bind(
            "<ButtonRelease-1>", self.get_cursor
        )

    # GET SELECTED ROW
    def get_cursor(self, event=""):
        selected = self.AttendanceReportTable.focus()
        if not selected:
            return

        data = self.AttendanceReportTable.item(
            selected, "values"
        )

        if len(data) < 7:
            return

        entries = [
            self.attendance_id_entry,
            self.roll_entry,
            self.name_entry,
            self.department_entry,
            self.time_entry,
            self.date_entry
        ]

        for entry, value in zip(entries, data[:6]):
            entry.delete(0, END)
            entry.insert(0, value)

        self.status_combo.set(
            data[6] if data[6] in ("Present", "Absent") else "Status"
        )

    # FETCH DATA
    def fetchData(self, rows):
        self.AttendanceReportTable.delete(
            *self.AttendanceReportTable.get_children()
        )

        for row in rows:
            if len(row) == 6:
                row = [
                    row[0], "", row[1], row[2],
                    row[3], row[4], row[5]
                ]

            elif len(row) >= 7:
                row = row[:7]

            else:
                continue

            self.AttendanceReportTable.insert(
                "", END, values=row
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
            mydata = []

            with open(
                fln, newline="", encoding="utf-8"
            ) as myfile:
                for row in csv.reader(myfile):
                    if row:
                        mydata.append(row)

            self.fetchData(mydata)

            messagebox.showinfo(
                "Success",
                "CSV file imported successfully!",
                parent=self.root
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error importing CSV:\n{e}",
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
                file, "w", newline="", encoding="utf-8"
            ) as myfile:
                csv.writer(myfile).writerows(mydata)

            messagebox.showinfo(
                "Success",
                "CSV file exported successfully!",
                parent=self.root
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error exporting CSV:\n{e}",
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

        data = [
            self.attendance_id_entry.get(),
            self.roll_entry.get(),
            self.name_entry.get(),
            self.department_entry.get(),
            self.time_entry.get(),
            self.date_entry.get(),
            self.status_combo.get()
        ]

        if "" in data or data[6] == "Status":
            messagebox.showerror(
                "Error",
                "Please fill all fields!",
                parent=self.root
            )
            return

        self.AttendanceReportTable.item(
            selected, values=data
        )

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
            entry.delete(0, END)

        self.status_combo.current(0)


# MAIN
if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()