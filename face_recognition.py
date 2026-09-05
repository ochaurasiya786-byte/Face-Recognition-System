from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
import cv2
import os
import csv


class Face_Recognition:

    def __init__(self, root):

        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")
        self.root.resizable(False, False)

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # TITLE
        title_lbl = Label(
            self.root,
            text="FACE RECOGNITION",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="darkgreen"
        )

        title_lbl.place(
            x=0,
            y=0,
            width=1366,
            height=70
        )

        # TOP IMAGE
        top_image_path = os.path.join(
            self.base_dir,
            "College_images",
            "Detector1.png"
        )

        try:
            img_top1 = Image.open(top_image_path)

            img_top1 = img_top1.crop(
                (
                    10,
                    30,
                    img_top1.width,
                    img_top1.height
                )
            )

            img_top1 = img_top1.resize(
                (620, 585),
                Image.Resampling.LANCZOS
            )

            self.photoimg_top1 = ImageTk.PhotoImage(img_top1)

            f_lbl1 = Label(
                self.root,
                image=self.photoimg_top1,
                bd=0
            )

            f_lbl1.place(
                x=0,
                y=70,
                width=620,
                height=585
            )

        except Exception as e:
            messagebox.showerror(
                "Image Error",
                f"Detector1.png not found!\n\n{e}",
                parent=self.root
            )

        # RIGHT IMAGE
        right_image_path = os.path.join(
            self.base_dir,
            "College_images",
            "Dec1.png"
        )

        try:
            img_top2 = Image.open(right_image_path)

            img_top2 = img_top2.resize(
                (746, 585),
                Image.Resampling.LANCZOS
            )

            self.photoimg_top2 = ImageTk.PhotoImage(img_top2)

            f_lbl2 = Label(
                self.root,
                image=self.photoimg_top2,
                bd=0
            )

            f_lbl2.place(
                x=620,
                y=70,
                width=746,
                height=585
            )

        except Exception as e:
            messagebox.showerror(
                "Image Error",
                f"Dec1.png not found!\n\n{e}",
                parent=self.root
            )

        # FACE RECOGNITION BUTTON
        b1 = Button(
            self.root,
            text="Face Recognition",
            cursor="hand2",
            font=("times new roman", 18, "bold"),
            bg="dark green",
            fg="white",
            command=self.face_recog
        )

        b1.place(
            x=895,
            y=590,
            width=200,
            height=40
        )

    # MARK ATTENDANCE
    def mark_attendance(
        self,
        student_id,
        roll,
        name,
        department
    ):

        file_name = os.path.join(
            self.base_dir,
            "attendence.csv"
        )

        now = datetime.now()

        today_date = now.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M:%S")

        # CREATE CSV IF NOT EXISTS
        if not os.path.exists(file_name):

            try:
                with open(
                    file_name,
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as f:

                    writer = csv.writer(f)

                    writer.writerow([
                        "ID",
                        "Roll",
                        "Name",
                        "Department",
                        "Time",
                        "Date",
                        "Attendance"
                    ])

            except Exception as e:

                messagebox.showerror(
                    "CSV Error",
                    f"Could not create attendance file.\n\n{e}",
                    parent=self.root
                )

                return False

        # CHECK TODAY'S ATTENDANCE
        try:

            with open(
                file_name,
                "r",
                newline="",
                encoding="utf-8"
            ) as f:

                reader = csv.reader(f)

                for row in reader:

                    if not row:
                        continue

                    # NEW FORMAT - 7 COLUMNS
                    if len(row) >= 7:

                        old_id = str(row[0]).strip()
                        old_date = str(row[5]).strip()

                        if (
                            old_id == str(student_id).strip()
                            and old_date == today_date
                        ):

                            old_time = str(row[4]).strip()

                            # ALREADY MARKED MESSAGE
                            messagebox.showwarning(
                                "Already Marked",
                                f"⚠️ You are Already Marked Present!\n\n"
                                f"Name: {name}\n"
                                f"Roll No: {roll}\n"
                                f"Department: {department}\n"
                                f"Date: {today_date}\n"
                                f"Time: {old_time}\n\n"
                                f"Your attendance has already been "
                                f"marked for today.",
                                parent=self.root
                            )

                            return False

                    # OLD FORMAT - 6 COLUMNS
                    elif len(row) >= 6:

                        old_id = str(row[0]).strip()
                        old_date = str(row[4]).strip()

                        if (
                            old_id == str(student_id).strip()
                            and old_date == today_date
                        ):

                            old_time = str(row[3]).strip()

                            # ALREADY MARKED MESSAGE
                            messagebox.showwarning(
                                "Already Marked",
                                f"⚠️ You are Already Marked Present!\n\n"
                                f"Name: {name}\n"
                                f"Roll No: {roll}\n"
                                f"Department: {department}\n"
                                f"Date: {today_date}\n"
                                f"Time: {old_time}\n\n"
                                f"Your attendance has already been "
                                f"marked for today.",
                                parent=self.root
                            )

                            return False

        except Exception as e:

            messagebox.showerror(
                "CSV Error",
                f"Could not read attendance file.\n\n{e}",
                parent=self.root
            )

            return False

        # ADD NEW ATTENDANCE
        try:

            with open(
                file_name,
                "a",
                newline="",
                encoding="utf-8"
            ) as f:

                writer = csv.writer(f)

                writer.writerow([
                    student_id,
                    roll,
                    name,
                    department,
                    current_time,
                    today_date,
                    "Present"
                ])

            # SUCCESS MESSAGE
            messagebox.showinfo(
                "Attendance Marked",
                f"✅ Attendance Marked Successfully!\n\n"
                f"Name: {name}\n"
                f"Roll No: {roll}\n"
                f"Department: {department}\n"
                f"Date: {today_date}\n"
                f"Time: {current_time}\n"
                f"Status: Present",
                parent=self.root
            )

            return True

        except Exception as e:

            messagebox.showerror(
                "CSV Error",
                f"Could not save attendance.\n\n{e}",
                parent=self.root
            )

            return None

    # FACE RECOGNITION
    def face_recog(self):

        # HAAR CASCADE
        cascade_path = os.path.join(
            self.base_dir,
            "haarcascade_frontalface_default.xml"
        )

        if not os.path.exists(cascade_path):

            messagebox.showerror(
                "Error",
                "haarcascade_frontalface_default.xml file not found!",
                parent=self.root
            )

            return

        face_cascade = cv2.CascadeClassifier(
            cascade_path
        )

        if face_cascade.empty():

            messagebox.showerror(
                "Error",
                "Unable to load Haar Cascade.",
                parent=self.root
            )

            return

        # LBPH FACE RECOGNIZER
        try:

            clf = cv2.face.LBPHFaceRecognizer_create()

        except AttributeError:

            messagebox.showerror(
                "Error",
                "cv2.face is not available.\n\n"
                "Please install opencv-contrib-python.",
                parent=self.root
            )

            return

        # CLASSIFIER
        classifier_path = os.path.join(
            self.base_dir,
            "classifier.xml"
        )

        if not os.path.exists(classifier_path):

            messagebox.showerror(
                "Error",
                "classifier.xml file not found!\n\n"
                "First train the dataset.",
                parent=self.root
            )

            return

        try:

            clf.read(classifier_path)

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load classifier.xml\n\n{e}",
                parent=self.root
            )

            return

        # DATABASE
        student_data = {}

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Omkar@7518",
                database="student"
            )

            cursor = conn.cursor()

            # GET REQUIRED STUDENT DATA
            cursor.execute("""
                SELECT
                    Student_ID,
                    Roll,
                    Student_Name,
                    Dep
                FROM student
            """)

            results = cursor.fetchall()

            # STORE STUDENT DATA
            for row in results:

                try:

                    student_id = int(row[0])

                    roll = str(row[1]).strip()
                    name = str(row[2]).strip()
                    department = str(row[3]).strip()

                    student_data[student_id] = {
                        "roll": roll,
                        "name": name,
                        "department": department
                    }

                except Exception:

                    continue

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err),
                parent=self.root
            )

            return

        # CHECK DATABASE DATA
        if not student_data:

            messagebox.showwarning(
                "Warning",
                "No student data found in database.",
                parent=self.root
            )

            return

        # CAMERA
        video_cap = cv2.VideoCapture(0)

        if not video_cap.isOpened():

            messagebox.showerror(
                "Camera Error",
                "Camera could not be opened.",
                parent=self.root
            )

            return

        # CAMERA WINDOW
        window_name = "Welcome to Face Recognition"

        cv2.namedWindow(
            window_name,
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            window_name,
            535,
            425
        )

        cv2.moveWindow(
            window_name,
            315,
            150
        )

        # FACE RECOGNITION LOOP
        attendance_processed = False
        recognized_id = None
        recognized_frames = 0

        while True:

            ret, img = video_cap.read()

            if not ret:

                messagebox.showerror(
                    "Camera Error",
                    "Could not read camera frame.",
                    parent=self.root
                )

                break

            # MIRROR CAMERA
            img = cv2.flip(
                img,
                1
            )

            # GRAYSCALE
            gray_image = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            # DETECT FACE
            features = face_cascade.detectMultiScale(
                gray_image,
                scaleFactor=1.1,
                minNeighbors=5
            )

            # PROCESS EACH FACE
            for (
                x,
                y,
                w,
                h
            ) in features:

                try:

                    student_id, distance = clf.predict(
                        gray_image[
                            y:y + h,
                            x:x + w
                        ]
                    )

                except Exception:

                    continue

                # CONFIDENCE
                confidence = int(
                    100 * (
                        1 - distance / 300
                    )
                )

                confidence = max(
                    0,
                    min(
                        confidence,
                        100
                    )
                )

                # CHECK STUDENT
                if (
                    confidence >= 75
                    and student_id in student_data
                ):

                    student = student_data[student_id]

                    roll = student["roll"]
                    name = student["name"]
                    department = student["department"]

                    # GREEN FACE BOX
                    cv2.rectangle(
                        img,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        3
                    )

                    # TEXT POSITION
                    text_x = x
                    text_y = y - 105

                    if text_y < 10:

                        text_y = y + h + 30

                    # ID
                    cv2.putText(
                        img,
                        f"ID: {student_id}",
                        (
                            text_x,
                            text_y
                        ),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    # ROLL
                    cv2.putText(
                        img,
                        f"Roll: {roll}",
                        (
                            text_x,
                            text_y + 25
                        ),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    # NAME
                    cv2.putText(
                        img,
                        f"Name: {name}",
                        (
                            text_x,
                            text_y + 50
                        ),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    # DEPARTMENT
                    cv2.putText(
                        img,
                        f"Department: {department}",
                        (
                            text_x,
                            text_y + 75
                        ),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    # CONFIDENCE
                    cv2.putText(
                        img,
                        f"Confidence: {confidence}%",
                        (
                            text_x,
                            text_y + 100
                        ),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    # FACE RECOGNIZED
                    cv2.putText(
                        img,
                        "Face Recognized",
                        (
                            x,
                            y + h + 30
                        ),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    # STABLE FACE RECOGNITION
                    if student_id == recognized_id:
                        recognized_frames += 1
                    else:
                        recognized_id = student_id
                        recognized_frames = 1

                    # MARK ATTENDANCE AFTER STABLE RECOGNITION
                    if not attendance_processed and recognized_frames >= 15:

                        attendance_processed = True

                        attendance_result = self.mark_attendance(
                            student_id,
                            roll,
                            name,
                            department
                        )

                        # SHOW DETAILS BEFORE CLOSING CAMERA
                        cv2.imshow(window_name, img)
                        cv2.waitKey(2000)
                        break

                else:

                    # RESET STABLE RECOGNITION
                    recognized_id = None
                    recognized_frames = 0

                    # UNKNOWN FACE
                    cv2.rectangle(
                        img,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        img,
                        "Unknown Face",
                        (
                            x,
                            y - 10
                        ),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

            # CLOSE CAMERA AFTER ATTENDANCE
            if attendance_processed:
                break

            # SHOW CAMERA
            cv2.imshow(
                window_name,
                img
            )

            # KEYBOARD
            key = cv2.waitKey(1) & 0xFF

            if (
                key == ord("q")
                or key == 27
            ):

                break

            # CLOSE WINDOW MANUALLY
            try:

                if cv2.getWindowProperty(
                    window_name,
                    cv2.WND_PROP_VISIBLE
                ) < 1:

                    break

            except:

                break

        # RELEASE CAMERA
        video_cap.release()

        cv2.destroyAllWindows()

        # SMALL DELAY FOR WINDOW CLEANUP
        try:

            cv2.waitKey(1)

        except:

            pass


# MAIN
if __name__ == "__main__":

    root = Tk()

    obj = Face_Recognition(root)

    root.mainloop()