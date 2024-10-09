import pyqrcode
import tkinter
# Create and render the QR code
code = pyqrcode.create('Knights who say ni!')
code_xbm = code.xbm(scale=5)
# Create a tk window
top = tkinter.Tk()
# Make generate the bitmap image from the redered code
code_bmp = tkinter.BitmapImage(data=code_xbm)
# Set the code to have a white background,
# instead of transparent
code_bmp.config(background="white")
# Bitmaps are accepted by lots of Widgets
label = tkinter.Label(image=code_bmp)
# The QR code is now visible
label.pack()
top.mainloop()