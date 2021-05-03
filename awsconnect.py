from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import pigpio
import RPi.GPIO as GPIO
import serial
import time
from datetime import date, datetime
 
host = "asj6rxy47hoyr-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/pi/certificate/"
clientId = "pi-demo-publisher"
topic = "demo-topic"
#payload3 = "tempPayload"
payload1 = "lightPayload"
#payload2 = "waterPayload"
 
# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("{}Amazon-root-CA-1.pem".format(certPath), "{}private.pem.key".format(certPath), "{}device.pem.crt".format(certPath))
 
# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()
 
# Publish to the same topic
def send_AWS(trigger_info, weather):
    now = datetime.utcnow()
    current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ') #save current time
    message = {}
    message['Threshold Temp'] = trigger_info
    message['city'] = weather[0]
    message['country'] = weather[1]
    message['temperature'] = weather[3]
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(payload1, messageJson, 1) #send to aws
    print('Published topic %s: %s\n' % (payload1, messageJson))
    #myAWSIoTMQTTClient.disconnect()
