#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2


class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

    def __del__(self):
        self.capture.release()

    def stream_brightness(self, threshold=250):
        while True:
            # Capture frame
            _, frame = self.capture.read()

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Binary threshold the frame
            _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

            # Get greyscale 'brightness' sum
            v, _, _, _ = cv2.sumElems(thresh)

            print(v)


if __name__ == '__main__':
    c = Camera()
    c.stream_brightness()
