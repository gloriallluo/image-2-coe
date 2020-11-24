# Imported Standard Modules
import sys
from PIL import Image


def Convert(image_name):
    """
    This converts the given image into a risc-v (.s) file.
    Pass it the name of the image including the file suffix.
    The file must reside in the directory from which this function is called
    or provide the absolute path.
    """
    # Open image
    img = Image.open(image_name)
    # Verify that the image is in the 'RGB' mode, every pixel is described by
    # three bytes
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Store Width and height of image
    width = img.size[0]
    height = img.size[1]

    # Create a . file and open it.
    # Write the header to the file, where lines that start with ';'
    # are commented
    filetype = image_name[image_name.find('.'):]
    filename = image_name.replace(filetype, '.s')
    with open(filename, 'w') as img_riscv:
        img_riscv.write("\t.org 0x0\n")
        img_riscv.write("\t.global _start\n")
        img_riscv.write("\t.text\n")
        img_riscv.write("\n_start:\n")

        # Iterate through every pixel, retain the 3 least significant bits for the
        # red and green bytes and the 2 least significant bits for the blue byte.
        # These are then combined into one byte and their hex equivalent is written
        # to the .coe file
        cnt = 0
        line_cnt = 0
        for r in range(0, height):
            for c in range(0, width):
                cnt += 1
                # Check for IndexError, usually occurs if the script is trying to
                # access an element that does not exist
                try:
                    R, G, B = img.getpixel((c, r))
                except IndexError:
                    print('Index Error Occurred At:')
                    print(f'c: {c}, r: {r}')
                    sys.exit()
                # convert the value (0-255) to a binary string by cutting off the
                # '0b' part and left filling zeros until the string represents 8 bits
                # then slice off the bits of interest with [5:] for red and green
                # or [6:] for blue
                Rb = bin(R)[2:].zfill(8)[:3]
                Gb = bin(G)[2:].zfill(8)[:3]
                Bb = bin(B)[2:].zfill(8)[:2]

                Outbyte = Rb + Gb + Bb
                # Check for Value Error, happened when the case of the pixel being
                # zero was not handled properly
                try:
                    img_riscv.write('%2.2X' % int(Outbyte, 2))
                except ValueError:
                    print('Value Error Occurred At:')
                    print(f'Contents of Outbyte: {Outbyte} at r:{r} c:{c}')
                    print(f'R: {R} G: {G} B: {B}')
                    print(f'Rb: {Rb} Gb: {Gb} Bb: {Bb}')
                    sys.exit()
                # Write correct punctuation depending on line end, byte end or file end
                if cnt % 8 == 0:
                    line_cnt += 1
    print(f'risc-v File: {filename} DONE')
    print(f'Converted from {filetype} to .s')


if __name__ == '__main__':
    image_name = input('Enter the name of your image: ')
    Convert(image_name)
