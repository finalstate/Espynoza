#! /usr/local/bin/python3.6
# -*- coding: utf-8 -*-
####################################################################################################

import argparse
import os
import sys
import time

##################################################

sys.path.append(os.path.join(sys.path[0], 'etc'))    

import paho.mqtt.client as mqtt

try:
    import DeviceList
except:
    import DemoDeviceList as DeviceList

####################################################################################################

def getResponse(p_Client, p_UserData, p_Message):
    C_TimeStampLength = 4

#    print(f'''\nResponse: {p_Message.topic} -> {p_Message.payload} ''')

    try:
        l_Timestamp, l_Payload = p_Message.payload.split(b':',1)
        l_Timestamp = int(l_Timestamp)
        
    except ValueError:
        l_Timestamp  = int.from_bytes(p_Message.payload[0:C_TimeStampLength], 'big')
        l_Payload    = p_Message.payload[C_TimeStampLength:]
    
    try:
        l_Timestring = str(l_Timestamp)
        l_Timestamp = ''
        while l_Timestring != '':
            l_Timestamp   = l_Timestring[-3:] + ',' + l_Timestamp
            l_Timestring  = l_Timestring[:-3]
        l_Timestamp = l_Timestamp[:-1]
        
        l_Topic = p_Message.topic    
        
        l_TopicParts = l_Topic.split('/')
        
        l_Target = l_TopicParts[2]
        l_Id     = l_TopicParts[3]
        l_Tag    = l_TopicParts[4]
        
        l_Payload = l_Payload.decode()
        
        print(f'''{l_Target:10s} : {l_Timestamp:>12s} {l_Tag:15s}({l_Id:10s}) -> {l_Payload}''')
        
    except Exception as l_Exception:
        print (l_Exception)
        
####################################################################################################
if __name__ == '__main__':
    l_ArgumentParser = argparse.ArgumentParser(description='Communicate with an ESP6288 board via MQTT')
    
    l_ArgumentParser.add_argument('-v', '--verbose',    required=False,  action='store_true',          help='Verbose user info')
    l_ArgumentParser.add_argument('-b', '--broker',     required=True,   action='store',               help='Broker to access ESP.')
    l_ArgumentParser.add_argument('-t', '--target',     required=False,  action='store', default=None, help='Only show these targets')
    
    g_Arguments  = l_ArgumentParser.parse_args()    
        
    l_Broker = g_Arguments.broker
    l_UserName = DeviceList.C_MQTTCredentials[l_Broker][0]
    l_Password = DeviceList.C_MQTTCredentials[l_Broker][1]
    l_Target   = '+' if g_Arguments.target == None else g_Arguments.target
    
    l_Client     = mqtt.Client()
        
    if l_UserName is not None:
        l_Client.username_pw_set(l_UserName, l_Password)
        
    l_Client.connect(l_Broker, 1883,60)
    
    l_Client.on_message = getResponse
    l_Client.subscribe(f'sensors/esp/{l_Target}/#',  qos=0)
    l_Client.loop_start()

    while True:
        time.sleep(0.01)
