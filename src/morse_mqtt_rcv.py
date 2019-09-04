from morse_mqtt.mqtt_recevier import MqttReceiver

def main():
    host = '192.168.1.103'
    topic = '+/CAR/#'
    mqtt_recevier = MqttReceiver(host, topic)
    mqtt_recevier.connect_loop()


main()
