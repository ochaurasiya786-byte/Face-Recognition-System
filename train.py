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

        # ================= TITLE =================

        title_lbl = Label(self.root, text="TRAIN DATA SET", font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=70)

        # ================= TOP IMAGE =================

        img_top = Image.open(r"College_images\img2.png")
        img_top = img_top.resize((1450, 270), Image.Resampling.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl1 = Label(self.root, image=self.photoimg_top, bd=0)
        f_lbl1.place(x=0, y=70, width=1450, height=270)

        # ================= TRAIN DATA =================

        train_btn = Button(self.root, text="TRAIN DATA", command=self.train_classifier, font=("times new roman", 18, "bold"), bg="green", fg="white", activebackground="darkgreen", activeforeground="white", cursor="hand2", bd=0)
        train_btn.place(x=0, y=340, width=1450, height=50)

        # ================= BOTTOM IMAGE =================

        img_bottom = Image.open(r"College_images\train2.png")
        img_bottom = img_bottom.resize((1450, 270), Image.Resampling.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl2 = Label(self.root, image=self.photoimg_bottom, bd=0)
        f_lbl2.place(x=0, y=390, width=1450, height=270)

    # ================= TRAIN CLASSIFIER =================

    def train_classifier(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        classifier_path = os.path.join(base_dir, "classifier.xml")
        temp_path = os.path.join(base_dir, "classifier_temp.xml")

        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data folder not found!")
            return

        path = [
            os.path.join(data_dir, file)
            for file in os.listdir(data_dir)
            if file.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        if len(path) == 0:
            messagebox.showerror("Error", "No training images found in data folder!")
            return

        faces = []
        ids = []

        # ================= SHOW TRAINING WINDOW =================

        training_window = cv2.namedWindow("Training", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Training", 450, 450)

        for image in path:

            try:
                img = Image.open(image).convert("L")
                image_np = np.array(img, dtype=np.uint8)

                filename = os.path.basename(image)
                id = int(filename.split(".")[1])

                faces.append(image_np)
                ids.append(id)

                # ================= SHOW SAVED FACE =================

                cv2.imshow("Training", image_np)
                cv2.waitKey(1)

            except Exception as e:
                print("Error in image:", image)
                print("Error:", e)
                continue

        if len(faces) == 0:
            cv2.destroyAllWindows()
            messagebox.showerror("Error", "Valid training images not found!")
            return

        try:

            ids = np.array(ids)

            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.train(faces, ids)

            # ================= SAVE CLASSIFIER =================

            clf.write(temp_path)

            # ================= REPLACE OLD CLASSIFIER =================

            if os.path.exists(classifier_path):
                os.remove(classifier_path)

            os.replace(temp_path, classifier_path)

            cv2.destroyAllWindows()

            messagebox.showinfo("Result", "Training datasets completed!!!")

        except Exception as e:

            cv2.destroyAllWindows()

            if os.path.exists(temp_path):
                os.remove(temp_path)

            messagebox.showerror("Training Error", str(e))


if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()