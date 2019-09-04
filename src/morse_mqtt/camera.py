#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
import threading
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
        self._brightness = BufferedMean(100)
        self._brightness_thread = None
        self._stop = threading.Event()
        self._light_on = deque(maxlen=1)

    def __del__(self):
        self.stop_thread.set()
        self.capture.release()

    def is_light_on(self):
        try:
            return self._light_on[0]
        except IndexError:
            return False

    def stream_brightness(self, binary_threshold=250, light_threshold=1.2):
        if self._brightness_thread is not None:
            return

        def capture_brightness_impl(binary_threshold, light_threshold):
            while not self._stop.is_set():
                # Capture frame
                _, frame = self.capture.read()

                # Convert frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Binary threshold the frame
                _, thresh = cv2.threshold(gray, binary_threshold, 255,
                                          cv2.THRESH_BINARY)

                # Get greyscale 'brightness' sum
                v, _, _, _ = cv2.sumElems(thresh)

                self._brightness.push(v)

                # Push to the current light status to the 1-element queue
                self._light_on.append(
                    (v / self._brightness.mean()) > light_threshold
                        )
                print("ON? {} count: {}, background: {}, value: {}".format(
                    self.is_light_on(), self._brightness.count,
                    int(self._brightness.mean()), int(v)))

        self.brightness_thread = threading.Thread(
            target=capture_brightness_impl,
            args=(binary_threshold, light_threshold))
        self.brightness_thread.daemon = True
        self.brightness_thread.start()


if __name__ == '__main__':
    c = Camera()
    c.stream_brightness()

    while True:
        pass
        #if c.is_light_on():
        #    print("1")
