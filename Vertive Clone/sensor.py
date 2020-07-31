# import package serial
import serial

import time
# import package numpy
import numpy as np
# import paho.mqtt.client
# import paho.mqtt.client as mqtt
# import json package
import json
import requests
import subprocess

time.sleep(20)

SERVER_DNS = "http://192.168.0.66:8000/data"
DATA_ENDP = "http://vertiv.vacustech.in/data"

broker = "13.233.32.234"
port = 1883
topic = "sensorsData"
gatewayMac = "5a-c2-15-d1-00-01"

byteBuffer = np.zeros(2 ** 11, dtype='uint8')
byteBufferLength = 0

oid = { "5a-c2-15-c1-00-01" : ["1.3.6.6.1.54326.2.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.49","1.3.6.6.1.54326.3.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.49",
       "1.3.6.6.1.54326.4.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.49","1.3.6.6.1.54326.5.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.49"] ,
        "5a-c2-15-c1-00-02" : ["1.3.6.6.1.54326.2.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.50","1.3.6.6.1.54326.3.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.50",
        "1.3.6.6.1.54326.4.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.50","1.3.6.6.1.54326.5.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.50"] ,
        "5a-c2-15-c1-00-03" : ["1.3.6.6.1.54326.2.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.51","1.3.6.6.1.54326.3.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.51",
        "1.3.6.6.1.54326.4.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.51","1.3.6.6.1.54326.5.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.51"] ,
        "5a-c2-15-c1-00-04":["1.3.6.6.1.54326.2.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.52","1.3.6.6.1.54326.3.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.52",
       "1.3.6.6.1.54326.4.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.52","1.3.6.6.1.54326.5.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.52"] , 
       "5a-c2-15-c1-00-05":["1.3.6.6.1.54326.2.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.53","1.3.6.6.1.54326.3.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.53",
       "1.3.6.6.1.54326.4.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.53","1.3.6.6.1.54326.5.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.53"] , 
       "5a-c2-15-c1-00-06":["1.3.6.6.1.54326.2.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.54","1.3.6.6.1.54326.3.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.54",
       "1.3.6.6.1.54326.4.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.54","1.3.6.6.1.54326.5.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.54"] , 
       "5a-c2-15-c1-00-07":["1.3.6.6.1.54326.2.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.55","1.3.6.6.1.54326.3.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.55",
       "1.3.6.6.1.54326.4.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.55","1.3.6.6.1.54326.5.17.53.97.45.99.50.45.49.53.45.99.49.45.48.48.45.48.55"] }


def getIpAddress():
    with open("/home/pi/Desktop/snmp.config","r+") as fd:
        ip = fd.readline()
    ipAddress = ip.split('\n')[0]
    return ipAddress

HOST_IP = getIpAddress()

def systemcon():
    st = 0
    try:
        print("try exception")
        st = client.connect(broker, port, keepalive=60)  # establishing connection

    except:
        print("exception")
        st = 1;

    finally:
        print("finalyy exception")
        if (st != 0):
            time.sleep(5)
            systemcon();


def serial_config():
    """
    function to configure the pi or computer
    receive da  ta and returns the serial port
    """
    # Open the serial ports for the configuration and the data ports

    # Raspberry pi
    # data_port = serial.Serial('/dev/ttyS0', 9600)
    data_port = serial.Serial('/dev/ttyUSB0', 9600)

    # Windows
    #data_port = serial.Serial('COM3', 9600)

    if data_port.isOpen():
        try:
            # throwing all the data stored at port coming from sensor
            data_port.flushInput()
        # if error is been thrown print it
        except Exception as err:
            print("Error " + str(err))
            data_port.close()
            exit()

    else:
        try:
            data_port.open()
        except Exception as err:
            print("Error " + str(err))
            data_port.close()
            exit()

    return data_port


