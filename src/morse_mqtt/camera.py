#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)

    while (True):
        # Capture frame-by-frame
        ret, frame = capture.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

        # Print out a greyscale 'brightness' sum
        print(cv2.sumElems(thresh)[0])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
