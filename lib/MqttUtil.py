#! /usr/bin/python3
# -*- coding: utf-8 -*-
####################################################################################################

import json
import time

import paho.mqtt.client as mqtt

####################################################################################################

class MQTT:
    C_TimeStampLength = 4
    
    ''' *All* payload data is in bytes.
        Return value from target is prefixed with a timestamp (microseconds since device startup). 
        The timestamp has a 0 value upon error.
    '''
    def __init__(self, p_TargetName, p_Broker, p_UserName=None, p_Password=None):
        self.resetState()
        self.f_TargetName = p_TargetName
        
        self.f_Client     = mqtt.Client()
        
        if p_UserName is not None:
            self.f_Client.username_pw_set(p_UserName, p_Password)
        
        self.f_Client.connect(p_Broker, 1883,60) #
        
        self.f_Client.on_message = self.getResponse
        l_Result = self.f_Client.subscribe(f'sensors/esp/{self.f_TargetName}/Hello', qos=0)  # Message: AccessPoint (FSSI)
        l_Result = self.f_Client.subscribe(f'sensors/esp/{self.f_TargetName}/Bye',   qos=0)  # Message: either Crash (the will), or regular (remote reset by software) 
        
        l_Result = self.f_Client.subscribe(f'sensors/esp/{self.f_TargetName}/res',   qos=0)
        l_Result = self.f_Client.subscribe(f'sensors/esp/{self.f_TargetName}/print', qos=0)
        l_Result = self.f_Client.subscribe(f'sensors/esp/{self.f_TargetName}/data',  qos=0)
#        print('Subscribe result: ', l_Result)
        self.f_Client.loop_start()
        
    def resetState(self):
        self.f_Hello     = False
        self.f_Bye       = False
        self.f_Done      = False
        self.f_Payload   = None
        self.f_Data      = bytearray()
        self.f_Timestamp = True
    
    def __str__(self):
        return  f'''
                     {self.f_Done}     
                     {self.f_Payload}
                     {self.f_Data}     
                     {self.f_Timestamp}       
                 '''
                 
    def getData(self):
        return self.f_Data
    
    def getResponse(self, p_Client, p_UserData, p_Message):
        '''
            MQTT subscribe callback.
            Sets the global state:
                f_Data      : add the data returned by the target to a bytearray
                f_Payload   : the payload of this message
                f_Timestamp : a timestamp in microseconds giving the time since startup of the target. Is 0 in case of error.
               
            
            The global state should not be read by external functions, the return value of sendCommand should be used instead.
            Cumulated data during file rerievel is accessible through getData().
            Text printed on remote host is printed to console, and is not part of either data or payload.
        '''
        
#        print(f'''\nResponse: {p_Message.topic} -> {p_Message.payload} ''')
        
        try:
            self.f_Timestamp, self.f_Payload = p_Message.payload.split(b':',1)
            self.f_Timestamp = int(self.f_Timestamp)
            
        except ValueError:
            self.f_Timestamp  = int.from_bytes(p_Message.payload[0:MQTT.C_TimeStampLength], 'big')
            self.f_Payload = p_Message.payload[MQTT.C_TimeStampLength:]

        if   p_Message.topic.endswith('print'):
            print(self.f_Payload.decode(), end='', flush=True)
                
        elif p_Message.topic.endswith('data'):
            if self.f_Payload != b'':
                self.f_Data += self.f_Payload
                print('.', end='', flush=True)
            else:
                print ('', flush=True)
                
        elif p_Message.topic.endswith('Hello'):
            self.f_Hello = True
            
        elif p_Message.topic.endswith('Bye'):
            self.f_Bye   = True
            
        elif p_Message.topic.endswith('res'):
            self.f_Done  = True
        else:
            print (f'Unknown topic: {p_Message.topic}')
            
    def sendCommand(self, p_Command, p_Timeout=15):
        '''
            p_Command : convert to bytes
            p_Timeout : timeout, not waiting for response if 0
        ''' 
        l_Command = p_Command
        if isinstance(l_Command, str):
            l_Command = l_Command.encode()
        
        self.resetState()
        self.f_Client.publish(f'esp/{self.f_TargetName}/cmd', l_Command, qos=0)
        
#        print ('Timeout', p_Timeout)
        
        if p_Timeout <= 0:
            return (True, '')
        
        while (not self.f_Done):
            time.sleep(0.1)
            p_Timeout -= 0.1
            if p_Timeout <= 0:
                return (False, b'Timeout')
            
#        print ('Payload', self.f_Payload)
        return (self.f_Timestamp, self.f_Payload)
    
    def waitHello(self, p_Timeout=15):
        while (not self.f_Hello):
            time.sleep(0.1)
            p_Timeout -= 0.1
            if p_Timeout <= 0:
                return (False, b'Hello timeout')
        return (self.f_Timestamp, self.f_Payload)
    
    def waitBye(self, p_Timeout=15):
        while (not self.f_Bye):
            time.sleep(0.1)
            p_Timeout -= 0.1
            if p_Timeout <= 0:
                return (False, b'Bye timeout')
        return (self.f_Timestamp, self.f_Payload)
        
    def close(self):
        self.f_Client.disconnect()
        
####################################################################################################
  