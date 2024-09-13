import os
import numpy as np
import torch
import cv2
from facenet_pytorch import InceptionResnetV1, MTCNN
from scipy.spatial.distance import cosine
import json
from PIL import Image, ImageEnhance, ImageFilter
from tkinter import Tk, Button, Label
from time import strftime
from datetime import date, datetime
import mysql.connector

# Initialize MTCNN and FaceNet model
mtcnn = MTCNN(keep_all=True)
facenet = InceptionResnetV1(pretrained='vggface2').eval()

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x100+500+200")
        self.root.title("Face Recognition System")

        # Create a button to trigger face recognition
        self.recognize_button = Button(self.root, text="Recognize Face", command=self.start_face_recognition,
                                       font=("times new roman", 15))
        self.recognize_button.pack(pady=20)

        # Label to display messages
        self.message_label = Label(self.root, text="", font=("times new roman", 12), fg="green")
        self.message_label.pack(pady=20)

    def load_all_embeddings(self):
        """Load embeddings for all stored roll numbers."""
        embeddings_data = {}
        for filename in os.listdir('.'):
            if filename.startswith('embeddings_') and filename.endswith('.json'):
                roll_number = filename.split('_')[1].split('.')[0]
                with open(filename, 'r') as f:
                    embeddings_list = json.load(f)
                    embeddings_data[roll_number] = np.array(embeddings_list, dtype=np.float32)
        return embeddings_data

    def preprocess_face(self, img):
        """Preprocess the face image."""
        try:
            img_pil = Image.fromarray(img)

            # Enhance image quality
            enhancer = ImageEnhance.Contrast(img_pil)
            img_pil = enhancer.enhance(2.0)  # Increase contrast
            enhancer = ImageEnhance.Brightness(img_pil)
            img_pil = enhancer.enhance(1.5)  # Increase brightness

            # Sharpen the image
            img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=1, percent=150))  # Adjust sharpness

            img = np.array(img_pil)
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img_gray = cv2.equalizeHist(img_gray)
            img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
            img = cv2.GaussianBlur(img, (5, 5), 0)

            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
            img_yuv[:, :, 0] = clahe.apply(img_yuv[:, :, 0])
            img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)

            img = cv2.resize(img, (160, 160))
            img = np.array(img).astype('float32')
            img = (img - 127.5) / 128.0
            img = np.transpose(img, (2, 0, 1))
            img = torch.tensor(img).unsqueeze(0)
            return img
        except Exception as e:
            print(f"Error in preprocessing face: {str(e)}")
            return None

    def get_student_info(self, Roll):
        """Fetch the student's name and class from the database using the roll number."""
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="gasab1431@5", database="new_face_recognizer")
            cursor = conn.cursor()

            # Fetch the name and class from the database
            query = "SELECT Name, Class FROM student WHERE Roll = %s"
            cursor.execute(query, (Roll,))
            result = cursor.fetchone()

            if result:
                Name, Class = result
                return Name, Class
            else:
                return None, None
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None, None
        finally:
            cursor.close()
            conn.close()

    def recognize_face(self, img):
        """Recognize face in the given image and return the roll number if matched."""
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes, _ = mtcnn.detect(img_rgb)

            recognized_rolls = set()  # Set to track already recognized roll numbers

            if boxes is not None:
                for box in boxes:
                    x, y, w, h = map(int, box)
                    face = img[y:h, x:w]

                    face_img = self.preprocess_face(face)
                    if face_img is None:
                        continue

                    embedding = facenet(face_img).detach().numpy().flatten()
                    if embedding.size != 512:
                        print(f"Generated embedding size is invalid: {embedding.size}")
                        return None, None

                    # Step 3: Automatically compare embedding with all stored embeddings
                    stored_embeddings = self.load_all_embeddings()

                    min_distance = float('inf')
                    recognized_roll_number = None

                    for Roll, embeddings in stored_embeddings.items():
                        for stored_embedding in embeddings:
                            if stored_embedding.size != 512:
                                print(f"Invalid stored embedding size: {stored_embedding.size}. Skipping...")
                                continue

                            # Calculate cosine distance between the embeddings
                            distance = cosine(embedding, stored_embedding)
                            print(f"Comparing with Roll Number {Roll}, Distance: {distance}")
                            if distance < 0.3:  # Threshold for face match
                                if distance < min_distance:
                                    min_distance = distance
                                    recognized_roll_number = Roll

                    # Check if the roll number is already recognized
                    if recognized_roll_number and recognized_roll_number not in recognized_rolls:
                        recognized_rolls.add(recognized_roll_number)  # Add to the set of processed rolls
                        Name, Class = self.get_student_info(recognized_roll_number)
                        if Name and Class:
                            # Display Name
                            cv2.putText(img, f'Name: {Name}', (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0),
                                        2)

                            # Display Class below Name
                            cv2.putText(img, f'Class: {Class}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0),
                                        2)

                            # Display Roll number below Class
                            cv2.putText(img, f'Roll no: {recognized_roll_number}', (x, y + 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                            self.mark_attendance(recognized_roll_number, Name, Class)
                        print(
                            f"Recognized student with Roll No: {recognized_roll_number}, Name: {Name}, Class: {Class}")

            print("No matching face found")
            return None, None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None, None

    def mark_attendance(self, Roll, Name, Class):
        try:
            file_name = "Gaurab.csv"
            print(f"Attempting to mark attendance for Roll No: {Roll}, Name:{Name}, Class:{Class}")

            # Check if the roll number is already present in the file
            existing_rolls = set()
            if os.path.exists(file_name):
                with open(file_name, "r") as f:
                    lines = f.readlines()
                    existing_rolls = {line.split(",")[0] for line in lines}

            if Roll not in existing_rolls:
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                date_string = now.strftime("%d/%m/%Y")

                # Write the attendance record
                with open(file_name, "a") as f:
                    f.write(f"{Roll},{Name},{Class},{dt_string},{date_string},Present\n")
                    print(f"Marked attendance for Roll No: {Roll}, Name:{Name}, Class:{Class}")
            else:
                print(f"Roll No: {Roll} already marked as present.")
        except Exception as e:
            print(f"Error in marking attendance: {str(e)}")

    def start_face_recognition(self):
        """Start the face recognition process using webcam."""
        cap = cv2.VideoCapture(2)
        if not cap.isOpened():
            print("Error: Unable to open video stream.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture image.")
                break

            roll_number, bbox = self.recognize_face(frame)
            if roll_number and bbox:
                x, y, w, h = bbox
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
                cv2.putText(frame, f'Roll No: {roll_number}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0),
                            2)

            cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) == 13:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
