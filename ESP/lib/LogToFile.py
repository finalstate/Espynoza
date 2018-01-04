import time
import machine

import Config

####################################################################################################

class Log:
    def __init__(self):
        self.f_LogFile = open(Config.C_LogFile, 'a')
        
        machine.RTC().datetime((2010, 1,1,5,0,0,0,0))
            
#########################
        
    def add(self, * p_Args):
        l_Now = time.localtime(time.time()+2*60*60)
        self.f_LogFile.write('{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} - '.format(l_Now[0],l_Now[1],l_Now[2],l_Now[3],l_Now[4],l_Now[5]))
        self.f_LogFile.write(' '.join(map(str,p_Args)))
        self.f_LogFile.write('\n')
        
        self.f_LogFile.flush()
    
#########################

    def clear(self):        
        self.f_LogFile.close()
        self.f_LogFile = open(Config.C_LogFile, 'w')

#########################

    def close(self):        
        self.f_LogFile.close()

#########################
