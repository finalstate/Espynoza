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
            l_APs  = []
            l_RSSI = 0
            
            while True:        
                if len(l_APs) == 0:
                    l_APs = self.f_Wifi.scan()
                    p_Blinker.blink(1)
                    l_APs.sort(key=lambda x: x[3]) # sort by RSSI
            
                l_AP     = l_APs.pop()
                l_Choice = l_AP[0]
                l_RSSI   = l_AP[3]
                
                self.f_Wifi.connect(l_Choice, Config.C_Password)
                l_Count = Config.C_ConnectTO * 100
                while not self.f_Wifi.isconnected():
                    time.sleep(0.01)
                    l_Count -= 1
                    if l_Count == 0:
                        break
                    
                if self.f_Wifi.isconnected():
                    break
                else:
                    p_Log.add('NC {}, RSSI {}'.format(l_Choice, l_RSSI))
                    p_Blinker.blink(10)
                    
            self._AP = '{} ({})'.format(l_Choice.decode('ascii'), l_RSSI)
            
        p_Blinker.setLed(True)

#########################
        
    @property
    def f_AP(self):
        return self._AP
