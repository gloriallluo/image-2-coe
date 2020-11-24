# Imported Standard Modules
import sys
from PIL import Image


def Convert(image_name):
    """
    将一张 800 * 600 的图片转化为 .bin 文件。
    """
    # Open image
    img = Image.open(image_name)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Store Width and height of image
    width = img.size[0]
    height = img.size[1]

    filetype = image_name[image_name.find('.'):]
    filename = image_name.replace(filetype, '.bin')
    with open(filename, 'wb') as imgbin:
        for r in range(0, height):
            for c in range(0, width):
                # Check for IndexError, usually occurs if the script is trying to
                # access an element that does not exist
                try:
                    R, G, B = img.getpixel((c, r))
                except IndexError:
                    print('Index Error Occurred At:')
                    print(f'c: {c}, r: {r}')
                    sys.exit()
                rb = bin(R)[2:].zfill(8)[:3]
                gb = bin(G)[2:].zfill(8)[:3]
                bb = bin(B)[2:].zfill(8)[:2]

            out_byte = rb + gb + bb
            # Check for Value Error, happened when the case of the pixel being
            # zero was not handled properly
            try:
                imgbin.write(bytes('%2.2X' % int(out_byte, 2), encoding='utf8'))
            except ValueError:
                print('Value Error Occurred At:')
                print(f'Contents of out_byte: {out_byte} at r:{r} c:{c}')
                print(f'R: {R} G: {G} B: {B}')
                print(f'Rb: {rb} gb: {gb} Bb: {bb}')
                sys.exit()
    print(f'Xilinx Coefficients File:{filename} DONE')
    print(f'Converted from {filetype} to .coe')
    print(f'Size: h:{height} pixels w:{width} pixels')


if __name__ == '__main__':
    ImageName = input('Enter the name of your image: ')
    Convert(ImageName)
