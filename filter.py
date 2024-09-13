import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
from tkinter import Tk, Button, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from tkinter import *
import cv2
from PIL import Image

class Filter:

    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")
        self.root.title("Image Filtering")

        # bg image
        img3 = Image.open(r"C:\Users\User\PycharmProjects\pythonProject\pexels-kaip-1341279.jpg")
        img3 = img3.resize((300, 200))
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=300, height=200)

        # Create a button to start image filtering
        self.filter_button = Button(self.root, text="Click to Filter Images", command=self.start_image_filtering,
                                    font=("times new roman", 15), bg="green")
        self.filter_button.pack(pady=20)

    def apply_clahe(self, image):
        """Apply CLAHE to improve contrast."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    def enhance_image(self, image):
        """Enhance the image quality using various techniques."""
        # Apply CLAHE for better contrast in uneven lighting
        image = self.apply_clahe(image)

        # Convert to PIL Image for easier manipulation
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Enhance brightness
        enhancer = ImageEnhance.Brightness(pil_image)
        pil_image = enhancer.enhance(1.2)  # Adjust brightness

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.5)  # Increase contrast

        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(2.0)  # Increase sharpness

        # Convert back to OpenCV format
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Optional: Denoise
        image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

        return image

    def process_and_save_images_for_roll(self, roll_number, base_directory):
        """Process and save images for a specific roll number."""
        roll_directory = os.path.join(base_directory, roll_number)

        if not os.path.exists(roll_directory):
            messagebox.showerror("Error", f"No directory found for roll number: {roll_number}")
            return

        for filename in os.listdir(roll_directory):
            if filename.endswith(".jpg"):
                file_path = os.path.join(roll_directory, filename)

                # Read the image
                image = cv2.imread(file_path)
                if image is None:
                    print(f"Failed to load image: {file_path}")
                    continue

                # Enhance the image
                enhanced_image = self.enhance_image(image)

                # Save the enhanced image
                output_path = os.path.join(roll_directory, f"user_{filename}")
                cv2.imwrite(output_path, enhanced_image)
                print(f"Processed and saved: {output_path}")

        messagebox.showinfo("Success", f"Images for roll number {roll_number} have been processed and saved.")

    def start_image_filtering(self):
        """Start the image filtering process."""
        # Prompt user to select base directory
        base_directory = r"C:\Users\User\PycharmProjects\pythonProject\data"
        if not base_directory:
            messagebox.showwarning("Warning", "No directory selected.")
            return

        # Prompt user to enter roll number
        roll_number = simpledialog.askstring("Input", "Enter Roll Number:")
        if not roll_number:
            messagebox.showwarning("Warning", "No roll number entered.")
            return

        # Process and save images
        self.process_and_save_images_for_roll(roll_number, base_directory)


if __name__ == "__main__":
    # Create the main Tkinter window
    root = Tk()
    obj=Filter(root)
    # Create an instance of the Filter class
    filter_instance = Filter(root)

    # Start the Tkinter event loop
    root.mainloop()
