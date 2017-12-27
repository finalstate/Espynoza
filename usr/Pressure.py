import machine

import bme280

import BaseHandler

####################################################################################################
    
class Handler(BaseHandler.Handler):
    
    '''
        Target      : ESP8266,
        Description : Read Temperature and Pressure from BME280 (BME180?) module
        Parameters  : Period: The read frequency, in milliseconds 
                      Params:
                        - The Tag to use in MQTT topic
                        - Anti-jitter: do not send value if it did not change by more than this value (relative to the last send value)
        Returns     : The Temperature and the Pressure, with channel set to 1   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)

        self.f_i2c        = machine.I2C(scl=self.f_Pins['SCL'], sda=self.f_Pins['SDA'])
        self.f_BME280     = bme280.BME280(mode=bme280.BME280_OSAMPLE_16, i2c=self.f_i2c)
        self.f_Temp       = 0
        self.f_Pressure   = 0
        
        bme280.BME280.__init__ = None  # no longer needed
    
######################### 

    def periodic(self, p_Now):
        l_Values   = self.getBMEValues()
        l_Temp     = float(l_Values[0][:-1]) # .replace('C',   ''))
        l_Pressure = float(l_Values[1][:-3]) # .replace('hPa', ''))
        
        if abs(self.f_Temp     - l_Temp    ) > self.f_Params[0][1]:
            self.f_MQTT.publish('1/' + self.f_Params[0][0], l_Temp    )
            self.f_Temp     = l_Temp
            
        if abs(self.f_Pressure - l_Pressure) > self.f_Params[1][1]:
            self.f_MQTT.publish('1/' + self.f_Params[1][0], l_Pressure)
            self.f_Pressure = l_Pressure

######################### 

    def getBMEValues(self):
        return self.f_BME280.values
           
