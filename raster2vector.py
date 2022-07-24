import os
import base64
import struct
import imghdr
 
def get_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0)
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                fhandle.seek(1, 1)
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception:
                return
        else:
            return
        return width, height

def svg():
    
    start_svg_tag = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
    """
    end_svg_tag = """</svg>"""
    
    for image in os.listdir(os.getcwd()+ "/"): # Image must be in the folder with the program
        if image.endswith(".jpg") or image.endswith(".png") or image.endswith(".gif"):
            width, height = get_image_size(image)
            img_file = open(image, 'rb')
            base64data = base64.b64encode(img_file.read())
            base64String = f'<image xlink:href="data:image/png;base64,{base64data.decode("utf-8")}" width="{width}" height="{height}" x="0" y="0" />'
            svg_size = f'width="{width}px" height="{height}px" viewBox="0 0 {width} {height}">'
            
            if os.path.exists('result') == False: os.mkdir('result') # create a folder "result"
            
            svg = open("result/"+os.path.splitext(image)[0]+".svg",'w') # write the result to a folder
            svg.write( start_svg_tag + svg_size + base64String + end_svg_tag)
            print ('Converted '+ image + ' to ' + os.path.splitext(image)[0]+".svg")


if __name__== '__main__':
    svg()
