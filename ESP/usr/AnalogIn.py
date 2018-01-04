import machine

import BaseHandler

####################################################################################################

class Handler (BaseHandler.Handler):
    
    '''
        Target      : ESP8266,
        Description : Read analog input
        Parameters  : Period: The read frequency, in milliseconds 
                      Params:
                        - The Tag to use in MQTT topic
                        - Anti-jitter: do not send value if it did not change by more than this value (relative to the last send value)
        Returns     : Value between 0 and 1023   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)

        self.f_ADC      = machine.ADC(0)
       
        self.f_OldValue = -self.f_Params[0][1]
        
#########################
 
    def periodic(self, p_Now):
        l_NewValue = self.f_ADC.read()
        
        if abs(l_NewValue - self.f_OldValue) > self.f_Params[0][1]: 
            self.f_OldValue = l_NewValue
            self.f_MQTT.publish(self.f_Params[0][0] + '/Analog', l_NewValue)
