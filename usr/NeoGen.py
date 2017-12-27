import machine
import esp

import BaseHandler

####################################################################################################

class Handler (BaseHandler.Handler):
    
    '''
        Target      : ESP8266,
        Description : Control Neopixel
        Parameters  : Period: The update frequency, in milliseconds 
                      Params:
                        - data pin 
                        - buffer size
                        - name of Python file containing a generator function named 'pixelString'
        Returns     : N/A   
    '''
    
    def __init__(self, p_Context):
        BaseHandler.Handler.__init__(self, p_Context)
        
        self.f_Neo        = self.f_Pins[self.f_Params[0][0]] 
        self.f_BufferSize = self.f_Params[0][1]*3
        l_GeneratorName   = self.f_Params[0][2]

        exec ("""from {} import pixelString""".format(l_GeneratorName), globals())
        
        self.f_Generator  = pixelString(self.f_Params[0][1], * self.f_Params[0][3:])
        
        machine.freq(160000000)
               
#########################
 
    def periodic(self, p_Now):
        esp.neopixel_write(self.f_Neo, next(self.f_Generator), True)

####################################################################################################

    def clear(self):
        esp.neopixel_write(self.f_Neo, bytearray(self.f_BufferSize), True)
        
