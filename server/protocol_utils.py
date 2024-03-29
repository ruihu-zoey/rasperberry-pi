import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import numpy as np
import json

def on_connect(client, userdata, flags, rc):
    global mqtt_topic
    print("Connected with result code "+str(rc)) 
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    global message
    global count1
    x = msg.payload.decode("utf-8") ##test
    x = json.loads(x)
    x = np.asarray(x)
    message.append(x)
    if len(message)>count:
        client.loop_stop()

def receive(server_ip,topic, port, self_name,time1,count):
    global mqtt_topic
    global message
    global count1

    
    count1 = count
    message = []
    mqtt_topic = topic
    client = mqtt.Client(self_name)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(server_ip, port, 60)
    client.loop_start()
    time1 = float(time1)
    time.sleep(time1)
    exist = len(message)
    client.loop_stop()
    return message


def send(server_ip,topic, ports, data):
    '''
    Input: data: numpy array
    '''
    data1 = json.dumps(data) #.tolist()
    publish.single(topic, data1, hostname=server_ip,port=ports)

