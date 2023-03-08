import os
import io
import time
import picamera
import cv2
import numpy as np

fileName = ""
stream = io.BytesIO()
camera = picamera.PiCamera()
camera.start_preview()
camera.resolution = (320, 240)
time.sleep(1)

def takePicture() : # 사진 촬영하는 함수
        global fileName, stream, camera

        if len(fileName) != 0:
                os.unlink(fileName)

        stream.seek(0)
        stream.truncate()
        camera.capture(stream, format='jpeg', use_video_port=True)
        data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        takeTime = time.time()
        fN = "./static/%d" % (takeTime * 10)
        fileName =  fN + ".jpg"
        cv2.imwrite(fileName, image)
        return fileName

def remakePicture() : # 얼굴 인식하는 함수
        haar = cv2.CascadeClassifier('./haarCascades/haar-cascade-files-master/haarcascade_frontalface_default.xml')
        image2 = cv2.imread(fileName)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        
        faces = haar.detectMultiScale(image2_gray,1.1,3)

        for x, y, w, h in faces:
                cv2.rectangle(image2, (x, y), (x + w, y + h), (255, 0, 0), 2)

        reFileName = fileName.replace('.jpg', 're.jpg')
        cv2.imwrite(reFileName, image2)
        return reFileName

if __name__ == '__main__' :
        while(True):
                name = takePicture()
                print("fname= %s" % name)
