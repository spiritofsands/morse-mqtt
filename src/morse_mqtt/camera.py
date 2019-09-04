#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
import cv2


class BufferedMean:
    def __init__(self, maxlen):
        self.buffer = deque(maxlen=maxlen)
        self.sum = 0
        self.count = 0

    def push(self, value):
        if self.count == self.buffer.maxlen:
            self.sum -= self.buffer[0]
        else:
            self.count += 1

        self.buffer.append(value)
        self.sum += value

    def is_full(self):
        return self.count == self.buffer.maxlen

    def mean(self):
        return self.sum / self.count


class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.brightness = BufferedMean(100)

    def __del__(self):
        self.capture.release()

    def stream_brightness(self, binary_threshold=250, light_threshold=1.2):
        while True:
            # Capture frame
            _, frame = self.capture.read()

            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Binary threshold the frame
            _, thresh = cv2.threshold(gray, binary_threshold, 255,
                                      cv2.THRESH_BINARY)

            # Get greyscale 'brightness' sum
            v, _, _, _ = cv2.sumElems(thresh)

            self.brightness.push(v)

            is_light_on = (v / self.brightness.mean()) > light_threshold

            print("ON? {} count: {}, background: {}, value: {}".format(
                is_light_on, self.brightness.count,
                int(self.brightness.mean()), int(v)))


if __name__ == '__main__':
    c = Camera()
    c.stream_brightness()
