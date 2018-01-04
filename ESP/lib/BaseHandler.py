class Handler():
    def __init__(self, p_Context):
        self.f_Params, self.f_Pins, self.f_MQTT = p_Context

        self.f_Timer = 0

#########################
        
    def periodic(self, p_Now):
        ...

