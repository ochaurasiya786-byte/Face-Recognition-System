from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
import cv2
import os
import csv
import asyncio
import math
import threading


class Face_Recognition:

    def __init__(self, root):

        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition System")
        self.root.resizable(False, False)

        self.base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        # UNIVERSITY LOCATION

        self.COLLEGE_LAT = 26.928674
        self.COLLEGE_LON = 80.896134
        self.MAX_DISTANCE = 4000

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

        # LEFT IMAGE

        top_image_path = os.path.join(
            self.base_dir,
            "College_images",
            "Detector1.png"
        )

        try:

            img_top1 = Image.open(top_image_path)

            img_top1 = img_top1.resize(
                (620, 585),
                Image.Resampling.LANCZOS
            )

            self.photoimg_top1 = ImageTk.PhotoImage(
                img_top1
            )

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

            self.photoimg_top2 = ImageTk.PhotoImage(
                img_top2
            )

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

    # GET WINDOWS LOCATION

    def get_windows_location(self):

        result = {
            "success": False,
            "latitude": None,
            "longitude": None,
            "error": None
        }

        def location_worker():

            try:

                from winrt.windows.devices.geolocation import (
                    Geolocator
                )

                # ASYNC LOCATION FUNCTION

                async def get_location():

                    print(
                        "\n========================================"
                    )

                    print(
                        "WINDOWS LOCATION: START"
                    )

                    # CREATE GEOLOCATOR

                    geolocator = Geolocator()

                    # GET CURRENT POSITION

                    position = await (
                        geolocator.get_geoposition_async()
                    )

                    coordinate = (
                        position.coordinate.point.position
                    )

                    latitude = float(
                        coordinate.latitude
                    )

                    longitude = float(
                        coordinate.longitude
                    )

                    print(
                        f"CURRENT LATITUDE : {latitude}"
                    )

                    print(
                        f"CURRENT LONGITUDE: {longitude}"
                    )

                    print(
                        "WINDOWS LOCATION: SUCCESS"
                    )

                    print(
                        "========================================"
                    )

                    return latitude, longitude

                # RUN WINRT ASYNC IN BACKGROUND THREAD

                latitude, longitude = asyncio.run(
                    get_location()
                )

                # VALIDATE

                if (
                    latitude is None
                    or longitude is None
                ):

                    raise Exception(
                        "Windows returned empty location."
                    )

                if (
                    latitude == 0
                    and longitude == 0
                ):

                    raise Exception(
                        "Windows returned 0,0 coordinates."
                    )

                result["success"] = True
                result["latitude"] = latitude
                result["longitude"] = longitude

            except Exception as e:

                result["success"] = False
                result["error"] = repr(e)

        # RUN LOCATION IN BACKGROUND THREAD

        location_thread = threading.Thread(
            target=location_worker,
            daemon=True
        )

        location_thread.start()

        # Wait until location is received

        location_thread.join()

        # LOCATION SUCCESS

        if result["success"]:

            return (
                True,
                result["latitude"],
                result["longitude"]
            )

        # LOCATION ERROR

        print(
            "\n========================================"
        )

        print(
            "WINDOWS LOCATION ERROR:"
        )

        print(
            result["error"]
        )

        print(
            "========================================\n"
        )

        return (
            False,
            None,
            None
        )

    # DISTANCE CALCULATION

    def calculate_distance(
        self,
        latitude,
        longitude
    ):

        R = 6371000

        lat1 = math.radians(
            self.COLLEGE_LAT
        )

        lat2 = math.radians(
            latitude
        )

        dlat = math.radians(
            latitude - self.COLLEGE_LAT
        )

        dlon = math.radians(
            longitude - self.COLLEGE_LON
        )

        a = (
            math.sin(dlat / 2) ** 2
            +
            math.cos(lat1)
            *
            math.cos(lat2)
            *
            math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return R * c

    # CHECK LAPTOP LOCATION

    def check_pc_location(self, student_id):

        success, latitude, longitude = (
            self.get_windows_location()
        )

        # LOCATION FAILED

        if not success:

            return False, {

                "success": False,

                "message":
                "Windows location could not be accessed.\n\n"
                "Please check Windows Location permission."
            }

        # CALCULATE DISTANCE

        distance = self.calculate_distance(
            latitude,
            longitude
        )

        print(
            f"Windows Latitude : {latitude}"
        )

        print(
            f"Windows Longitude: {longitude}"
        )

        print(
            f"College Latitude : {self.COLLEGE_LAT}"
        )

        print(
            f"College Longitude: {self.COLLEGE_LON}"
        )

        print(
            f"Distance         : {distance:.2f} meters"
        )

        # INSIDE UNIVERSITY

        if distance <= self.MAX_DISTANCE:

            print(
                "LOCATION STATUS : VERIFIED"
            )

            return True, {

                "success": True,

                "student_id": student_id,

                "latitude": latitude,

                "longitude": longitude,

                "distance": round(
                    distance,
                    2
                )
            }

        # OUTSIDE UNIVERSITY

        print(
            "LOCATION STATUS : OUTSIDE UNIVERSITY"
        )

        return False, {

            "success": False,

            "student_id": student_id,

            "latitude": latitude,

            "longitude": longitude,

            "distance": round(
                distance,
                2
            ),

            "message":
            f"Laptop is outside university range.\n\n"
            f"Distance: {distance:.2f} meters\n"
            f"Allowed: {self.MAX_DISTANCE} meters"
        }

    # EYE BLINK DETECTION

    def detect_eye_blink(
        self,
        img,
        face_box,
        blink_state
    ):

        x, y, w, h = face_box

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        face_roi = gray[
            y:y+h,
            x:x+w
        ]

        if (
            face_roi.size == 0
            or
            w < 80
            or
            h < 80
        ):

            return False

        face_roi = cv2.GaussianBlur(
            face_roi,
            (3, 3),
            0
        )

        # EYE AREA

        eye_y1 = int(
            0.18 * h
        )

        eye_y2 = int(
            0.48 * h
        )

        left_x1 = int(
            0.10 * w
        )

        left_x2 = int(
            0.48 * w
        )

        right_x1 = int(
            0.52 * w
        )

        right_x2 = int(
            0.90 * w
        )

        left_eye = face_roi[
            eye_y1:eye_y2,
            left_x1:left_x2
        ]

        right_eye = face_roi[
            eye_y1:eye_y2,
            right_x1:right_x2
        ]

        if (
            left_eye.size == 0
            or
            right_eye.size == 0
        ):

            return False

        # EDGE SCORE

        left_edges = cv2.Canny(
            left_eye,
            50,
            150
        ).mean()

        right_edges = cv2.Canny(
            right_eye,
            50,
            150
        ).mean()

        eye_score = (
            float(left_edges)
            +
            float(right_edges)
        ) / 2.0

        scores = blink_state["scores"]

        scores.append(
            eye_score
        )

        if len(scores) > 60:

            del scores[:-60]

        # WAIT FOR BASELINE

        if len(scores) < 12:

            return False

        recent_scores = scores[-45:]

        sorted_scores = sorted(
            recent_scores
        )

        index = int(
            len(sorted_scores) * 0.80
        )

        if index >= len(sorted_scores):

            index = (
                len(sorted_scores) - 1
            )

        baseline = float(
            sorted_scores[index]
        )

        if baseline <= 1:

            return False

        # EYE CLOSING

        if not blink_state["closed"]:

            if (
                eye_score
                <
                baseline * 0.82
            ):

                blink_state[
                    "closed_frames"
                ] += 1

                blink_state[
                    "open_frames"
                ] = 0

                if (
                    blink_state[
                        "closed_frames"
                    ] >= 3
                ):

                    blink_state[
                        "closed"
                    ] = True

                    blink_state[
                        "closed_frames"
                    ] = 0

            else:

                blink_state[
                    "closed_frames"
                ] = 0

            return False

        # EYE OPENING AGAIN

        if (
            eye_score
            >
            baseline * 0.93
        ):

            blink_state[
                "open_frames"
            ] += 1

            if (
                blink_state[
                    "open_frames"
                ] >= 2
            ):

                blink_state[
                    "closed"
                ] = False

                blink_state[
                    "open_frames"
                ] = 0

                blink_state[
                    "closed_frames"
                ] = 0

                blink_state[
                    "blinked"
                ] = True

                return True

        else:

            blink_state[
                "open_frames"
            ] = 0

        return False

    # MARK ATTENDANCE

    def mark_attendance(
        self,
        student_id,
        roll,
        name,
        department,
        verification_data
    ):

        file_name = os.path.join(
            self.base_dir,
            "attendence.csv"
        )

        now = datetime.now()

        today_date = now.strftime(
            "%d/%m/%Y"
        )

        current_time = now.strftime(
            "%H:%M:%S"
        )

        latitude = verification_data.get(
            "latitude",
            ""
        )

        longitude = verification_data.get(
            "longitude",
            ""
        )

        distance = verification_data.get(
            "distance",
            ""
        )

        face_status = "Matched"
        location_status = "Verified"
        time_status = "Verified"
        attendance_status = "Present"

        header = [
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
        ]

        # CREATE CSV

        if not os.path.exists(
            file_name
        ):

            try:

                with open(
                    file_name,
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as f:

                    writer = csv.writer(f)

                    writer.writerow(
                        header
                    )

            except Exception as e:

                messagebox.showerror(
                    "CSV Error",
                    f"Could not create attendance file.\n\n{e}",
                    parent=self.root
                )

                return False

        # CHECK TODAY ATTENDANCE

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

                    if str(
                        row[0]
                    ).strip().lower() in (
                        "student_id",
                        "student id"
                    ):

                        continue

                    if len(row) >= 13:

                        old_id = str(
                            row[0]
                        ).strip()

                        old_date = str(
                            row[5]
                        ).strip()

                        if (
                            old_id ==
                            str(student_id).strip()
                            and
                            old_date ==
                            today_date
                        ):

                            old_time = str(
                                row[4]
                            ).strip()

                            messagebox.showwarning(
                                "Already Marked",

                                f"⚠️ Attendance Already Marked!\n\n"
                                f"Name: {name}\n"
                                f"Roll No: {roll}\n"
                                f"Department: {department}\n"
                                f"Student ID: {student_id}\n"
                                f"Date: {today_date}\n"
                                f"Time: {old_time}",

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

        # SAVE ATTENDANCE

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
                    latitude,
                    longitude,
                    distance,
                    face_status,
                    location_status,
                    time_status,
                    attendance_status
                ])

            messagebox.showinfo(
                "Attendance Marked",

                f"✅ Attendance Marked Successfully!\n\n"
                f"Name: {name}\n"
                f"Roll No: {roll}\n"
                f"Department: {department}\n"
                f"Student ID: {student_id}\n"
                f"Date: {today_date}\n"
                f"Time: {current_time}\n\n"
                f"Face: {face_status}\n"
                f"Location: {location_status}\n"
                f"Distance: {distance} meters\n"
                f"Time Verification: {time_status}\n"
                f"Status: {attendance_status}",

                parent=self.root
            )

            return True

        except Exception as e:

            messagebox.showerror(
                "CSV Error",
                f"Could not save attendance.\n\n{e}",
                parent=self.root
            )

            return False

    # FACE RECOGNITION

    def face_recog(self):

        # HAAR CASCADE

        cascade_path = os.path.join(
            self.base_dir,
            "haarcascade_frontalface_default.xml"
        )

        if not os.path.exists(
            cascade_path
        ):

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

        # LBPH

        try:

            clf = (
                cv2.face.LBPHFaceRecognizer_create()
            )

        except AttributeError:

            messagebox.showerror(
                "Error",
                "cv2.face is not available.\n\n"
                "Install opencv-contrib-python.",
                parent=self.root
            )

            return

        # CLASSIFIER

        classifier_path = os.path.join(
            self.base_dir,
            "classifier.xml"
        )

        if not os.path.exists(
            classifier_path
        ):

            messagebox.showerror(
                "Error",
                "classifier.xml file not found!\n\n"
                "First train the dataset.",
                parent=self.root
            )

            return

        try:

            clf.read(
                classifier_path
            )

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
            from approval_service import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    Student_ID,
                    Roll,
                    Student_Name,
                    Dep
                FROM student
            """)

            results = cursor.fetchall()

            for row in results:

                try:

                    student_id = int(
                        row[0]
                    )

                    student_data[
                        student_id
                    ] = {

                        "roll": str(
                            row[1]
                        ).strip(),

                        "name": str(
                            row[2]
                        ).strip(),

                        "department": str(
                            row[3]
                        ).strip()
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

        if not student_data:

            messagebox.showwarning(
                "Warning",
                "No student data found in database.",
                parent=self.root
            )

            return

        # CAMERA

        video_cap = cv2.VideoCapture(
            0
        )

        if not video_cap.isOpened():

            messagebox.showerror(
                "Camera Error",
                "Camera could not be opened.",
                parent=self.root
            )

            return

        window_name = (
            "Welcome to Face Recognition"
        )

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

        # VARIABLES

        attendance_processed = False

        recognized_id = None

        recognized_frames = 0

        # BLINK VARIABLES

        blink_verified = False

        blink_state = {

            "scores": [],

            "closed": False,

            "closed_frames": 0,

            "open_frames": 0,

            "blinked": False
        }

        # CAMERA LOOP

        while True:

            ret, img = video_cap.read()

            if not ret:

                messagebox.showerror(
                    "Camera Error",
                    "Could not read camera frame.",
                    parent=self.root
                )

                break

            img = cv2.flip(
                img,
                1
            )

            gray_image = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            features = (
                face_cascade.detectMultiScale(
                    gray_image,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(100, 100)
                )
            )

            for (
                x,
                y,
                w,
                h
            ) in features:

                try:

                    predicted_id, distance = (
                        clf.predict(
                            gray_image[
                                y:y+h,
                                x:x+w
                            ]
                        )
                    )

                except Exception:

                    continue

                confidence = int(
                    100 *
                    (
                        1 -
                        distance / 300
                    )
                )

                confidence = max(
                    0,
                    min(
                        confidence,
                        100
                    )
                )

                # RECOGNIZED FACE

                if (
                    confidence >= 80
                    and
                    predicted_id in student_data
                ):

                    student_id = int(
                        predicted_id
                    )

                    student = student_data[
                        student_id
                    ]

                    roll = student[
                        "roll"
                    ]

                    name = student[
                        "name"
                    ]

                    department = student[
                        "department"
                    ]

                    cv2.rectangle(
                        img,
                        (x, y),
                        (x+w, y+h),
                        (0, 255, 0),
                        3
                    )

                    text_x = x

                    text_y = y - 105

                    if text_y < 10:

                        text_y = (
                            y + h + 30
                        )

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

                    # STABLE RECOGNITION

                    if (
                        student_id ==
                        recognized_id
                    ):

                        recognized_frames += 1

                    else:

                        recognized_id = (
                            student_id
                        )

                        recognized_frames = 1

                        # RESET BLINK WHEN NEW FACE
                        blink_verified = False

                        blink_state = {

                            "scores": [],

                            "closed": False,

                            "closed_frames": 0,

                            "open_frames": 0,

                            "blinked": False
                        }

                    # EYE BLINK VERIFICATION

                    if not blink_verified:

                        blink_now = self.detect_eye_blink(
                            img,
                            (x, y, w, h),
                            blink_state
                        )

                        if blink_now:

                            blink_verified = True

                            cv2.putText(
                                img,
                                "Blink Verified",
                                (
                                    x,
                                    y + h + 55
                                ),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.65,
                                (0, 255, 0),
                                2
                            )

                        else:

                            cv2.putText(
                                img,
                                "Please Blink Your Eyes",
                                (
                                    x,
                                    y + h + 55
                                ),
                                cv2.FONT_HERSHEY_COMPLEX,
                                0.65,
                                (0, 255, 255),
                                2
                            )

                    else:

                        cv2.putText(
                            img,
                            "Blink Verified",
                            (
                                x,
                                y + h + 55
                            ),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.65,
                            (0, 255, 0),
                            2
                        )

                    # 15 FRAMES + BLINK

                    if (
                        not attendance_processed
                        and
                        recognized_frames >= 15
                        and
                        blink_verified
                    ):

                        attendance_processed = True

                        # AUTOMATIC WINDOWS LOCATION

                        (
                            verification_success,
                            verification_data
                        ) = (
                            self.check_pc_location(
                                student_id
                            )
                        )

                        # LOCATION FAILED

                        if not verification_success:

                            messagebox.showwarning(
                                "Location Verification Failed",

                                f"❌ Attendance Not Marked!\n\n"
                                f"Name: {name}\n"
                                f"Student ID: {student_id}\n\n"
                                f"Reason:\n"
                                f"{verification_data.get('message', 'Location verification failed.')}",

                                parent=self.root
                            )

                            break

                        # DISPLAY VERIFICATION

                        cv2.putText(
                            img,
                            "Location Verified",
                            (
                                x,
                                y + h + 80
                            ),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.65,
                            (0, 255, 0),
                            2
                        )

                        cv2.putText(
                            img,
                            "Time Verified",
                            (
                                x,
                                y + h + 105
                            ),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.65,
                            (0, 255, 0),
                            2
                        )

                        cv2.putText(
                            img,
                            "Attendance Verified",
                            (
                                x,
                                y + h + 130
                            ),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.65,
                            (0, 255, 0),
                            2
                        )

                        # SAVE ATTENDANCE

                        self.mark_attendance(
                            student_id,
                            roll,
                            name,
                            department,
                            verification_data
                        )

                        cv2.imshow(
                            window_name,
                            img
                        )

                        cv2.waitKey(
                            2000
                        )

                        break

                # UNKNOWN FACE

                else:

                    recognized_id = None

                    recognized_frames = 0

                    blink_verified = False

                    blink_state = {

                        "scores": [],

                        "closed": False,

                        "closed_frames": 0,

                        "open_frames": 0,

                        "blinked": False
                    }

                    cv2.rectangle(
                        img,
                        (x, y),
                        (x+w, y+h),
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

            # ATTENDANCE PROCESSED

            if attendance_processed:

                break

            cv2.imshow(
                window_name,
                img
            )

            key = cv2.waitKey(
                1
            ) & 0xFF

            if (
                key == ord("q")
                or
                key == 27
            ):

                break

            try:

                if (
                    cv2.getWindowProperty(
                        window_name,
                        cv2.WND_PROP_VISIBLE
                    ) < 1
                ):

                    break

            except:

                break

        # RELEASE CAMERA

        video_cap.release()

        cv2.destroyAllWindows()

        try:

            cv2.waitKey(
                1
            )

        except:

            pass


# MAIN

if __name__ == "__main__":

    root = Tk()

    obj = Face_Recognition(
        root
    )

    root.mainloop()