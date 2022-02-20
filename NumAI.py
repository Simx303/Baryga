import cv2
import os
import numpy as np
import discord.ext

img_dir = "ksi.jpg"

age_model = cv2.dnn.readNetFromCaffe("aimodels/ageproto.txt", "aimodels/dex_chalearn_iccv2015.caffemodel")
# gender_model = cv2.dnn.readNetFromCaffe("aimodels/genderproto.txt", "aimodels/dex_chalearn_iccv2015.caffemodel")
img = cv2.imread(img_dir)
img = ((img / np.max(img)) * 255).astype('uint8')
print(len(img))
haar_detector = cv2.CascadeClassifier('aimodels/haarcascade_frontalface_default.xml')
detected_face = 0
def detect_faces(imgg):
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   faces = haar_detector.detectMultiScale(imgg, 1.3, 5)
   return faces
faces = detect_faces(img)
print(len(faces))
for x, y, w, h in faces:
   detected_face = img[int(y):int(y+h), int(x):int(x+w)]

detected_face = cv2.resize(detected_face, (224, 224)) #img shape is (224, 224, 3) now
print(len(detected_face))
print(detected_face.shape)
if img is None:
    raise Exception('Image not found!')
img_blob = cv2.dnn.blobFromImage(detected_face) # img_blob shape is (1, 3, 224, 224)

age_model.setInput(img_blob)
age_dist = age_model.forward()[0]

# gender_model.setInput(img_blob)
# gender_class = gender_model.forward()[0]

output_indexes = np.array([i for i in range(0, 101)])
apparent_predictions = round(np.sum(age_dist * output_indexes), 2)

print(apparent_predictions)