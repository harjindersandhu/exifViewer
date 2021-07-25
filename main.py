from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter as tk
from PIL.ExifTags import TAGS, GPSTAGS


global exif_text


# Function that browse image
def browse_image():
    global image_object, image_loaded_label
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                               filetypes=(("jpeg files", "*.jpeg"),("png files", "*.png")))
    openimage(root.filename)
    listbox.delete(0, 'end')


# Function that opens image loaded
def openimage(uri):
    global image_object

    image = Image.open(uri)
    image_object = image.resize((450, 350), Image.ANTIALIAS)
    image_loaded = ImageTk.PhotoImage(image_object)
    img_lbl.configure(image=image_loaded)
    img_lbl.image = image_loaded


# Rotating image left and right
def rotate_image(direction):
    global image_object
    angle = {"left": 90, "right": -90}[direction]
    image_object = image_object.rotate(angle)
    rotated_tk = ImageTk.PhotoImage(image_object)
    img_lbl.config(image=rotated_tk)
    img_lbl.image = rotated_tk  # Prevent garbage collection


# Exif data of image
def get_exif():
    global image_object, listbox
    listbox = Listbox(exif_frame,width=50, height=8)
    listbox.grid(row=2, column=0)
    try:
        exif = image_object.getexif()
    except AttributeError:
        return {}
    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value
        listbox.insert(END, tag + ':  ' + str(exif_table[tag])) # Insert data into a list


root = tk.Tk()
root.title('Exif Viewer')
root.geometry('500x550')
root.iconbitmap("icons/exif.png")
root.minsize(500, 550)
root.maxsize(500, 550)

info_frame = Frame(root)
info_frame.pack(side=TOP)

image_frame = Frame(info_frame)
image_frame.grid(row=0, column=0)

exif_frame = LabelFrame(info_frame)
exif_frame.grid(row=1, column=0)

img_lbl = Label(image_frame)
img_lbl.grid(row=0, column=0)

buttons_frame = Frame(root, padx=5, pady=5)

browse_button = Button(buttons_frame, padx=20, pady=5, text="Load image",
                       command=browse_image)
browse_button.grid(row=0, column=0)

rotate_left_button = Button(buttons_frame, padx=10, pady=5, text="Rotate left",
                            command=lambda: rotate_image("left"))
rotate_left_button.grid(row=0, column=1)

rotate_right_button = Button(buttons_frame, padx=10, pady=5, text="Rotate right",
                             command=lambda: rotate_image("right"))
rotate_right_button.grid(row=0, column=2)

exif_btn = Button(buttons_frame, padx=20, pady=5, text="Get EXIF",
                  command=get_exif)
exif_btn.grid(row=0, column=3)

exit_button = Button(buttons_frame, padx=20, pady=5, text="Exit",
                     command=root.quit)
exit_button.grid(row=0, column=4)

buttons_frame.pack(side=BOTTOM)

openimage('images/sample.jpeg')
get_exif()
root.mainloop()
