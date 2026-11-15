from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import os

class Developer:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title(" AI-Based Face Recognition System")
        self.root.resizable(False,False)

        # BASE PATH
        base=os.path.dirname(os.path.abspath(__file__))

        # TITLE
        Label(root,text="Developer",font=("times new roman",35,"bold"),bg="white",fg="darkgreen").place(x=0,y=0,width=1366,height=70)

        # IMAGE FOLDER
        folder=os.path.join(base,"College_images")
        if not os.path.exists(folder):
            folder=os.path.join(base,"college_images")

        # BACKGROUND
        bg_path=os.path.join(folder,"Devloper1.png")
        try:
            bg=Image.open(bg_path)
            bg=bg.resize((1360,665),Image.Resampling.LANCZOS)
            self.bg_img=ImageTk.PhotoImage(bg)
            Label(root,image=self.bg_img,bd=0).place(x=0,y=70,width=1360,height=665)
        except Exception as e:
            messagebox.showerror("Background Error","Devloper1.png nahi mil rahi.\n\nCheck karo:\n"+bg_path+"\n\nError:\n"+str(e))

        # MAIN FRAME
        frame=Frame(root,bd=2,relief=SOLID,bg="white")
        frame.place(x=20,y=85,width=500,height=640)

        # DEVELOPER PHOTO
        pic_path=os.path.join(folder,"om.png")
        try:
            pic=Image.open(pic_path)
            pic=pic.resize((190,190),Image.Resampling.LANCZOS)
            self.pic_img=ImageTk.PhotoImage(pic)
            Label(frame,image=self.pic_img,bd=0).place(x=15,y=15,width=190,height=190)

            # DEVELOPER INFORMATION
            Label(frame,text="Hello, My name is",font=("Segoe UI",13,"bold"),bg="white").place(x=225,y=20)
            Label(frame,text="Omkar Chaurasiya",font=("Segoe UI",16,"bold"),bg="white",fg="darkgreen").place(x=225,y=55)
            Label(frame,text="Full Stack Developer",font=("Segoe UI",12,"bold"),bg="white").place(x=225,y=95)
            Label(frame,text="B.Tech – CSE",font=("Segoe UI",11),bg="white").place(x=225,y=125)
            Label(frame,text="AI-Based Student Recognition System",font=("Segoe UI",10,"bold"),bg="white",fg="darkgreen").place(x=225,y=155)

            # SEPARATOR
            Frame(frame,bg="darkgreen",height=2).place(x=15,y=215,width=465)

            # PROJECT INFORMATION
            Label(frame,text="Project Information",font=("Segoe UI",14,"bold"),bg="white",fg="darkgreen").place(x=18,y=230)
            Label(frame,text="Project:",font=("Segoe UI",10,"bold"),bg="white").place(x=18,y=270)
            Label(frame,text="AI-Based Face Recognition Attendance System",font=("Segoe UI",10),bg="white").place(x=95,y=270)
            Label(frame,text="Institute:",font=("Segoe UI",10,"bold"),bg="white").place(x=18,y=300)
            Label(frame,text="Khwaja Moinuddin Chishti Language University",font=("Segoe UI",9),bg="white").place(x=95,y=300)
            Label(frame,text="Location:",font=("Segoe UI",10,"bold"),bg="white").place(x=18,y=330)
            Label(frame,text="Lucknow, Uttar Pradesh",font=("Segoe UI",10),bg="white").place(x=95,y=330)
            Label(frame,text="Guide:",font=("Segoe UI",10,"bold"),bg="white").place(x=18,y=360)
            Label(frame,text="Dr. Amlendra Sir",font=("Segoe UI",10),bg="white").place(x=95,y=360)

            # TECHNOLOGIES
            Label(frame,text="Technologies Used",font=("Segoe UI",13,"bold"),bg="white",fg="darkgreen").place(x=18,y=395)
            Label(frame,text="Python  •  Tkinter  •  OpenCV",font=("Segoe UI",10),bg="white").place(x=18,y=425)
            Label(frame,text="NumPy  •  MySQL  •  PIL",font=("Segoe UI",10),bg="white").place(x=18,y=455)

            # DEVELOPER ROLE
            Label(frame,text="Developer Role",font=("Segoe UI",13,"bold"),bg="white",fg="darkgreen").place(x=260,y=395)
            Label(frame,text="• GUI Development",font=("Segoe UI",9),bg="white").place(x=260,y=425)
            Label(frame,text="• Database Integration",font=("Segoe UI",9),bg="white").place(x=260,y=450)
            Label(frame,text="• Face Recognition",font=("Segoe UI",9),bg="white").place(x=260,y=475)

            # PROJECT FEATURES
            Label(frame,text="Project Features",font=("Segoe UI",13,"bold"),bg="white",fg="darkgreen").place(x=18,y=500)
            Label(frame,text="• Face Detection & Recognition",font=("Segoe UI",9),bg="white").place(x=18,y=530)
            Label(frame,text="• Automated Student Attendance",font=("Segoe UI",9),bg="white").place(x=18,y=555)
            Label(frame,text="• Student Record Management",font=("Segoe UI",9),bg="white").place(x=18,y=580)

            # COPYRIGHT
            Label(frame,text="© 2026 AI-Based Face Recognition Attendance System",font=("Segoe UI",9,"bold"),bg="white",fg="gray").place(x=18,y=610)

        except Exception as e:
            messagebox.showerror("Developer Photo Error","om.png nahi mil rahi.\n\nCheck karo:\n"+pic_path+"\n\nError:\n"+str(e))

# MAIN
if __name__=="__main__":
    root=Tk()
    obj=Developer(root)
    root.mainloop()