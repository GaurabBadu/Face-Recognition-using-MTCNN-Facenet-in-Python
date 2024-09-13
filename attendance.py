from tkinter import *
import os
import csv
from tkinter import filedialog, messagebox

mydata = []


class Attendance:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Attendance Report")

        # Add a button to trigger the importCsv method
        import_btn = Button(self.root, text="Import CSV", command=self.importCsv, font=("Arial", 15), bg="blue",
                            fg="white")
        import_btn.pack(pady=20)

        # Text widget to display the imported data
        self.text_box = Text(self.root, width=100, height=20)
        self.text_box.pack(pady=20)

    def importCsv(self):
        global mydata
        mydata.clear()  # Clear the old data

        # Open file dialog to select CSV file
        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Open CSV",
            filetypes=[("CSV File", "*.csv"), ("All Files", "*.*")]
        )

        # Check if a file was selected
        if fln:
            with open(fln, mode='r') as myfile:
                csvread = csv.reader(myfile, delimiter=",")
                for row in csvread:
                    mydata.append(row)
            print("Data imported from CSV:", mydata)  # To verify data
            self.display_data()  # Call the function to display data
        else:
            print("No file selected.")
            messagebox.showwarning("Warning", "No file selected!")

    # Method to display data in the Text widget
    def display_data(self):
        self.text_box.delete('1.0', END)  # Clear any previous data
        if mydata:
            for row in mydata:
                self.text_box.insert(END, ", ".join(row) + "\n")
        else:
            self.text_box.insert(END, "No data found in the CSV file.\n")


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
