#!/usr/bin/env python
# -*- coding: utf-8 -*-
from queue import Queue
from threading import Thread
from time import sleep

from morse_mqtt.receiver import MqttReceiver
from morse_mqtt.decode import Pulse, decode_pulses


def receiver(host, topic, queue):
    receiver = MqttReceiver(host, topic, queue)
    receiver.connect_loop()


# SAMPLE READER
def reader(timeout, queue):
    print("Reader started")
    while True:
        timestamps = queue.get()

        # Ignore the value and use the timestamps to create pulses
        timestamps = (a for (a, b) in timestamps)
        timestamps = [iter(timestamps)] * 2
        pulses = [Pulse(x, y) for (x, y) in zip(*timestamps)]

        print(decode_pulses(pulses))


def main():
    host = '192.168.1.103'
    topic = '+/CAR/#'
    read_timeout = 2
    queue = Queue()

    receiver_thread = Thread(target=receiver, args=(host, topic, queue))
    receiver_thread.start()

    reader_thread = Thread(target=reader, args=(read_timeout, queue))
    reader_thread.start()

    receiver_thread.join()
    reader_thread.join()


main()
