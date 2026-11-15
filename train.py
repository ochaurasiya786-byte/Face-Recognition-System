from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

class Train:

    def __init__(self, root):

        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.resizable(True, True)

        self.base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        # TITLE

        title_lbl = Label(
            self.root,
            text="TRAIN DATA SET",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="darkgreen"
        )

        title_lbl.place(
            x=0,
            y=0,
            width=1530,
            height=70
        )

        # TOP IMAGE

        img_top_path = os.path.join(
            self.base_dir,
            "College_images",
            "img2.png"
        )

        try:

            img_top = Image.open(
                img_top_path
            )

            img_top = img_top.resize(
                (1450, 270),
                Image.Resampling.LANCZOS
            )

            self.photoimg_top = ImageTk.PhotoImage(
                img_top
            )

            f_lbl1 = Label(
                self.root,
                image=self.photoimg_top,
                bd=0
            )

            f_lbl1.place(
                x=0,
                y=70,
                width=1450,
                height=270
            )

        except Exception as e:

            messagebox.showerror(
                "Image Error",
                f"img2.png not found!\n\n{e}",
                parent=self.root
            )

        # TRAIN BUTTON

        train_btn = Button(
            self.root,
            text="TRAIN DATA",
            command=self.train_classifier,
            font=("times new roman", 18, "bold"),
            bg="green",
            fg="white",
            activebackground="darkgreen",
            activeforeground="white",
            cursor="hand2",
            bd=0
        )

        train_btn.place(
            x=0,
            y=340,
            width=1450,
            height=50
        )

        train_btn.bind(
            "<Enter>",
            lambda e: train_btn.config(bg="darkgreen")
        )

        train_btn.bind(
            "<Leave>",
            lambda e: train_btn.config(bg="green")
        )

        # BOTTOM IMAGE

        img_bottom_path = os.path.join(
            self.base_dir,
            "College_images",
            "train2.png"
        )

        try:

            img_bottom = Image.open(
                img_bottom_path
            )

            img_bottom = img_bottom.resize(
                (1450, 270),
                Image.Resampling.LANCZOS
            )

            self.photoimg_bottom = ImageTk.PhotoImage(
                img_bottom
            )

            f_lbl2 = Label(
                self.root,
                image=self.photoimg_bottom,
                bd=0
            )

            f_lbl2.place(
                x=0,
                y=390,
                width=1450,
                height=270
            )

        except Exception as e:

            messagebox.showerror(
                "Image Error",
                f"train2.png not found!\n\n{e}",
                parent=self.root
            )

    # TRAIN CLASSIFIER

    def train_classifier(self):

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        data_dir = os.path.join(
            base_dir,
            "data"
        )

        classifier_path = os.path.join(
            base_dir,
            "classifier.xml"
        )

        temp_path = os.path.join(
            base_dir,
            "classifier_temp.xml"
        )

        # CHECK DATA FOLDER

        if not os.path.exists(data_dir):

            messagebox.showerror(
                "Error",
                "Data folder not found!",
                parent=self.root
            )

            return

        image_files = [
            os.path.join(data_dir, file)
            for file in os.listdir(data_dir)
            if file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            )
        ]

        if len(image_files) == 0:

            messagebox.showerror(
                "Error",
                "No training images found in data folder!",
                parent=self.root
            )

            return

        # LOAD DATABASE

        student_data = {}

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Omkar@7518",
                database="student"
            )

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    Student_ID,
                    Student_Name
                FROM student
            """)

            results = cursor.fetchall()

            for row in results:

                try:

                    sid = int(row[0])

                    student_data[sid] = str(
                        row[1]
                    ).strip()

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

        # TRAINING DATA

        faces = []
        ids = []

        training_window = "Training"

        cv2.namedWindow(
            training_window,
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            training_window,
            450,
            450
        )

        # READ IMAGES

        for image_path in image_files:

            try:

                filename = os.path.basename(
                    image_path
                )

                # EXPECTED:
                # User.213.1.jpg
                # User.213.2.jpg
                # User.213.3.jpg

                parts = filename.split(".")

                if len(parts) < 3:
                    continue

                try:

                    student_id = int(
                        parts[1]
                    )

                except ValueError:
                    continue

                # CHECK ID IN DATABASE

                if student_id not in student_data:

                    print(
                        "Skipped - Student ID not in database:",
                        filename
                    )

                    continue

                student_name = student_data[
                    student_id
                ]

                # LOAD IMAGE

                img = Image.open(
                    image_path
                ).convert("L")

                image_np = np.array(
                    img,
                    dtype=np.uint8
                )

                # ADD TRAINING DATA

                faces.append(
                    image_np
                )

                ids.append(
                    student_id
                )

                # SHOW TRAINING INFORMATION

                display_img = cv2.cvtColor(
                    image_np,
                    cv2.COLOR_GRAY2BGR
                )

                cv2.putText(
                    display_img,
                    f"ID: {student_id}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    display_img,
                    f"Name: {student_name}",
                    (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 0),
                    2
                )

                cv2.imshow(
                    training_window,
                    display_img
                )

                cv2.waitKey(1)

                print(
                    f"Training: {filename} -> "
                    f"ID={student_id} -> "
                    f"Name={student_name}"
                )

            except Exception as e:

                print(
                    "Error in image:",
                    image_path
                )

                print(
                    "Error:",
                    e
                )

                continue

        # CHECK VALID DATA

        if len(faces) == 0:

            cv2.destroyAllWindows()

            messagebox.showerror(
                "Error",
                "Valid training images not found!\n\n"
                "Check your data folder filenames.",
                parent=self.root
            )

            return

        # TRAIN

        try:

            ids = np.array(
                ids,
                dtype=np.int32
            )

            clf = cv2.face.LBPHFaceRecognizer_create()

            clf.train(
                faces,
                ids
            )

            # SAVE TEMP CLASSIFIER

            clf.write(
                temp_path
            )

            # REPLACE OLD CLASSIFIER

            if os.path.exists(
                classifier_path
            ):

                os.remove(
                    classifier_path
                )

            os.replace(
                temp_path,
                classifier_path
            )

            cv2.destroyAllWindows()

            # TRAINING SUCCESS

            unique_ids = sorted(
                set(ids.tolist())
            )

            trained_students = []

            for sid in unique_ids:

                trained_students.append(
                    f"{sid} - "
                    f"{student_data.get(sid, 'Unknown')}"
                )

            messagebox.showinfo(
                "Training Completed",

                "✅ Training datasets completed!\n\n"
                "Students trained:\n\n"
                +
                "\n".join(
                    trained_students
                ),

                parent=self.root
            )

        except Exception as e:

            cv2.destroyAllWindows()

            if os.path.exists(
                temp_path
            ):

                os.remove(
                    temp_path
                )

            messagebox.showerror(
                "Training Error",
                str(e),
                parent=self.root
            )

# MAIN

if __name__ == "__main__":

    root = Tk()

    obj = Train(
        root
    )

    root.mainloop()
