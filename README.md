image-2-coe
===========

- Python 3.7 script to convert an image to the Xilinx .coe format.
- Can also convert an image to risc-v code, saving the image into block ram.

To Use
-------
Copy the image2coe.py file to the directory where your image resides.
Open a terminal and change to the same directory. 
Run the image2coe.py file by typing:
`python3 image2coe.py`
You will be prompted for the name of your image. Enter it and hit the return key.

When you make your BRAM in Xilinx select 'Simple Dual RAM' and enter '8' as the Read Width and the number that is returned in the terminal as Total addresses as the Read Depth.
