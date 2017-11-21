#RGB888 -> RGBA5551 converter for Mario Party, by Celery

import sys

ALPHAMODE_UNKNOWN    = 1
ALPHAMODE_OFF        = 2
ALPHAMODE_ON         = 3
DEFAULT_FILENAME_IN  = "input.bmp"
DEFAULT_FILENAME_OUT = "output.bin"
INVISIBLE_COLOR      = b'\xf8' + b'\x78' + b'\xf8' #modify this to change invis color
MAX_5_BIT            = 32
MAX_8_BIT            = 256
VERBOSE              = False

AlphaState = ALPHAMODE_UNKNOWN
PixelsRgb888 = []

def checkAlphaState():
    global AlphaState
    if(AlphaState == ALPHAMODE_UNKNOWN):
        ActivateAlpha = input("Pixel #" + str(Index) + " matches invisible color. Enable transparency for this session? ")
        if('y' in ActivateAlpha):
            AlphaState = ALPHAMODE_ON
        else:
            AlphaState = ALPHAMODE_OFF

#Multiply using ratios of an 8bit component to find a 5bit component
def eightToFive(Color):
    for Component in Color:
        Ratio = Component/MAX_8_BIT
        NewColor = Ratio*MAX_5_BIT
        if(VERBOSE):
            print(str(NewColor) + '\n')
        return int(NewColor)
        
#Sorting method of pixels for final image
def getIndex(Pixel):
    return Pixel.Index
    
#Shift component values to the left to make room for other colors, return 16bit RGBA5551 pixel
def makePixel(Red, Green, Blue, Alpha):
    NewRed = eightToFive(Red) << 11
    NewGreen = eightToFive(Green) << 6
    NewBlue = eightToFive(Blue) << 1
    NewColor = NewRed + NewGreen + NewBlue + Alpha
        
    return NewColor.to_bytes(2, byteorder='big')

class Rgb888:
    def __init__(self, Red, Green, Blue, Index):
        self.Red   = Red
        self.Green = Green
        self.Blue  = Blue
        self.Index = Index
        
    def writeRgba5551(self, Output):
        Alpha = 1
        global AlphaState
        
        #Turn visibility off if color matches invis
        if((self.Red + self.Green + self.Blue) == INVISIBLE_COLOR):
            checkAlphaState()
            if(AlphaState == ALPHAMODE_ON):
                Alpha = 0
                
        Output.write(makePixel(self.Red, self.Green, self.Blue, Alpha))

print("Starting...")

if(len(sys.argv) > 1):
    InputFilename = sys.argv[1]
else:
    InputFilename = DEFAULT_FILENAME_IN
    
print("Opening \"" + InputFilename + "\" as RGB888 bitmap...")
InputFile = open(InputFilename, "rb")
try:
    HeaderField = InputFile.read(2)
    
    #Verify 'BM' is in start of header
    if("BM" in str(HeaderField)):
        print("Header is OK.")
    else:
        print("Header is BAD. Is this a bitmap?")
    
    Width = input("Horizontal pixel count of image: ")
    
    print("Discarding header...")
    header = InputFile.read(52)
    
    print("Opening input file...")
    byte = InputFile.read(1)
    CurPixels = 0
    ReadPixels = 0
    ReadRows = 0
    while byte:
        if(VERBOSE):
            print(str(ReadPixels))
            
        blue = byte
        byte = InputFile.read(1)
        green = byte
        byte = InputFile.read(1)
        red = byte
        byte = InputFile.read(1)
        Index = (int(Width)-CurPixels) + (int(Width)*ReadRows)
        
        if(VERBOSE):
            print("index: " + str(Index))
            
        NewPixel = Rgb888(red, green, blue, Index)
        PixelsRgb888.append(NewPixel)
        ReadPixels += 1
        CurPixels += 1
        
        #Index on next row when one row is read in
        if(CurPixels == int(Width)):
            ReadRows += 1
            CurPixels = 0
            
    print("Read " + str(ReadPixels) + " pixels. " + str(Width) + "x" + str(ReadRows))
    
    print("Sorting pixels into MP format...")
    PixelsRgb888 = sorted(PixelsRgb888, reverse=True, key=getIndex)
    
    print("Opening output file...")
    Output = open(InputFilename + ".bin", "wb")
    
    ReadPixels = 0
    for Pixel in PixelsRgb888:
        if(VERBOSE):
            print(str(ReadPixels))
        ReadPixels += 1
        Pixel.writeRgba5551(Output)
    print("Wrote " + str(ReadPixels) + " pixels to " + InputFilename + ".bin. Done!")
    Output.close()
    
finally:
    InputFile.close()
