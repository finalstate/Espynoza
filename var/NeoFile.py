
def pixelString(p_BufferSize, p_FileName):
    l_Buffer = bytearray(p_BufferSize)
    
    with open(p_FileName, 'rb') as l_File:
        while True:
            l_Size = l_File.readinto(l_Buffer)
            if l_Size < p_BufferSize:
                l_File.seek(0)
                l_Size = l_File.readinto(l_Buffer)
                
            yield l_Buffer
            
