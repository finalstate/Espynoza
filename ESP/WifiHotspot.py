import network
import time

import Config

####################################################################################################

class Wifi:
    def __init__(self, p_Log, p_Blinker):        
        if network.WLAN(network.AP_IF).active():
            network.WLAN(network.AP_IF).active(False) # make sure it does not interfere

        l_Wifi = network.WLAN(network.STA_IF)
        if l_Wifi.active():
            l_Wifi.disconnect()  
            l_Wifi.active    (False)  
            
        self.f_Wifi = network.WLAN(network.STA_IF)
        self.f_Wifi.active(True )
        self.f_Wifi.ifconfig((Config.C_IP, Config.C_Netmask, Config.C_Gateway, Config.C_DNS))
        
        if not self.f_Wifi.isconnected():            
            while True:        
                self.f_Wifi.connect(Config.C_Hotspot.encode(), Config.C_Password)
                l_Count = Config.C_ConnectTO * 100
                while not self.f_Wifi.isconnected():
                    time.sleep(0.01)
                    l_Count -= 1
                    if l_Count == 0:
                        break
                    
                if self.f_Wifi.isconnected():
                    break
                else:
                    p_Log.add('Retry...')
                    p_Blinker.blink(10)
                    
        p_Blinker.setLed(True)

#########################
        
    @property
    def f_AP(self):
        return Config.C_Hotspot
