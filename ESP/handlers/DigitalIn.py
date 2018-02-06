import BaseHandler

####################################################################################################

class Handler (BaseHandler.Handler):
    
    '''
        Target      : ESP8266,
        Description : Read digital input
        Parameters  : Period: The read frequency, in milliseconds 
                      Params:
                        - Name of the pin to read. Is also used as Tag in MQTT topic
                        - Delay. Do not send state changes occuring more often than this.
        Returns     : State of the Pin.   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)

        # init to opposite of current state, and start time minus the delay. This will provoke the sending of the first value read
        self.f_States = { l_PinName : (not self.f_Pins[l_PinName].value(), -l_Delay) for l_PinName, l_Delay in self.f_Params}
        
#########################
 
    def periodic(self, p_Now):
        for l_PinName, l_Delay in self.f_Params:
            
            l_NewState = self.f_Pins[l_PinName].value()
            if l_NewState != self.f_States[l_PinName][0]:
                if (p_Now -self.f_States[l_PinName][1]) > l_Delay:
                    self.f_MQTT.publish('1/' + l_PinName, ('On' if l_NewState else 'Off'))
                    
                    self.f_States[l_PinName] = (l_NewState, p_Now)
        
