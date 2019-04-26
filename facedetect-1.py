# -*- coding: utf-8 -*-
# @sa https://www.tech-tech.xyz/haar-cascade.html
import cv2
img = cv2.imread('D:/work/tool/python/openCvPython/family-2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#カスケードファイルの読み込み
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
# haarcascade_frontalface_default.xml
#カスケードファイルと使って顔認証
scaleFactor=1.1
minNeighbours=5
flags=0
minSize=(2,2)
maxSize=(100,100)
#
faces = face_cascade.detectMultiScale(gray,scaleFactor,minNeighbours,flags,minSize,maxSize)
#faces = face_cascade.detectMultiScale(gray)
for (x,y,w,h) in faces:
    #顔部分を四角で囲う
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
