import cv2
import numpy as np
import math

def write_sheet(coords):
    c1 = coords[0], c2 = coords[1], c3 = coords[2], c4 = coords[3]
    w1 = math.sqrt((c4[0]-c3[0])**2+(c4[1]-c3[1])**2)
    w2 = math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
    h1 = math.sqrt((c3[0]-c2[0])**2+(c3[1]-c2[1])**2)
    h2 = math.sqrt((c4[0]-c1[0])**2+(c4[1]-c1[1])**2)
    w = max(int(w1), int(w2))
    h = max(int(h1), int(h2))
    return w, h

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise RuntimeError("Camera is broken")


cam.set(cv2.CAP_PROP_EXPOSURE, -4)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Background", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Delta", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Paper", cv2.WINDOW_KEEPRATIO)

bg = None
fc = 0
binary = None

while cam.isOpened():
    ret, frame = cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    if fc < 30:
        if bg is None:
            bg = gray.copy().astype("f4")
        cv2.accumulateWeighted(gray, bg, 0.2)
    else:
        bg = bg.astype("uint8")
        cv2.imshow("Background", bg)
        delta = cv2.absdiff(bg, gray)
        binary = cv2.threshold(delta, 10, 255, cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        cv2.drawContours(frame, contours, -1, (0, 255, 0))
        cv2.imshow("Delta", binary)
        
        if len(contours) > 0:
            paper = max(contours, key=cv2.contourArea)
            arcLength = 0.1 * cv2.arcLength(paper, True)
            approx = cv2.approxPolyDP(paper, arcLength, True)
        
            if len(approx) == 4:
                shape = approx.reshape(4, 2)
                coord = np.zeros((4, 2), dtype="f4")
                shape_sum = shape.sum(axis=1)
                coord [0] = shape[np.argmin(shape_sum)]  
                coord [2] = shape[np.argmax(shape_sum)]  
                shape_sum = np.diff(shape, axis=1)
                coord [1] = shape[np.argmin(shape_sum)]  
                coord [3] = shape[np.argmax(shape_sum)]  
                shape = coord
                
                c,r = write_sheet(shape)

                shape2 = np.float32([[0, 0], [c, 0], [c, r], [0, r]])
                transform = cv2.getPerspectiveTransform(shape, shape2)
                new_img = cv2.warpPerspective(frame, transform, (c, r))
            
                cv2.imshow("Paper", new_img)
        
    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('p'):
        if binary is not None:
            print("Take screenshot frame")
            cv2.imwrite("screen.png", np.hstack([frame[:, :, 0], gray, binary]))
    if key == ord('l'):
        if binary is not None:
            print("Take screenshot paper")
            cv2.imwrite("screen.png", np.hstack([paper[:, :, 0], gray, binary]))
    fc += 1

cam.release()
cv2.destroyAllWindows()
