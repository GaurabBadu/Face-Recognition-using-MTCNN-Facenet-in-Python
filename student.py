from re import search
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
from click import password_option
from facenet_pytorch import InceptionResnetV1, MTCNN
import numpy as np
import os
import torch
import mysql.connector
from numpy.lib.function_base import delete


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Initialize MTCNN for face detection
        self.mtcnn =  MTCNN(keep_all=True, min_face_size=20, thresholds=[0.2, 0.3, 0.4])
        # Initialize FaceNet model for face embeddings
        self.facenet = InceptionResnetV1(pretrained='vggface2').eval()

        # Variables
        self.var_Dep = StringVar()
        self.var_course = StringVar()
        self.var_Year = StringVar()
        self.var_Name = StringVar()
        self.var_Class = StringVar()
        self.var_Roll = StringVar()
        self.var_Teacher_name = StringVar()
        self.var_radio1= StringVar()

        # Load and display images
        self.load_images()

        title_lbl = Label(self.root, text="STUDENT ATTENDANCE SYSTEM",
                          font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=50, width=1530, height=45)

        # Main Frame
        main_frame = Frame(self.root, bd=5, relief="ridge", bg="white")
        main_frame.place(x=5, y=100, width=1345, height=590)

        # Left label frame
        Left_frame = LabelFrame(main_frame, bd=5, relief="solid",
                                 font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=690, height=570)

        self.load_left_frame_images(Left_frame)

        # Right label frame
        Right_frame = LabelFrame(main_frame, bd=5, relief="solid",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=710, y=10, width=620, height=570)

        img_Right=Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-pixabay-38568.jpg")
        img_Right=img_Right.resize((605,150))
        self.photoimg_Right=ImageTk.PhotoImage(img_Right)

        f_label=Label(Right_frame, image=self.photoimg_Right, bd=5, relief="raised")
        f_label.place(x=5, y=0, width=605, height=140 )


        #Search System
        Search_frame=LabelFrame(Right_frame, bd=5, bg="white", relief="raised", text="Search System", font=("times new roman", 12))
        Search_frame.place(x=5, y=150, width=605, height=70)

        Search_label=Label(Search_frame, text='Search By:', font=("times new roman", 13, "bold"), bg="white")
        Search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)


        search_combo = ttk.Combobox(Search_frame,  font=("times new roman", 12, "bold"),
                                 state="readonly", width=17)
        search_combo["values"] = ("Select ", "Name", "Roll ")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_btn=Button(Search_frame, text="Search", width=12, font=("times new roman", 13, "bold"), bg="blue")
        search_btn.grid(row=0, column=2)

        showAll_btn = Button(Search_frame, text="Show All", command=self.fetch_data, width=12, font=("times new roman", 13, "bold"), bg="blue")
        showAll_btn.grid(row=0, column=3)

        table_frame = Frame(Right_frame, bd=5,  bg="white", relief="raised")
        table_frame.place(x=5, y=230, width=605, height=300)

        scroll_x=ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        style = ttk.Style()

        # Configure a new style for the Treeview headings
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")  # Change font and color

        self.Student_table=ttk.Treeview(table_frame, column=("dep","Course", "Year", "Name", "Class", "Roll",  "Teacher_name"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT,   fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        self.Student_table.heading("dep", text="Department")
        self.Student_table.heading("Course", text="Course")
        self.Student_table.heading("Year", text="Year")
        self.Student_table.heading("Name", text="Name")
        self.Student_table.heading("Class", text="Class")
        self.Student_table.heading("Roll", text="Roll")
        self.Student_table.heading("Teacher_name", text="Teacher_name")

        self.Student_table.column("dep", width=100, anchor=CENTER)
        self.Student_table.column("Course", width=100, anchor=CENTER)
        self.Student_table.column("Year", width=100, anchor=CENTER)
        self.Student_table.column("Name", width=150, anchor=CENTER)
        self.Student_table.column("Class", width=100, anchor=CENTER)
        self.Student_table.column("Roll", width=100, anchor=CENTER)
        self.Student_table.column("Teacher_name", width=150, anchor=CENTER)

        self.Student_table["show"]="headings"

        self.Student_table.pack(fill=BOTH, expand=1, )

        self.setup_student_details_frame(Left_frame)

    def load_images(self):
        self.image_paths = [
            r"C:\Users\User\PycharmProjects\pythonProject\pexels-kaip-1341279.jpg"]
        self.image_positions = [(0, 0, 1400, 50)]

        for path, pos in zip(self.image_paths, self.image_positions):
            img = Image.open(path)
            img = img.resize((pos[2], pos[3]))
            photo_img = ImageTk.PhotoImage(img)
            Label(self.root, image=photo_img).place(x=pos[0], y=pos[1], width=pos[2], height=pos[3])
            self.root.image = photo_img

        img_bg = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-kaip-1341279.jpg")
        img_bg = img_bg.resize((1530, 710))
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)
        bg_img = Label(self.root, image=self.photoimg_bg)
        bg_img.place(x=0, y=130, width=1530, height=710)

    def load_left_frame_images(self, left_frame):
        img_left = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-pixabay-38568.jpg")
        img_left = img_left.resize((665, 150))
        self.photoimg_left = ImageTk.PhotoImage(img_left)
        Label(left_frame, image=self.photoimg_left, bd=5, relief="raised").place(x=5, y=0, width=665, height=150)



    def setup_student_details_frame(self, left_frame):
        # Current Course
        current_course_frame = LabelFrame(left_frame, bd=5, relief="raised", text="Current Course",
                                          font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=150, width=675, height=150)

        self.create_course_widgets(current_course_frame)

        # Class Student Information
        class_Student_frame = LabelFrame(left_frame, bd=5, relief="raised", text="Class Student Information",
                                         font=("times new roman", 12, "bold"))
        class_Student_frame.place(x=5, y=310, width=675, height=220)

        self.create_student_info_widgets(class_Student_frame)

    def create_course_widgets(self, frame):
        # Department
        Label(frame, text="School", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=0, padx=10)
        dep_combo = ttk.Combobox(frame, textvariable=self.var_Dep, font=("times new roman", 12, "bold"),
                                 state="readonly", width=17)
        dep_combo["values"] = ("Select Schools", "Kanjirowa", "Samriddhi", "RBS", "Euro")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Course
        Label(frame, text="Course", font=("times new roman", 12, "bold"), bg="white").grid(row=1, column=0, padx=10)
        course_combo = ttk.Combobox(frame, textvariable=self.var_course,
                                    font=("times new roman", 12, "bold"), state="readonly", width=17)
        course_combo["values"] = ("Select Course", "Robotics", "Coding")
        course_combo.current(0)
        course_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Year
        Label(frame, text="Year", font=("times new roman", 12, "bold"), bg="white").grid(row=2, column=0, padx=10)
        year_combo = ttk.Combobox(frame, textvariable=self.var_Year,
                                  font=("times new roman", 12, "bold"), state="readonly", width=17)
        year_combo["values"] = ("Select Year", "2022", "2023", "2024")
        year_combo.current(0)
        year_combo.grid(row=2, column=1, padx=2, pady=10, sticky=W)

    def create_student_info_widgets(self, frame):
        # Student name
        Label(frame, text="Name", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, sticky=W)
        ttk.Entry(frame, textvariable=self.var_Name, width=20, font=("times new roman", 13, "bold")).grid(row=0, column=1, padx=10, sticky=W)

        # Class
        Label(frame, text="Class", font=("times new roman", 12, "bold"), bg="white").grid(row=1, column=0, padx=10, sticky=W)
        ttk.Entry(frame, textvariable=self.var_Class, width=20, font=("times new roman", 13, "bold")).grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Roll no
        Label(frame, text="Roll", font=("times new roman", 12, "bold"), bg="white").grid(row=0, column=2, padx=10, sticky=W)
        ttk.Entry(frame, textvariable=self.var_Roll, width=20, font=("times new roman", 13, "bold")).grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # Teacher name
        Label(frame, text="Teacher Name", font=("times new roman", 12, "bold"), bg="white").grid(row=1, column=2, padx=10, sticky=W)
        ttk.Entry(frame, textvariable=self.var_Teacher_name, width=20, font=("times new roman", 13, "bold")).grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # Radio buttons
        self.var_radio1 = StringVar()
        ttk.Radiobutton(frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes").grid(row=3, column=0)
        ttk.Radiobutton(frame, variable=self.var_radio1, text="No Photo Sample", value="No").grid(row=3, column=1)

        # Button frame
        btn_frame = Frame(frame, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=120, width=650, height=30)
        Button(btn_frame, text="Save", command=self.add_data, width=15, font=("times new roman", 13, "bold"),
                bg="green", fg="white").grid(row=0, column=0)
        Button(btn_frame, text="Update", width=15, command=self.update, font=("times new roman", 13, "bold"),
                bg="green", fg="white").grid(row=0, column=1)
        Button(btn_frame, text="Delete", width=15, command=self.delete, font=("times new roman", 13, "bold"),
                bg="green", fg="white").grid(row=0, column=2)
        Button(btn_frame, text="Reset", width=18, command=self.reset, font=("times new roman", 13, "bold"),
                bg="green", fg="white").grid(row=0, column=3)

        # Buttons Frame for photo generation
        btn_frame1 = Frame(frame, bd=2, relief=RIDGE)
        btn_frame1.place(x=0, y=150, width=650, height=30)
        Button(btn_frame1, text="Take Photo Sample", width=32, font=("times new roman", 13, "bold"),
                bg="blue", fg="white", command=self.generate_dataset).grid(row=0, column=0)
        Button(btn_frame1, text="Update Photo Sample", width=32, font=("times new roman", 13, "bold"),
                bg="blue", fg="white").grid(row=0, column=1)

    def add_data(self):
        # Method to add student data into the database
        if self.var_Dep.get()=="Select Department" or  self.var_Name.get()=="" or self.var_Roll.get()=="":
            messagebox.showerror("Error","All fields are required", parent=self.root)
        else:
            try:
                conn=mysql.connector.Connect(host="localhost", username="root", password="gasab1431@5", database="new_face_recognizer")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s, %s, %s, %s, %s, %s, %s, %s)", (
                self.var_Dep.get(),
                self.var_course.get(),
                self.var_Year.get(),
                self.var_Name.get(),
                self.var_Class.get(),
                self.var_Roll.get(),
                self.var_Teacher_name.get(),
                self.var_radio1.get()

                    ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "student details has been added sucessfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to:{str(es)}", parent=self.root)

    #fetch data
    def fetch_data(self):
        conn = mysql.connector.Connect(host="localhost", username="root", password="gasab1431@5",
                                       database="new_face_recognizer")
        my_cursor = conn.cursor()
        my_cursor.execute(" Select * from student")
        data=my_cursor.fetchall()
        if len(data)!=0:
            self.Student_table.delete(*self.Student_table.get_children())
            for i in data:
                self.Student_table.insert("", END, values=i)
            conn.commit()
        conn.close()
    def update(self):
        if self.var_Dep.get()=="Select Department" or  self.var_Name.get()=="" or self.var_Roll.get()=="":
            messagebox.showerror("Error","All fields are required", parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update", "Do you want to update this student details", parent=self.root)
                if Update>0:
                    conn = mysql.connector.Connect(host="localhost", username="root", password="gasab1431@5",
                                           database="new_face_recognizer")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set dep=%s, course=%s, Year=%s, Name=%s, Class=%s,  Teacher_name=%s, Photo_sample=%s where Roll=%s",(
                        self.var_Dep.get(),
                        self.var_course.get(),
                        self.var_Year.get(),
                        self.var_Name.get(),
                        self.var_Class.get(),

                        self.var_Teacher_name.get(),
                        self.var_radio1.get(),
                        self.var_Roll.get(),
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success", "Student details successfully completed", parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except  Exception as es:
                messagebox.showerror("Error", f"Due to:{str(es)}", parent=self.root)

    def delete(self):
        if self.var_Roll.get()=="":
            messagebox.showerror("Error", "Student Roll must be required", parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student Delete Page", "Do you want to delete this student", parent=self.root)
                if delete>0:
                    conn = mysql.connector.Connect(host="localhost", username="root", password="gasab1431@5",
                                           database="new_face_recognizer")
                    my_cursor = conn.cursor()
                    sql="delete from student where Roll=%s"
                    val=(self.var_Roll.get(),)
                    my_cursor.execute(sql, val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete", "Successfully deleted student details", parent=self.root)
            except  Exception as es:
                messagebox.showerror("Error", f"Due to:{str(es)}", parent=self.root)


    def reset(self):
        # Method to reset the form
        pass

    def preprocess_face(self, face_img):
        """Preprocess the face image."""
        try:
            # Denoise the image
            face_img = cv2.fastNlMeansDenoisingColored(face_img, None, 10, 10, 7, 21)

            # Resize image
            face_img = cv2.resize(face_img, (160, 160))  # Adjust size as needed
            face_img = np.array(face_img).astype('float32')
            face_img = (face_img - 127.5) / 128.0  # Normalize
            face_img = np.transpose(face_img, (2, 0, 1))  # Change to CxHxW
            face_img = torch.tensor(face_img).unsqueeze(0)  # Add batch dimension

            return face_img
        except Exception as e:
            print(f"Error in preprocessing face: {str(e)}")
            return None

    def augment_image(self, img):
        """Augment the image for training."""
        try:
            # Rotate image
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            return img
        except Exception as e:
            print(f"Error in augmenting image: {str(e)}")
            return img

    def generate_dataset(self):
        if self.var_Dep.get() == "Select Department" or self.var_Name.get() == "" or self.var_Roll.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return

        try:
            # Create a directory for the student using their roll number
            student_dir = os.path.join("data", self.var_Roll.get())
            print(f"Creating directory: {student_dir}")  # Debug line
            os.makedirs(student_dir, exist_ok=True)

            cap = cv2.VideoCapture(2)
            img_id = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                boxes, _ = self.mtcnn.detect(frame)
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box)
                        face = frame[y1:y2, x1:x2]

                        # Preprocess face
                        face_img = self.preprocess_face(face)
                        if face_img is None:
                            continue

                        img_id += 1
                        file_name_path = os.path.join(student_dir, f"user.{self.var_Roll.get()}.{img_id}.jpg")
                        print(f"Saving file: {file_name_path}")  # Debug line
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(frame, str(img_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        cv2.imshow("Face Capture", frame)
                        print(f"Faces detected: {len(boxes)}")
                else:
                    print("No faces detected.")
                if cv2.waitKey(1) == 13 or img_id >= 100:
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Generating dataset completed!")
        except Exception as e:
            messagebox.showerror("Error", f"Due to: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
