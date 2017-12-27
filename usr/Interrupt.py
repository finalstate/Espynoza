import machine

import BaseHandler

####################################################################################################

class Handler (BaseHandler.Handler):
    
    '''
        Target      : ESP8266,
        Description : Read digital input vlues after an interrupt
        Parameters  : Period: The read frequency, in milliseconds. If changes occur at a higer frequency, the pulses will be ignored.
                      Params:
                        - The Tag to use in MQTT topic
        Returns     : The state of the interrupt pin, On or Off   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)

        self.f_States    = {}
        self.f_OldStates = {}
                
        for l_PinName in self.f_Params:
            l_Pin = self.f_Pins[l_PinName[0]]
            
            l_Pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.IRQ)
            
            self.f_States   [str(l_Pin)] = None
            self.f_OldStates[str(l_Pin)] = l_Pin.value()

#########################
 
    def periodic(self, p_Now):        
        for l_PinName in self.f_Params:
            l_PinString = str(self.f_Pins[l_PinName[0]])
            
            if  (   (self.f_States[l_PinString] is not None)
                and (self.f_States[l_PinString] != self.f_OldStates[l_PinString])
                ):
                self.f_MQTT.publish(l_PinName[0] + '/Interrupt', ('On' if self.f_States[l_PinString] else 'Off'))

                self.f_OldStates[l_PinString] = self.f_States[l_PinString]            
                self.f_States   [l_PinString] = None

#########################

    def IRQ(self, p_Pin):
        self.f_States[str(p_Pin)] = p_Pin.value()

