# import package serial
import random

import serial

import time
# import package numpy
import numpy as np
# import paho.mqtt.client
import paho.mqtt.client as mqtt
# import json package
import json

time.sleep(10)

broker = "dhl.vacustech.in"
port = 1883
topic = "dhltracking"
gatewayMac = "5a-c2-15-d1-00-01"


byteBuffer = np.zeros(2 ** 11, dtype='uint8')
byteBufferLength = 0


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
    receive data and returns the serial port
    """
    # Open the serial ports for the configuration and the data ports

    # Raspberry pi
    # data_port = serial.Serial('/dev/ttyS0', 9600)
    data_port = serial.Serial('/dev/ttyUSB0', 9600)

    # Windows
    # data_port = serial.Serial('COM3', 9600)

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
    frame_size = 600
    last_byte = 127
    # if data available in serial port
    if data_port.in_waiting:
        read_buffer = data_port.read(data_port.in_waiting)
        # print(read_buffer)
        byte_vec = np.frombuffer(read_buffer, dtype='uint8')
        byte_count = len(byte_vec)

        # Check that the buffer is not full, and then add the data to the buffer
        if (byteBufferLength + byte_count) < max_buffer_size:
            # byteBuffer[byteBufferLength:byteBufferLength + byte_count] = byte_vec
            byteBuffer = np.insert(byteBuffer, byteBufferLength + 1, byte_vec)
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
                        print("byteBuffer", byteBuffer[:loc])
                        # Remove the data from buffer
                        # byteBuffer[:loc] = byteBuffer[loc:byteBufferLength]
                        # byteBuffer[byteBufferLength - loc:] = np.zeros(
                        #    len(byteBuffer[byteBufferLength - loc:]),
                        #    dtype='uint8')
                        np.pad(byteBuffer, (1, 0), mode='constant')[loc + 2:]
                        byteBufferLength = byteBufferLength - loc
                        break


def processDataFrame(data_array):
    '''
    function to process data array
    :param data_array:
    :return: none
    '''
    global client, gatewayMac, dbClient
    payload = []
    db_payload = []
    split_data_array = np.split(data_array, 100)
    for pair in split_data_array:
        if pair[1]:
            # "Tag1": "{0:0{1}x}".format(pair[0], 2) + "-" + "{0:0{1}x}".format(pair[1], 2),
            # "Tag2": "{0:0{1}x}".format(pair[2], 2) + "-" + "{0:0{1}x}".format(pair[3], 2),
            payload.append({
                "Tag1": "{0:0{1}d}".format(pair[0], 2) + "-" + "{0:0{1}d}".format(pair[1], 2),
                "Tag2": "{0:0{1}d}".format(pair[2], 2) + "-" + "{0:0{1}d}".format(pair[3], 2),
                "Battery": int(pair[4]),
                "RSSI": int(pair[5]),
                "Gateway": gatewayMac,
                "TimeStamp": int(round(time.time() * 1000))
            })
            
    # print("split_data_array", split_data_array)
    # print("split_data_array length", len(split_data_array))
    if len(payload):
        # print(payload)
        json_payload = json.dumps(payload)
        #json_db_payload = json.dumps(db_payload)
        ret = client.publish(topic, payload=json_payload, qos=0)
        #ret = dbClient.publish(db_topic, payload=json_db_payload, qos=0)
        if ret[0] != 0:
            systemcon()

        print(json_payload)
        #print(json_db_payload)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, user_data, flags, rc):
    print("Connected with result code " + str(rc))


Data_port = serial_config()
client = mqtt.Client()
client.on_connect = on_connect
systemcon()
client.loop_start()


while True:
    try:
        # process serial data
        processData(Data_port)
    except KeyboardInterrupt:
        Data_port.close()
        client.loop_stop()
        break
