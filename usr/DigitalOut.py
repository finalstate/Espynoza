import BaseHandler

####################################################################################################

class Handler (BaseHandler.Handler):
    '''
        Target      : ESP8266,
        Description : Set Digital output
        Parameters  : Period: the period if blinking is true, in milliseconds
                      Params:
                        - The pin used for output
                        - Boolean, if True, blink output
        Returns     : N/A   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)

        self.f_States = { l_Color : False for l_Color, l_Blink in self.f_Params}

#########################
        
    def periodic(self, p_Now):
        for l_Color, l_Blink in self.f_Params:
            if l_Blink:
                self.toggle(l_Color)

#########################

    def set(self, p_Color, p_State):
        self.f_States[p_Color] = int(p_State)
        self.f_Pins  [p_Color].value(int(p_State))
        
#########################

    def toggle(self, p_Color):
        self.f_States[p_Color] = not self.f_States[p_Color]
        self.f_Pins  [p_Color].value(self.f_States[p_Color])
        
