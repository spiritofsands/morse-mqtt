import paho.mqtt.client as mqtt
from time import time

class MqttReceiver:
    def __init__(self, host, topic, queue):
        self.host = host
        self.topic = topic
        # class variable so on_message could be used
        MqttReceiver.queue = queue

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe

    @staticmethod
    def get_queue():
        if MqttReceiver.queue is None:
            raise "No queue was provided"
        return MqttReceiver.queue

    @staticmethod
    def _on_connect(_client, _userdata, _flags, rc):
        print('Connected with result code ' + str(rc))

    @staticmethod
    def _on_message(_client, _userdata, msg):
        MqttReceiver.get_queue().put({time(): msg.payload})

    @staticmethod
    def _on_subscribe(_client, _userdata, _mid, _granted_qos):
        print('Subscribed')

    def connect_loop(self):
        self.client.connect(self.host)
        self.client.subscribe(self.topic)
        self.client.loop_forever()