def processData(data_port):
    '''
    processes the serial data
    :return: none
    '''
    data = 0
    global byteBuffer, byteBufferLength
    max_buffer_size = 2048
    frame_size = 150
    last_byte = 127
    # if data available in serial port
    if data_port.in_waiting:
        read_buffer = data_port.read(data_port.in_waiting)
        # print(read_buffer)
        byte_vec = np.frombuffer(read_buffer, dtype='uint8')
        byte_count = len(byte_vec)

        # Check that the buffer is not full, and then add the data to the buffer
        if (byteBufferLength + byte_count) < max_buffer_size:
            byteBuffer[byteBufferLength:byteBufferLength + byte_count] = byte_vec[:byte_count]
            byteBufferLength = byteBufferLength + byte_count

            # Check that the buffer has some data
            if byteBufferLength > frame_size:
                # check for all possible locations for 127
                possible_locs = np.where(byteBuffer == last_byte)[0]
                # print("possible_locs", possible_locs)
                # print("byteBufferLength", byteBufferLength)

                for loc in possible_locs:
                    if loc > (frame_size - 1):
                        data_frame = byteBuffer[(loc - frame_size):loc]
                        # print("data_frame", data_frame)
                        # print("data_frame length", len(data_frame))
                        processDataFrame(data_frame)
                        # print("byteBuffer", byteBuffer[:loc+1])
                        # Remove the data from buffer
                        byteBuffer[:byteBufferLength-loc] = byteBuffer[loc:byteBufferLength]
                        byteBuffer[byteBufferLength - loc:] = np.zeros(
                            len(byteBuffer[byteBufferLength - loc:]),
                            dtype='uint8')
                        byteBufferLength = byteBufferLength - loc
                        break


def processDataFrame(data_array):
    '''slee
    function to process data array
    :param data_array:
    :return: none
    '''
    global client, gatewayMac
    payload = []
    split_data_array = np.split(data_array, 10)
    for pair in split_data_array:
        if pair[1]:
            payload.append({
                "tagId": "{0:0{1}x}".format(pair[0], 2) + "-" + "{0:0{1}x}".format(pair[1], 2) + "-"
                         + "{0:0{1}x}".format(pair[2], 2) + "-" + "{0:0{1}x}".format(pair[3], 2) + "-"
                         + "{0:0{1}x}".format(pair[4], 2) + "-" + "{0:0{1}x}".format(pair[5], 2),
                "instrId": int(pair[6]),
                "Battery": int(pair[7]),
                "temp": int(pair[8]),
                "hum": int(pair[9]),
                "airFlow": int(pair[10]),
                "RSSI": int(pair[14]),
                "Gateway": gatewayMac,
                "TimeStamp": int(round(time.time() * 1000))
            })
    # print("split_data_array", split_data_array)
    # print("split_data_array length", len(split_data_array))
    if len(payload):
        # print(payload)
        # json_payload = json.dumps(payload)
        # ret = client.publish(topic, payload=json_payload, qos=0)
        # if (ret[0] != 0):
        #     systemcon()
        json_payload = json.dumps(payload)
        print(json_payload)

        try:
            #ret = requests.post(SERVER_DNS,json=json_payload)
            ret = requests.post(DATA_ENDP,json=json_payload)
        except Exception as err:
            print(err)
            print("Failed to post the Data")
        else:
            if(ret.status_code==200):
                print("Data posted successfully")
            else:
                print("Failed to post the data")

        try:
            changeSnmpAttr(payload)
        except Exception as err:
            print(err)
            print("Failed to change the SNMP attributes")
        else:
            print("Changed SNMP Attributes")



#This function changes the SNMP attributes according to the live data
def changeSnmpAttr(payload):
    dictLen = len(payload)

    for var in payload:
        macAddr = var["tagId"]
        oidList = oid[macAddr]
        
        if (var["airFlow"]>127):
            var["airFlow"] = 254-var["airFlow"]    

        args = [ "/usr/bin/snmpset","-v","2c","-c","public",HOST_IP,oidList[0],"i",str(var["temp"]) , oidList[1],"i",str(var["hum"]) , oidList[2],"i",str(var["airFlow"]) , oidList[3],"i",str(var["Battery"])  ]
        p = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        outs,errs = p.communicate()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, user_data, flags, rc):
    print("Connected with result code " + str(rc))

Data_port = serial_config()
# client = mqtt.Client()
# client.on_connect = on_connect
# systemcon()
# client.loop_start()

while True:
    try:
        # process serial data
        processData(Data_port)
    except KeyboardInterrupt:
        Data_port.close()
        # client.loop_stop()
        break
