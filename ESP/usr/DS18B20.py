import time

import ds18x20
import onewire
import ubinascii

import BaseHandler

####################################################################################################

class Handler(BaseHandler.Handler):
    '''
        Target      : ESP8266,
        Description : Read temperature from a ds18B20 sensor
        Parameters  : Period: period at which temperatures are measured, in milliseconds. Minimal period is 750ms, as per chip limitation.
                      Params:
                        - The name used as Tag. The channel is taken from the id of the chip.
                        - Anti-jitter: do not send value if it did not change by more than this value (relative to the last send value)
        Returns     : The temperature, between -55°C and +125°C
    '''

    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)
        
        try:
            self.f_DS18B20       = ds18x20.DS18X20(onewire.OneWire(self.f_Pins['OneWire']))
            self.f_Thermometers  = self.f_DS18B20.scan()
            self.f_Temperatures  = [0 for l_i in self.f_Thermometers]
            
            self.f_StartTime     = time.ticks_ms()
            self.f_DS18B20.convert_temp()
            
        except Exception as l_Exception:
            self.f_Thermometers  = []

#########################

    def periodic(self, p_Now):
        if  (   (len(self.f_Thermometers) == 0)
            or  ((750 - time.ticks_diff(p_Now, self.f_StartTime)) > 0)
            ):
            return None
        
        l_Temperatures = []
        for l_i, l_Thermometer in enumerate(self.f_Thermometers):
            l_Id          = ubinascii.hexlify(l_Thermometer).decode('ascii')
            l_Temperature = self.f_DS18B20.read_temp(l_Thermometer)
            
            if  (   (-55 <= l_Temperature <= 125)
                and (  abs(l_Temperature - self.f_Temperatures[l_i]) > self.f_Params[0][1])
                ):
                self.f_Temperatures[l_i] = l_Temperature
                self.f_MQTT.publish(l_Id + '/' + self.f_Params[0][0], l_Temperature)

        self.f_StartTime = p_Now
        self.f_DS18B20.convert_temp()
