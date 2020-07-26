import random
import time

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=HealthMonitor.azure-devices.net;DeviceId=HealthMonitor;SharedAccessKey=uB7JGL5A0LZ82p/P2l+cKnte0FEzP6nVhnEvk7vPPWY="
HEART_RATE = 80
DIASTOLIC_BP = 70
SYSTOLIC_BP = 105
BODY_TEMP = 37
MSG_TXT = '{{"heart_rate": {heart_rate}, "diastolic_bp": {diastolic_bp}, "systolic_bp": {systolic_bp}, "body_temp": {body_temp}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run(age):
    try:
        client = iothub_client_init()
        print("Health Monitor sending periodic messages, press Ctrl-C to exit")

        while True:
            heart_rate = random.normalvariate(HEART_RATE, 5)
            diastolic_bp = random.normalvariate(DIASTOLIC_BP, 4)
            systolic_bp = random.normalvariate(SYSTOLIC_BP, 4)
            body_temp = random.normalvariate(BODY_TEMP, 1)
            msg_txt_formatted = MSG_TXT.format(heart_rate = heart_rate, diastolic_bp = diastolic_bp, systolic_bp = systolic_bp, body_temp = body_temp)
            message = Message(msg_txt_formatted)

            # based on https://www.livescience.com/42081-normal-heart-rate.html
            if heart_rate < 60:
                message.custom_properties["heartRateAlert"] = "too slow"
            elif heart_rate <= (220 - age) * 0.85:
                message.custom_properties["heartRateAlert"] = "normal"
            else:
                message.custom_properties["heartRateAlert"] = "too fast"
            
            # based on http://www.bloodpressureuk.org/BloodPressureandyou/Thebasics/Bloodpressurechart
            if diastolic_bp < 60 and systolic_bp < 90:
                message.custom_properties["bloodPressureAlert"] = "low"
            elif diastolic_bp <= 80 and systolic_bp <= 120:
                message.custom_properties["bloodPressureAlert"] = "ideal"
            elif diastolic_bp <= 90 and systolic_bp <= 140:
                message.custom_properties["bloodPressureAlert"] = "pre-high"
            else:
                message.custom_properties["bloodPressureAlert"] = "high"

            # based on https://en.wikipedia.org/wiki/Human_body_temperature
            if body_temp < 35:
                message.custom_properties["temperatureAlert"] = "hypothermia"
            elif body_temp < 38:
                message.custom_properties["temperatureAlert"] = "normal"
            elif body_temp < 39:
                message.custom_properties["temperatureAlert"] = "fever"
            elif body_temp < 40:
                message.custom_properties["temperatureAlert"] = "hyperthermia"
            else:
                message.custom_properties["temperatureAlert"] = "hyperpyrexia"

            print("Sending message: {}".format(message))
            client.send_message(message)
            print("Message successfully sent")
            time.sleep(5)

    except KeyboardInterrupt:
        print("Health Monitor stopped")

def get_age():
    age = input("Enter the age of your simulated patient: ")
    try:
        age = int(age)
        if (age < 0 or age > 130):
            print("Please enter a number between 0 and 130")
            exit(1)
    except ValueError:
        print("Please enter an integer")
        exit(1)

    return age

if __name__ == '__main__':
    print("Health Monitor - Simulated device")
    age = get_age()
    print("Press Ctrl-C to exit")
    iothub_client_telemetry_sample_run(age)