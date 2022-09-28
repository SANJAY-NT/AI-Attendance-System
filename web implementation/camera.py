import cv2

import cap as cap
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'train_images'
images = []
Names = []
myList = os.listdir('./train_images')

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    Names.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for im in images:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(im)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList =[]
        for line in myDataList:
            entry = line.strip().split(',')
            nameList.append(entry[0])
        print(nameList)
        if name not in nameList:
            now = datetime.now()
            dt_string = now.strftime('%I:%M:%S')
            f.writelines(f'\n{name},{dt_string}')


class VideoCamera(object):

    # initialize camera
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    # closing camera
    def __del__(self):
        self.video.release()

    # read frames from webcame and send it to browser
    def get_frame(self):
        ret, frame = self.video.read()

        #######################################################
        
        encodeListKnow = findEncodings(images)

        # success, img = cap.read()
        ims = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(ims)
        encodesCurFrame = face_recognition.face_encodings(ims, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = Names[matchIndex].upper()

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)


        #######################################################

        # image coming out are number/ matrixs, so we need to convert it to jpg
        ret, jpeg = cv2.imencode('.jpg', frame)
        # sending data in byte format to the browser
        return jpeg.tobytes()