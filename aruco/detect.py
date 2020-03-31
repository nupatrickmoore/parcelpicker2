import cv2
import numpy as np

#numpy display precision
np.set_printoptions(precision=3, suppress=True)

#camera config from calibration
mtx = np.matrix([[5.50267427e+03, 0.00000000e+00, 3.23755083e+02],
                 [0.00000000e+00, 5.06413237e+03, 2.37283549e+02],
                 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.matrix([[-4.56265641e+00,
                   3.17800401e+03,
                   -1.80528193e-01,
                   -1.89096460e-01,
                   2.01299949e+01]])

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_EXPOSURE, -6)

#Parameters for aruco codes
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
params =  cv2.aruco.DetectorParameters_create()

while True:
    ret, frame = cam.read() #get image from camera
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert image ot grayscale
    corners, ids, rejects = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=params) #Detect aruco

    if np.all(ids != None):
        frame = cv2.aruco.drawDetectedMarkers(frame, corners) #Draw corners for visualisation
        rvec, tvec ,_ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05, mtx, dist)
        for i in range(ids.size):
            cv2.aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.01)
            frame = cv2.putText(frame, str(tvec[i]), (int(corners[i][0][0][0]-50), int(corners[i][0][0][1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 

    cv2.imshow('frame', frame) #show image in window
    if cv2.waitKey(1) & 0xFF == ord('q'): #q button quits
        break



#Cleanup    
cam.release()
cv2.destroyAllWindows()


# References
# 1. https://docs.opencv.org/3.4.0/d5/dae/tutorial_aruco_detection.html
