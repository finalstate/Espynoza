import machine

import BaseHandler

####################################################################################################

class Handler (BaseHandler.Handler):
    '''
        Target      : ESP8266,
        Description : Set PWM output
        Parameters  : Period: N/A 
                      Params:
                        - The pin used for PWM output
        Returns     : N/A   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)

        self.f_PWMs = {l_PwmPin[0]: machine.PWM(self.f_Pins[l_PwmPin[0]], freq=1000) for l_PwmPin in self.f_Params}

#########################
        
    def setDimmer(self, p_Name, p_Percent):
        self.f_PWMs[p_Name].duty(int(p_Percent*1023/100))
        
