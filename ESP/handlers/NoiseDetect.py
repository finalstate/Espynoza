import machine

import BaseHandler

####################################################################################################

class Handler (BaseHandler.Handler):
    
    '''
        Target      : ESP8266,
        Description : Read input connected to a digital sound input module, detect noise  
        Parameters  : Period: The sample frequency, in milliseconds 
                      Params:
                        - Name of the pin to read. Is also used as Tag in MQTT topic
                        - Threshold: the minimal count of pulses that are considered noise
        Returns     : State of the sound, > 0 if noisy.   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)

        self.f_Count    = {}
        self.f_OldState = {}
                
        for l_PinParams in self.f_Params:
            l_Pin = self.f_Pins[l_PinParams[0]]
            
            l_Pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.IRQ)
            
            self.f_Count   [str(l_Pin)] = 0
            self.f_OldState[str(l_Pin)] = False
        
#########################
 
    def periodic(self, p_Now):
        for l_PinParams, l_Threshold in self.f_Params:
            l_PinString = str(self.f_Pins[l_PinParams])
            
            l_NewState = self.f_Count[l_PinString] > l_Threshold
            if l_NewState:
                self.f_MQTT.publish('1/' + l_PinParams, self.f_Count[l_PinString])
            elif self.f_OldState[l_PinString]:
                self.f_MQTT.publish('1/' + l_PinParams, 0)
                
            self.f_OldState[l_PinString] = l_NewState            

            self.f_Count[l_PinString] = 0

#########################

    def IRQ(self, p_Pin):
        self.f_Count[str(p_Pin)] += 1

