import gc
import os
import sys
import time
import uio

####

import machine
import micropython

import mqtt

####

import Config

if Config.C_LogFile == "":
    import LogNone   as Log
else:
    import LogToFile as Log

if Config.C_Hotspot == "":
    import WifiScan    as Wifi
else:
    import WifiHotspot as Wifi

####################################################################################################
####################################################################################################
    
def trace2string(p_Exception):
    l_Error = uio.StringIO()
    sys.print_exception(p_Exception, l_Error)
    return l_Error.getvalue()

####################################################################################################

def reboot():    
    machine.reset()
    time.sleep(1) # don't know why this is needed, but else reboot loops/hangs/doesn't work

####################################################################################################

def print(* p_Args, sep=" ", end="\n"): # using sep and end (not p_Sep and p_End) to be like 'standard'
    g_MQTT.publish("print", sep.join(map(str, p_Args)) + end)

####################################################################################################

def ping():
    return "pong"
    
####################################################################################################
    
def getFile(p_FileName):
    with open(p_FileName, "rb") as l_File:
        while True:
            l_Buffer = l_File.read(Config.C_ChunkSize)
            g_MQTT.publish("data", l_Buffer)
            if len(l_Buffer) == 0:
                break
                    
    g_MQTT.publish("res", "Sent " + p_FileName)
                
####################################################################################################

def appendFile(p_FileName, p_Data):
    with open(p_FileName, "ab") as l_File:
        l_File.write(p_Data)
        
    return 'OK'

####################################################################################################
####################################################################################################
        
class Watchdog:
    def __init__(self):    
        self.f_WatchdogTouched = True
        self.f_WatchdogTimer   = machine.Timer(-1)
        self.f_WatchdogTimer.init(period=Config.C_WatchdogTO*1000, mode=machine.Timer.PERIODIC, callback=self.check)
    
    def check(self, p_Bizarre):
        if not self.f_WatchdogTouched:
            reboot()
        
        self.f_WatchdogTouched = False
        
    def touch(self):
        self.f_WatchdogTouched = True
                
####################################################################################################
####################################################################################################

class Blinker:
    def __init__(self, p_Led, p_Period):    
        self.f_Led      = machine.Pin (p_Led, machine.Pin.OUT)
        self.f_Period   = p_Period // 2
        self.f_LedState = 0
        self.f_Timer    = machine.Timer(-1)
        
        self.f_Led.on()
        
    def setLed(self, p_Value):
        self.f_Led.value(not p_Value)
        
    def toggleLED(self, p_Bizarre):
        self.f_Led.value(self.f_LedState%2)
        self.f_LedState -= 1
        if self.f_LedState > 0:
            self.f_Timer.init(period=self.f_Period, mode=machine.Timer.ONE_SHOT, callback=self.toggleLED)
 
    def blink(self, p_Count):
        self.f_LedState = p_Count * 2
        self.toggleLED(None)

####################################################################################################
####################################################################################################

