# Imported Standard Modules
import sys
from PIL import Image


def Convert(image_name):
    """
    输入为一张图片，输出为将这张图片存储至 Block RAM 的 riscv 代码。
    为了减轻码量，输入必须是一张 200 * 150 的图片。
    而 Block RAM 中存储的是 4 * 4 * 这张图片。
    """
    # Open image
    img = Image.open(image_name)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Store Width and height of image
    width = img.size[0]
    height = img.size[1]
    if width != 200 or height != 150:
        print(f'Image Size Error: {height}, {width}')
        sys.exit()

    # config in riscv code
    i = 't0'
    j = 't1'
    count = 't2'
    base_addr = 'a0'
    addr = 'a1'
    line_offset = 'a2'
    large_line_offset = 'a3'
    color = 'a4'
    offset = 4  # TODO: offset not sure

    # Create a .s file and open it.
    # Write the header to the file, where lines that start with ';'
    # are commented
    filetype = image_name[image_name.find('.'):]
    filename = image_name.replace(filetype, '.s')
    with open(filename, 'w') as img_riscv:
        img_riscv.write("\t.org 0x0\n")
        img_riscv.write("\t.global _start\n")
        img_riscv.write("\t.text\n")
        img_riscv.write("_start:\n")

        # initialization code
        img_riscv.write(f"\tori {count}, zero, 4\n")
        img_riscv.write(f"\tori {base_addr}, zero, 0\n")    # TODO: base_addr initialization not sure
        img_riscv.write(f"\tori {line_offset}, zero, {offset * 600}\n")
        img_riscv.write(f"\tori {large_line_offset}, zero, 0x268\n")
        img_riscv.write(f"\tlui {large_line_offset}, 0x1d\n")

        # in outer loop, save a line
        img_riscv.write(f"\tori {i}, zero, 0\n")
        img_riscv.write("_OUTER_LOOP:\n")

        # in inner loop
        img_riscv.write(f"\tori {j}, zero, 0\n")
        img_riscv.write(f"_INNER_LOOP:\n")

        # save one picture
        img_riscv.write(f"\tor {addr}, zero, {base_addr}\n")

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
                rb = bin(R)[2:].zfill(8)[:3]
                gb = bin(G)[2:].zfill(8)[:3]
                bb = bin(B)[2:].zfill(8)[:2]

                out_byte = rb + gb + bb
                # Check for Value Error, happened when the case of the pixel being
                # zero was not handled properly
                try:
                    img_riscv.write(f"\tori {color}, zero, {int(out_byte, 2)}\n")
                    img_riscv.write(f"\twb {color}, 0({addr})\n")
                    img_riscv.write(f"\taddi {addr}, {addr}, {offset}\n")
                except ValueError:
                    print('Value Error Occurred At:')
                    print(f'Contents of out_byte: {out_byte} at r:{r} c:{c}')
                    print(f'R: {R} G: {G} B: {B}')
                    print(f'Rb: {rb} Gb: {gb} Bb: {bb}')
                    sys.exit()

            line_cnt += 1
            img_riscv.write(f"\taddi {addr}, {addr}, {line_offset}\n")

        # inner loop
        img_riscv.write(f"\taddi {base_addr}, {base_addr}, {offset * 200}\n")
        img_riscv.write(f"\taddi {j}, {j}, 1\n")
        img_riscv.write(f"\tbne {j}, {count}, _INNER_LOOP\n")

        # outer loop
        img_riscv.write(f"\tadd {base_addr}, {base_addr}, {large_line_offset}\n")
        img_riscv.write(f"\taddi {i}, {i}, 1\n")
        img_riscv.write(f"\tbne {i}, {count}, _OUTER_LOOP\n")
    print(f'RISC-V File: {filename} DONE')
    print(f'Converted from {filetype} to .s')


if __name__ == '__main__':
    _image_name = input('Enter the name of your image: ')
    Convert(_image_name)
