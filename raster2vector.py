from os import listdir, getcwd, mkdir, path # firstWay + secondWay

from base64 import b64encode # firstWay
from struct import unpack #firstWay
from imghdr import what #firstWay

from pathlib import Path # secondWay
from svgtrace import trace # secondWay

def get_image_size_for_first_way(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if what(fname) == 'png':
            check = unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = unpack('>ii', head[16:24])
        elif what(fname) == 'gif':
            width, height = unpack('<HH', head[6:10])
        elif what(fname) == 'jpeg':
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
                    size = unpack('>H', fhandle.read(2))[0] - 2
                fhandle.seek(1, 1)
                height, width = unpack('>HH', fhandle.read(4))
            except Exception:
                return
        else:
            return
        return width, height

def firstWay_raster2vector():
    
    start_svg_tag = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
    """
    end_svg_tag = """</svg>"""
    
    for image in listdir(path2png):
        if image.endswith(".jpg") or image.endswith(".png") or image.endswith(".gif"):
            width, height = get_image_size_for_first_way(path2png + image)
            img_file = open(path2png + image, 'rb')
            base64data = b64encode(img_file.read())
            base64String = f'<image xlink:href="data:image/png;base64,{base64data.decode("utf-8")}" width="{width}" height="{height}" x="0" y="0" />'
            svg_size = f'width="{width}px" height="{height}px" viewBox="0 0 {width} {height}">'
            
            svg = open(path2svg + path.splitext(image)[0] + "[1].svg",'w')
            svg.write( start_svg_tag + svg_size + base64String + end_svg_tag)
            print ('Converted '+ image + ' to ' + path.splitext(image)[0]+".svg")





def secondWay_raster2vector(): 
    for image in listdir(path2png):
        if image.endswith(".jpg") or image.endswith(".png") or image.endswith(".gif"):
            Path(path2svg + image[0] + "[2].svg").write_text(trace(path2png + image), encoding="utf-8")





if __name__== '__main__':
    
    # if you do not have a folder, 
    # the program will create it, 
    # and you will have to put your images inside the folder
    if path.exists('image') == False: mkdir('image')
    
    path2png = getcwd() + "/image/"
    path2svg = getcwd() + "/svg/"
    if path.exists('svg') == False: mkdir('svg') # create a folder "svg"
    firstWay_raster2vector()
    secondWay_raster2vector()
