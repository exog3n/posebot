# # from network import WLAN
# # wlan = WLAN(mode=WLAN.STA)
# #
# # nets = wlan.scan()
# # for net in nets:
# #     print(net.ssid)
# #     if net.ssid == 'posenet':
# #         print('Network found!')
# #         wlan.connect(net.ssid, auth=(net.sec, 'posenetS'), timeout=5000)
# #         while not wlan.isconnected():
# #             machine.idle() # save power while waiting
# #         print('WLAN connection succeeded!')
# #         break
#
# import pycom
# import network
# import time
# # import mqtt
# from mqtt import MQTTClient
# import machine
# import _thread
#
# from machine import Pin
#
# # initialize `P9` in gpio mode and make it an output
# relay = Pin('P9', mode=Pin.OUT)
#
# pycom.heartbeat(False)
#
# # user definitions
# systemInterval = 0.01
# inRoomSize = 600
# # left node
# clientName = "sideleft"
# nodeId = 'l'
# idNo = 0
# nodeTwin = 'r'
# # right node
# # clientName = "sideright"
# # nodeId = 'r'
# # idNo = 1
# # nodeTwin = 'l'
#
# # system definitions
# # curMsg = 'l0|r0'
# curMsg = '0'
# msgSeparator = '|'
# sideLRangeMax = 500 / 2
# sideLRangeMin = sideLRangeMax * (-1)
# ledRangeMin = 0
# ledRangeMax = 255
#
# topic="/pose/"+nodeId+"/sidelights"
# # topic="/pose/"+nodeId+"/handlights"
#
# ####################################################
# # setup as a wifi station
# wlan = network.WLAN(mode=network.WLAN.STA)
#
# # config static ip per node and also an id
# # wlan.ifconfig(config=('10.42.0.100', '255.255.255.0', '10.42.0.1', '10.42.0.1'))
# # wlan.ifconfig(config=('10.42.0.101', '255.255.255.0', '10.42.0.1', '10.42.0.1'))
#
# wlan.connect('posenet', auth=(network.WLAN.WPA2, 'posenetS'))
# while not wlan.isconnected():
#     time.sleep_ms(50)
# print('connected to rpi over wifi')
# print(wlan.ifconfig())
# ##################################################
#
#
# def msgListen(delay, id):
#     while True:
#         # print("Sending ON")
#         # client.publish(topic="/gps", msg="ON")
#         # time.sleep(1)
#         # print("Sending OFF")
#         # client.publish(topic="/gps", msg="OFF")
#         client.check_msg()
#         time.sleep(delay)
#
#
# def msgSuccess(topic, msg):
#     global curMsg
#     curMsg = str(msg, 'utf-8', 'ignore')
#
# # control the led based on nodeId and command
#
#
# def ledCtrl(delay, id):
#     while True:
#         global curMsg
#         cmd = deserializePose(curMsg)
#         # if(topic == "/pose/"+nodeId+"/sidelights"):
#         color = mapPose2Led(cmd, sideLRangeMin,sideLRangeMax, ledRangeMin, ledRangeMax)
#         if(color < 256 and color > 0):
#             # left node
#             colorValue = rgb_to_hex(color,0, 0)
#             # right node
#             # colorValue = rgb_to_hex(0, 0, color)
#             pycom.rgbled(int(colorValue, 16))
#         # if(topic == "/pose/"+nodeId+"/handlights"):
#         # relay.value(cmd)
#         # print(cmd)
#         time.sleep(delay)
#
# def rgb_to_hex(red, green, blue):
#     return '%02x%02x%02x' % (red, green, blue)
#
#
# # parse number from message (string to command)
#
# def deserializePose(msg):
#     # print(msg)
#     # return int(str(msg).split(msgSeparator)[idNo].replace(nodeId, '').replace('"', ''))
#     return int(str(msg))
#     # return msg
#
# # x:input value
# # a,b:input range
# # c,d:output range
# # y:return value
#
# def mapPose2Led(x, a, b, c, d):
#     if isinstance(x, int):
#         y = round((x - a) / (b - a) * (d - c) + c)
#     else:
#         y = 0
#     return y
#
#
# client = MQTTClient(clientName, "10.42.0.1", port=1883)
# client.settimeout = systemInterval
# client.set_callback(msgSuccess)
# client.connect()
# client.subscribe(topic)
# _thread.start_new_thread(msgListen, (systemInterval, (1, 0)))
# _thread.start_new_thread(ledCtrl, (systemInterval, (2, 1)))




from network import LoRa


import pycom
import time
import socket
import ubinascii
import struct

pycom.heartbeat(False)


# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an ABP authentication params
# dev_addr = struct.unpack(">l", ubinascii.unhexlify('260114D0'))[0]
dev_addr = struct.unpack(">l", ubinascii.unhexlify('26011BD9'))[0]
nwk_swkey = ubinascii.unhexlify('729A3E645F150E0440AD5B80523202CE')
app_swkey = ubinascii.unhexlify('A0C2283E89E1C0F9851AE9553F54AC57')

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)


# loop for sending data to gateway continuously
while True:
    # send some data
    s.send(bytes([0x01, 0x02, 0x03]))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print(data)

    pycom.rgbled(0xFF0000)  # Red led
    time.sleep(2)
    pycom.rgbled(0x0000FF)  # Blue

    time.sleep(240)
