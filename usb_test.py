
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:26:52 2023

@author: legend159
"""

import cv2

cam_index = 0
def main():
    cap = cv2.VideoCapture(cam_index)

    if not cap.isOpened():
        print("Camera can't open\nexit")
        return -1

    cap.set(cv2.CAP_PROP_EXPOSURE, -1)  # -1 sets exposure_time to auto
    cap.set(cv2.CAP_PROP_GAIN, -1)  # -1 sets gain to auto

    while True:
        ret, frame = cap.read()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BayerBG2BGR)  # for RGB camera demosaicing

        
        cv2.imshow("press q to quit", frame)
        key = cv2.waitKey(30)
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
