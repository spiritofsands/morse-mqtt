#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from threading import Timer
from time import time


class MqttReceiver:
    def __init__(self, host, topic, queue):
        self.host = host
        self.topic = topic
        self.queue = queue

        # class variable so on_message could be used
        self.events = []

        self.client = mqtt.Client()
        self.client.on_connect = lambda client, userdata, flags, rc: self._on_connect(
            client, userdata, flags, rc)
        self.client.on_message = lambda client, userdata, msg: self._on_message(
            client, userdata, msg)
        self.client.on_subscribe = lambda client, userdata, mid, granted_qos: self._on_subscribe(
            client, userdata, mid, granted_qos)

        # hardcode message timemout for now
        self.timer = Timer(1, lambda: self._message_complete())

    def _message_complete(self):
        self.queue.put(self.events)
        self.events = []

    def _on_connect(self, _client, _userdata, _flags, rc):
        print('Connected with result code ' + str(rc))

    def _on_message(self, _client, _userdata, msg):
        self.timer.cancel()
        self.events.append({time(): msg.payload})
        self.timer = Timer(1, lambda: self._message_complete())
        self.timer.start()

    def _on_subscribe(self, _client, _userdata, _mid, _granted_qos):
        print('Subscribed')

    def connect_loop(self):
        self.client.connect(self.host)
        self.client.subscribe(self.topic)
        self.client.loop_forever()
