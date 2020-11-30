import time
import Adafruit_DHT
from datetime import date, datetime 
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient




myMQTTClient = AWSIoTMQTTClient("MarinClientID")
myMQTTClient.configureEndpoint("axdy6b5vxgdrs-ats.iot.us-east-1.amazonaws.com", 8883) #provide arn
myMQTTClient.configureCredentials("/home/pi/termproj/PI_IOT_Cert/AmazonRootCA1.pem", "/home/pi/termproj/PI_IOT_Cert/private.pem.key", "/home/pi/termproj/PI_IOT_Cert/certificate.pem.crt") 
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

print('Initiating Iot Core Topic ...')
myMQTTClient.connect()
pin = 21
sensor = Adafruit_DHT.DHT11
connecting_time = time.time() + 10
if time.time() < connecting_time:  #try connecting to AWS for 10 seconds
    myMQTTClient.connect()
    myMQTTClient.publish("DHT11/info", "connected", 0)
    print ("MQTT Client connection success!")
else:
    print ("Error: Check your AWS details in the program")
time.sleep(2)
while 1:
    now = datetime.utcnow()
    current_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    time.sleep(2) #Wait for 2 sec then update the values
    payload = '{ "timestamp": "' + current_time + '","temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ' }'
    print (payload) 
    myMQTTClient.publish("DHT11/data", payload, 0)
    time.sleep(2)