class MQTT:
    def __init__(self, p_HelloMessage):
        self.f_Id     = Config.C_ClientId
        self.f_QoS    = Config.C_BrokerQoS
        try:
            l_Broker = Config.C_BrokerIP.split(':')
            self.f_MQTTClient = mqtt.MQTTClient( b"esp_{}".format(self.f_Id), 
                                                 l_Broker[0],                     port     = l_Broker[0] if (len(l_Broker) > 1) else 0,
                                                 user      = Config.C_BrokerUser, password = Config.C_BrokerPassword, 
                                                 keepalive = Config.C_WatchdogTO
                                               )
            self.f_MQTTClient.set_last_will(topic=Config.C_BrokerPubPat.format(ClientId=self.f_Id, Name='Bye'), msg=b"\0\0\0\0Crash", qos=self.f_QoS) 
            self.f_MQTTClient.connect()
            self.f_MQTTClient.set_callback(self.callback, g_Watchdog.touch)
            self.f_MQTTClient.subscribe(Config.C_BrokerSubPat.format(ClientId=self.f_Id), qos=self.f_QoS)
            Config.C_BrokerSubPat   = None
            
            mqtt.MQTTClient.__init__ = None # will not instantiate again
            
            self.publish("Hello", p_HelloMessage)
            
        except OSError:
            reboot()
        
    def callback(self, p_Topic, p_Message):
        g_Blinker.blink(1)
        try:
            _Result_ = eval(p_Message, globals())
            if self.f_Running:
                self.publish("res", _Result_ if _Result_ else "")
            
            gc.collect()
    
        except Exception as l_Exception:
            self.publish("res", trace2string(l_Exception), False)
            
    def loop(self, p_User):
        self.f_Running  = True
        self.f_LastSend = time.time()
        while self.f_Running:            
            if p_User is not None:
                try:
                    p_User.loop()
                except Exception as l_Exception:
                    self.publish("res", trace2string(l_Exception), False)
                    p_User = None # disable loop handlers

            try:
                self.f_MQTTClient.check_msg()
        
                if (time.time() - self.f_LastSend) > (Config.C_WatchdogTO // 2):
                    self.f_MQTTClient.ping()
                    self.f_LastSend = time.time()
                    
            except OSError:
                reboot()
                    
            gc.collect()
            time.sleep(Config.C_LoopDelay)
             
        self.f_MQTTClient.disconnect()
        g_Log.close()
        reboot()
        
    def publish(self, p_SubTopic, p_Data, p_Status=True):
        g_Blinker.blink(1)
        try:
            l_Topic   = Config.C_BrokerPubPat.format(ClientId=self.f_Id, Name=p_SubTopic)
            l_Message = bytearray(b'T' if p_Status else b'F')
            
            if isinstance(p_Data, (bytes, bytearray)):
                l_Message += p_Data
            else:
                l_Message += str(p_Data).encode()
            
            return self.f_MQTTClient.publish(l_Topic, l_Message, qos=self.f_QoS)
        
        except OSError:
            reboot()
        
    def stopESP(self):
        self.publish("Bye", "Regular")
        self.f_Running = False

####################################################################################################
####################################################################################################
    
class User:
    def __init__(self, p_MQTT):
        # Pins
        l_PinList = {}
        for l_Name, l_PinSpec in Config.C_Pins.items():
            if l_PinSpec[1] == 0: # i.e. an input
                l_Pin  = machine.Pin(l_PinSpec[0], l_PinSpec[1], l_PinSpec[2])
            else:
                if l_PinSpec[2] is None:
                    l_Pin  = machine.Pin(l_PinSpec[0], l_PinSpec[1])
                else:
                    l_Pin  = machine.Pin(l_PinSpec[0], l_PinSpec[1], value=l_PinSpec[2])
            l_PinList[l_Name] = l_Pin
            
        del Config.C_Pins
        
        # Handlers
        for l_Handler in Config.C_Handlers.keys():
            l_HandlerClass = __import__(l_Handler).Handler
            Config.C_Handlers[l_Handler]["Handler"] = l_HandlerClass((Config.C_Handlers[l_Handler]["Params"], l_PinList, p_MQTT))
            l_HandlerClass.__init__ = None

            g_Watchdog.touch()
        
        User.Handlers = Config.C_Handlers
        
#########################

    def loop(self):
        l_Now = time.ticks_ms()
        for l_Handler in Config.C_Handlers.values():
            if l_Handler["Period"] != None:
                if l_Handler["Handler"].f_Timer + l_Handler["Period"] < l_Now:
                    l_Handler["Handler"].periodic(l_Now)
                    l_Handler["Handler"].f_Timer += l_Handler["Period"]
                
####################################################################################################      
####################################################################################################

def setup():
    global g_Watchdog
    global g_Blinker
    global g_User
    global g_Log
    global g_MQTT
    
    micropython.alloc_emergency_exception_buf(100)
    
    g_Watchdog = Watchdog()
    Watchdog.__init__ = None
    
    g_Blinker         = Blinker(2, 100)
    Blinker.__init__  = None
    
    g_Log             = Log.Log()
    Log.Log.__init__  = None
    
    l_Wifi            = Wifi.Wifi(g_Log, g_Blinker)
    g_MQTT            = MQTT(l_Wifi.f_AP)
    Wifi.Wifi         = None # init done, no longer needed. Saves almost 1 Kbytes!!!
    MQTT.__init__     = None
            
    try:
        g_User        = User(g_MQTT)
        User.__init__ = None
    except Exception as l_Exception:
        g_User    = None
        l_Message = trace2string(l_Exception)
        g_Log.add("Usr:", l_Message)
        print(l_Message)
    
####################################################################################################

setup()
setup = None

g_MQTT.loop(g_User)
