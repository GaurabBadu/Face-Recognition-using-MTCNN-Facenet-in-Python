import os
import numpy as np
import torch
import json
import cv2
from PIL import Image, ImageEnhance
from facenet_pytorch import InceptionResnetV1, MTCNN
from sklearn.preprocessing import normalize
from scipy.spatial.distance import cosine
from tkinter import Tk, Button, Label, Entry
from PIL import ImageTk

# Initialize MTCNN and FaceNet
mtcnn = MTCNN(keep_all=True)
facenet = InceptionResnetV1(pretrained='vggface2').eval()


class Capture:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x200+300+250")
        self.root.title("Face Recognition System")

        # bg image
        img3 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-kaip-1341279.jpg")
        img3 = img3.resize((500, 200))
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=500, height=200)

        # Create a label and entry for roll number
        self.roll_label = Label(self.root, text="Enter Roll Number:", font=("times new roman", 15), bg="blue")
        self.roll_label.place(x=50, y=50)

        self.roll_entry = Entry(self.root, font=("times new roman", 15))
        self.roll_entry.place(x=225, y=50, width=50)

        # Create a button to run the embedding generation process
        self.embed_button = Button(self.root, text="Click to Generate Embeddings", command=self.generate_embeddings_process,
                                   font=("times new roman", 15), bg="Green")
        self.embed_button.place(x=50, y=100)

        # Label to display a message after completion
        self.message_label = Label(self.root, text="", font=("times new roman", 15), fg="green")
        self.message_label.place(x=50, y=150)

    def generate_embeddings_process(self):
        """This function is triggered when the 'Generate Embeddings' button is pressed."""
        roll_number = self.roll_entry.get()
        print("Wait for few seconds")
        if roll_number:
            self.message_label.config(text="Wait for few seconds...")
            self.message_label.update()

            Capture.generate_and_save_embeddings(roll_number)
            self.message_label.config(text="Embedding generation completed!")  # Show message when done
        else:
            self.message_label.config(text="Please enter a roll number.", fg="red")  # Error message if no roll number

    @staticmethod
    def preprocess_face(face):
        """Preprocess the face image for embedding generation."""
        try:
            # Convert to PIL Image for enhancement
            face_img = Image.fromarray(face)

            # Enhance image quality
            enhancer = ImageEnhance.Contrast(face_img)
            face_img = enhancer.enhance(1.5)  # Increase contrast

            # Convert back to numpy array and resize
            face = np.array(face_img)
            face = cv2.resize(face, (160, 160))
            face = np.array(face).astype('float32')
            face = (face - 127.5) / 128.0
            face = np.transpose(face, (2, 0, 1))
            face = torch.tensor(face).unsqueeze(0)
            return face
        except cv2.error as e:
            print(f"Error resizing face: {str(e)}")
            return None

    @staticmethod
    def generate_and_save_embeddings(roll_number):
        """Generate and save valid face embeddings for a given roll number using enhanced images."""
        data_dir = r"C:\Users\User\PycharmProjects\pythonProject\data"
        student_dir = os.path.join(data_dir, roll_number)
        embeddings = []

        if not os.path.isdir(student_dir):
            print(f"Student directory {student_dir} does not exist.")
            return

        for img_name in os.listdir(student_dir):
            if not img_name.lower().startswith('user_user') or not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"File {img_name} is not a valid image. Skipping...")
                continue

            img_path = os.path.join(student_dir, img_name)
            try:
                img = Image.open(img_path).convert('RGB')
                img = np.array(img)

                boxes, _ = mtcnn.detect(img)
                if boxes is not None:
                    for box in boxes:
                        x, y, w, h = map(int, box)
                        face = img[y:h, x:w]

                        if face.size == 0:
                            print(f"Detected face in image {img_name} is invalid. Skipping...")
                            continue

                        face_img = Capture.preprocess_face(face)
                        if face_img is None:
                            continue

                        # Generate embedding
                        embedding = facenet(face_img).detach().numpy().flatten()

                        if embedding.size == 512:
                            embeddings.append(embedding)
                            print(f"Valid embedding generated for image {img_name}.")
                        else:
                            print(f"Invalid embedding size: {embedding.size} for image {img_name}. Discarded.")
                else:
                    print(f"No faces detected in image {img_name}.")
            except Exception as e:
                print(f"Error processing image {img_name}: {str(e)}")

        if embeddings:
            # Normalize embeddings
            embeddings = normalize(np.array(embeddings))
            Capture.save_embeddings_to_file(roll_number, embeddings)
        else:
            print(f"No valid embeddings found for Roll Number {roll_number}")

    @staticmethod
    def save_embeddings_to_file(roll_number, embeddings):
        """Save valid embeddings to a JSON file."""
        valid_embeddings = [embedding.tolist() for embedding in embeddings if embedding.shape == (512,)]

        if valid_embeddings:
            file_name = f"embeddings_{roll_number}.json"
            try:
                with open(file_name, 'w') as f:
                    json.dump(valid_embeddings, f)
                print(f"Saved valid embeddings to {file_name} for Roll Number {roll_number}")
            except Exception as e:
                print(f"Error saving embeddings to file: {str(e)}")
        else:
            print(f"No valid embeddings to save for Roll Number {roll_number}")



# Initialize the Tkinter app and run it
if __name__ == "__main__":
    root = Tk()
    app = Capture(root)
    root.mainloop()
