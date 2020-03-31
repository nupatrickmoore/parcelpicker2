import numpy as np
import cv2 

corner_set = []
cam = cv2.VideoCapture(0)

# shape of grid
size = (6,8)
objp = np.zeros((size[0]*size[1],3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

#get pictures
while True:
    _, frame = cam.read()
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, size, None)
    cv2.drawChessboardCorners(frame, size, corners, ret)

    frame = cv2.putText(frame, str(len(corner_set)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA) 

    cv2.imshow("img", frame)
    
    if (cv2.waitKey(1) & 0xFF == ord(' ')) and ret:
        corner_set.append(corners)
    if len(corner_set) >= 20:
        break

#calibrate
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([objp]*len(corner_set), corner_set, gray.shape[::-1], None, None)
print(mtx)
print(dist)

cv2.destroyAllWindows()

# References
# 1. https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html
