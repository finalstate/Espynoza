class NeoBuffer:
    def __init__(self, p_Pixels):
        self.f_Pixels = p_Pixels
        self.f_Buffer = bytearray(self.f_Pixels * 3)
        
    def setPixel(self, p_Pixel, p_Green, p_Red, p_Blue):
        l_Offset = (p_Pixel % self.f_Pixels) * 3
        self.f_Buffer[l_Offset+0] = p_Green
        self.f_Buffer[l_Offset+1] = p_Red
        self.f_Buffer[l_Offset+2] = p_Blue
                       
    def clearPixel(self, p_Pixel):
        l_Offset = (p_Pixel % self.f_Pixels) * 3
        self.f_Buffer[l_Offset+0] = 0
        self.f_Buffer[l_Offset+1] = 0
        self.f_Buffer[l_Offset+2] = 0
                       
####################################################################################################

def pixelString(p_PixelCount, p_Steps):    
    l_NeoBuffer = NeoBuffer(p_PixelCount)
    l_Frame = 0
    
    while True:
        l_Red   = (l_Frame * 1      ) % 256
        l_Green = (l_Frame * 4 +  85) % 256
        l_Blue  = (l_Frame * 7 + 170) % 180
            
        for l_Step in range(p_Steps):
            l_NeoBuffer.clearPixel(l_Frame - p_Steps + l_Step)
            l_NeoBuffer.setPixel  (l_Frame           + l_Step, l_Green, l_Red, l_Blue)
        
        l_Frame += p_Steps
            
        yield l_NeoBuffer.f_Buffer   
