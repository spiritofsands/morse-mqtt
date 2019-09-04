import paho.mqtt.client as mqtt

class MqttReceiver:
    def __init__(self, host, topic):
        self.host = host
        self.topic = topic

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe

    @staticmethod
    def _on_connect(client, _userdata, _flags, rc):
        print('Connected with result code ' + str(rc))

    @staticmethod
    def _on_message(_client, _userdata, msg):
        print('[' + msg.topic + ']: ' + str(msg.payload))

    @staticmethod
    def _on_subscribe(_client, _userdata, _mid, _granted_qos):
        print('Subscribed')

    def connect_loop(self):
        self.client.connect(self.host)
        self.client.subscribe(self.topic)
        self.client.loop_forever()
