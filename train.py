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

# STANDALONE ENGINE FUNCTION
def train_dataset_engine(base_dir=None, show_window=False):
    """
    Trains the LBPH Face Recognizer classifier using all samples in the data directory.
    Works independently of database availability (never skips valid faces).
    Returns (success: bool, message: str, trained_students: list).
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(base_dir, "data")
    classifier_path = os.path.join(base_dir, "classifier.xml")
    temp_path = os.path.join(base_dir, "classifier_temp.xml")

    if not os.path.exists(data_dir):
        return False, "Data folder not found!", []

    image_files = [
        os.path.join(data_dir, file)
        for file in os.listdir(data_dir)
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(image_files) == 0:
        return False, "No training images found in data folder!", []

    # Optional: fetch student names from cloud DB for display
    student_data = {}
    try:
        from approval_service import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Student_ID, Student_Name FROM student")
            for row in cursor.fetchall():
                try:
                    student_data[int(row[0])] = str(row[1]).strip()
                except Exception:
                    pass
        except Exception:
            pass

        try:
            cursor.execute("SELECT Student_ID, Student_Name FROM student_requests")
            for row in cursor.fetchall():
                try:
                    sid = int(row[0])
                    if sid not in student_data:
                        student_data[sid] = str(row[1]).strip()
                except Exception:
                    pass
        except Exception:
            pass

        cursor.close()
        conn.close()
    except Exception as e:
        print("Notice: Proceeding with training in offline ID mode (DB unreachable):", e)

    faces = []
    ids = []

    training_window = "Training Face Data"
    if show_window:
        try:
            cv2.namedWindow(training_window, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(training_window, 450, 450)
        except Exception:
            show_window = False

    for image_path in image_files:
        try:
            filename = os.path.basename(image_path)
            parts = filename.split(".")
            if len(parts) < 3:
                continue

            try:
                student_id = int(parts[1])
            except ValueError:
                continue

            student_name = student_data.get(student_id, f"Student {student_id}")

            img = Image.open(image_path).convert("L")
            image_np = np.array(img, dtype=np.uint8)

            faces.append(image_np)
            ids.append(student_id)

            if show_window:
                display_img = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
                cv2.putText(display_img, f"ID: {student_id}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(display_img, f"Name: {student_name}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
                cv2.imshow(training_window, display_img)
                cv2.waitKey(1)

        except Exception as e:
            print("Error in image:", image_path, e)
            continue

    if show_window:
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass

    if len(faces) == 0:
        return False, "Valid training images not found in data folder!", []

    try:
        ids_arr = np.array(ids, dtype=np.int32)
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids_arr)
        clf.write(temp_path)

        if os.path.exists(classifier_path):
            try:
                os.remove(classifier_path)
            except Exception:
                pass

        os.replace(temp_path, classifier_path)

        unique_ids = sorted(set(ids))
        trained_students = [
            f"ID {sid} - {student_data.get(sid, 'Student ' + str(sid))}"
            for sid in unique_ids
        ]
        return True, f"Successfully trained {len(faces)} face samples across {len(unique_ids)} student(s).", trained_students

    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return False, f"Classifier training failed: {str(e)}", []


    # TRAIN CLASSIFIER

    def train_classifier(self):
        success, message, trained_students = train_dataset_engine(self.base_dir, show_window=True)
        if success:
            summary = "\n".join(trained_students)
            messagebox.showinfo(
                "Training Completed",
                f"✅ Training datasets completed successfully!\n\n"
                f"{message}\n\n"
                f"Students trained:\n{summary}",
                parent=self.root
            )
        else:
            messagebox.showerror(
                "Training Error",
                message,
                parent=self.root
            )

# MAIN

if __name__ == "__main__":

    root = Tk()

    obj = Train(
        root
    )

    root.mainloop()
