from bluetooth import *
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
padding = 2

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()
disp.clear()
disp.display()


width = disp.width
height = disp.height
image = Image.new('1',(width,height))
draw = ImageDraw.Draw(image)
top = padding
bottom = height - padding
x = padding
font = ImageFont.load_default()



server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805f9b34fb"

advertise_service( server_sock, "SampleServer",service_id = uuid,
        service_classes = [ uuid, SERIAL_PORT_CLASS ],
        profiles = [ SERIAL_PORT_PROFILE ]#,protocols=[OBEX_UUID]
        )
        
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print "received [%s]" % data
        disp.clear()
        disp.display()
        #image = Image.new('1',(width,height))
        #draw = ImageDraw.Draw(image)
        if(len(data)>15):
            draw.text((x, top)," "+ data[0:18], font= font, fill = 255)
            #top=top+10
            draw.text((x, top+10)," "+ data[19:len(data)], font= font, fill = 255)
            #top=top+10
        else:
            draw.text((x, top)," "+ data, font = font, fill = 255)
        top=top+20
        if(top>62):
            disp.clear()
            image = Image.new('1',(width,height))
            draw = ImageDraw.Draw(image)
            top = padding
            draw.text((x,top)," "+ data, font= font, fill = 255)
            top = top+20
        disp.image(image)
        disp.display()

except IOError:
    pass

print("disconnected")
disp.clear()
disp.display()
client_sock.close()
server_sock.close()
print("all done")
