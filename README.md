# Face-Recognition-using-MTCNN-Facenet-in-Python
This is the project for face detection and recognition  using Python Programming. 
Please use the code in the folowing way:
1. first.py
It is used to create the backgroup of the app. It includes student details, filter, student, attendance and face_recognition button.

2. student.py
  It is used to create a button for student details. Inside it we can use the student information and use it to take photos. The photos are detected with the help of mtcnn module. And, detected photos are stored in a folder, which then can be used for recognition.
   
3. filter.py
  The photo we took can be filtered with the help of filter button.
   
4. capture.py
  This file is used for generating embedding from the stored photos after they have been given for filter.

5. face_recognition.py
   This is used to recognize face. Here, the code will compare the stored embedding with the embedding of recognized face and due to which our face is recognized. Facenet is used to perform this operation.
   
6. attendance.py
     Finally, the attendance is shown in this file.Present is given for those whose face are recognized.
