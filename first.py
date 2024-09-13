from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from numpy.core.defchararray import title
from student import Student
import os
from capture import Capture
from face_recognition import FaceRecognitionApp
from filter import Filter
from attendance import Attendance


class Face_Recognition_System:
    def __init__(self, root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("face recognition system")

        #first image
        img=Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-alex-andrews-271121-816608.jpg")
        img=img.resize((500, 130) )
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=500, height=130)

        #second image
        img1 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-alex-andrews-271121-816608.jpg")
        img1 = img1.resize((500, 130))
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=500, y=0, width=500, height=130)

        #third image
        img2 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-alex-andrews-271121-816608.jpg")
        img2 = img2.resize((500, 130))
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=1000, y=0, width=500, height=130)

        # bg image
        img3 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-kaip-1341279.jpg")
        img3 = img3.resize((1530, 710))
        self.photoimg3= ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=130, width=1530, height=710)


        title_lbl=Label(bg_img, text="FACE RECOGNITION ATTENDANCE SOFTWARE", font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=45 )

        #student button
        img4 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-pixabay-38568.jpg")
        img4 = img4.resize((220, 220))
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1=Button(bg_img, image=self.photoimg4, command=self.student_details, bd=5, relief="ridge", cursor="hand2")
        b1.place(x=250, y=80, width=220, height=200)

        b1_1 = Button(bg_img,  text="Student details", command=self.student_details, bd=5, relief="ridge", cursor="hand2", font=("times new roman", 15, "bold"), bg="light green")
        b1_1.place(x=250, y=270, width=220, height=40)

        # Detect face button
        img5 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-david-diniz-1128466754-25913051.jpg")
        img5 = img5.resize((220, 220))
        self.photoimg5 = ImageTk.PhotoImage(img5)

        b1 = Button(bg_img, image=self.photoimg5, command=self.filter_image,  bd=5, relief="ridge", cursor="hand2")
        b1.place(x=550, y=80, width=220, height=200)

        b1_1 = Button(bg_img, text="Face Filter", cursor="hand2", command=self.filter_image,  bd=5, relief="ridge", font=("times new roman", 15, "bold") ,bg="light green")
        b1_1.place(x=550, y=270, width=220, height=40)

        # Recognize face button
        img6 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-agk42-2599244.jpg")
        img6 = img6.resize((220, 220))
        self.photoimg6 = ImageTk.PhotoImage(img6)

        b1 = Button(bg_img, image=self.photoimg6, command=self.face_recognizer,  bd=5, relief="ridge", cursor="hand2")
        b1.place(x=550, y=340, width=220, height=220)

        b1_1 = Button(bg_img, text="Recognize Face", command=self.face_recognizer,  bd=5, relief="ridge", cursor="hand2", font=("times new roman", 15, "bold"), bg="light green")
        b1_1.place(x=550, y=520, width=220, height=40)

        #Train face button
        img7 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-spemone-62171-639090.jpg")
        img7 = img7.resize((220, 220))
        self.photoimg7 = ImageTk.PhotoImage(img7)

        b1 = Button(bg_img, image=self.photoimg7,command=self.Train_data,  bd=5, relief="ridge", cursor="hand2")
        b1.place(x=250, y=340, width=220, height=220)

        b1_1 = Button(bg_img, text="Trained Face",command=self.Train_data, cursor="hand2",  bd=5, relief="ridge", font=("times new roman", 15, "bold"), bg="light green")
        b1_1.place(x=250, y=520, width=220, height=40)


        # Photos
        img8 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-samerdaboul-1226721.jpg")
        img8 = img8.resize((220, 220))
        self.photoimg8 = ImageTk.PhotoImage(img8)

        b1 = Button(bg_img, image=self.photoimg8, cursor="hand2",  bd=5, relief="ridge", command=self.open_img)
        b1.place(x=850, y=80, width=220, height=220)

        b1_1 = Button(bg_img, text="Photos", cursor="hand2",command=self.open_img,  bd=5, relief="ridge", font=("times new roman", 15, "bold"), bg="light green")
        b1_1.place(x=850, y=270, width=220, height=40)

        # Attendance face button
        img9 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-pavel-danilyuk-8423018.jpg")
        img9 = img9.resize((220, 220))
        self.photoimg9 = ImageTk.PhotoImage(img9)

        b1 = Button(bg_img, image=self.photoimg9, command=self.face_attendance,  bd=5, relief="ridge", cursor="hand2")
        b1.place(x=850, y=340, width=220, height=200)

        b1_1 = Button(bg_img, text="Attendance", command=self.face_attendance,  bd=5, relief="ridge", cursor="hand2",
                      font=("times new roman", 15, "bold"), bg="light green")
        b1_1.place(x=850, y=520, width=220, height=40)


    def open_img(self):
        os.startfile("data")



    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)


    def Train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Capture(self.new_window)

    def face_recognizer(self):
        self.new_window=Toplevel(self.root)
        self.app=FaceRecognitionApp(self.new_window)

    def filter_image(self):
        self.new_window=Toplevel(self.root)
        self.app=Filter(self.new_window)

    def face_attendance(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)


if __name__=="__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.mainloop()
