# publisher/subscriber
import time
import paho.mqtt.client as mqtt
import mycamera # 카메라 사진 보내기
import circuit # LED 모듈

flag = False
onOff1 = 1
onOff2 = 1

def on_connect(client, userdata, flag, rc):
        # subscribe 메시지 수신하기 위해 broker에 토픽 등록
        client.subscribe("facerecognition", qos=0)
        client.subscribe("refacerecognition", qos=0)
        client.subscribe("led", qos = 0)
        client.subscribe("ultrasonic", qos=0)
        client.subscribe("led1On", qos=0)
        client.subscribe("led1Off", qos=0)
        client.subscribe("led2On", qos=0)
        client.subscribe("led2Off", qos=0)

def on_message(client, userdata, msg) :
        # subscriber가 브로커로부터 메시지 받았을 때 실행
        global flag
        command = msg.payload.decode("utf-8")
        if command == "action" :
                print("action msg received..")
                flag = True
                circuit.controlLED(1)
        elif command == "led1On":
                circuit.LED1ON()
        elif command == "led1Off":
                circuit.LED1OFF()
        elif command == "led2On":
                circuit.LED2ON()
        elif command == "led2Off":
                circuit.LED2OFF()
        
broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.on_connect = on_connect # 콜백 등록
client.on_message = on_message # 콜백 등록

client.connect(broker_ip, 1883)
client.loop_start()

while True :
        if flag==True :
                # publish 토픽과 함께 메시지 데이터 전송
                imageFileName = mycamera.takePicture() # 카메라 사진 촬영
                client.publish("image", imageFileName, qos=0)
                reImageFileName = mycamera.remakePicture() # 얼굴 인식
                client.publish("reImage", reImageFileName, qos=0)
                ledcomplete = circuit.ledComplete() # LED(조명)
                client.publish("led",ledcomplete, qos=0)
                distance = circuit.measureDistance() # 거리 측정
                client.publish("ultrasonic", distance, qos=0)
                temp = circuit.getTemperature() # 온도
                client.publish("temperature", temp, qos=0)
                hum = circuit.getHumidity() # 습도
                client.publish("humidity", hum, qos=0)
                ill = circuit.getIlluminance() # 조도
                client.publish("illuminance", ill, qos=0)
                
                flag = False
        time.sleep(1) # 1초 잠자기

client.loop_end()
client.disconnect()