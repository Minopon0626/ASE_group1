#sudo apt install libavutil56 libcairo-gobject2 libgtk-3-0 libqtgui4 libpango-1.0-0 libqtcore4 libavcodec58 libcairo2 libswscale5 libtiff5 libqt4-test libatk1.0-0 libavformat58 libgdk-pixbuf2.0-0 libilmbase23 libjasper1 libopenexr23 libpangocairo-1.0-0 libwebp6

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    if key == ord('s'):
        path = "photo.jpg"
        cv2.imwrite(path,frame)

cap.release()
cv2.destroyAllWindows()