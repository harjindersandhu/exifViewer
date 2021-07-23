from tkinter import *
import PIL
from PIL import ImageTk, Image
from tkinter import filedialog
import tkinter as tk
from PIL.ExifTags import TAGS, GPSTAGS
from exifread.tags import exif


global exif_text


def browse_image():
    global image_object, image_loaded_label
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                               filetypes=(("jpeg files", "*.jpeg"), ("png files", "*.png")))
    image = Image.open(root.filename)
    image_object = image.resize((450, 350), Image.ANTIALIAS)
    image_loaded = ImageTk.PhotoImage(image_object)
    img_lbl.configure(image=image_loaded)
    img_lbl.image = image_loaded
    exif_lbl.configure(text="")


def rotate_image(direction):
    global image_object
    angle = {"left": 90, "right": -90}[direction]
    image_object = image_object.rotate(angle)
    rotated_tk = ImageTk.PhotoImage(image_object)
    img_lbl.config(image=rotated_tk)
    img_lbl.image = rotated_tk #Prevent garbage collection


def get_exif():
    global image_object
    exifdata = image_object.getexif()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")


def insert_text():
    global exif_text
    exif_text = "calamdanrei"
    exif_lbl.configure(text=exif_text)


root = tk.Tk()
root.title('Exif Viewer')
root.geometry('500x550')
root.iconbitmap("/icons/exif.png")

info_frame = Frame(root)
info_frame.pack(side=TOP)


image_frame = Frame(info_frame)
image_frame.grid(row=0, column=0)

exif_frame = LabelFrame(info_frame)
exif_frame.grid(row=1, column=0)


img_lbl = Label(image_frame)
img_lbl.grid(row=0, column=0)


exif_lbl = Message(exif_frame, font=("helvetica", 18), aspect=200)
exif_lbl.grid(row=1, column=0)

listbox = Listbox(exif_frame)

buttons_frame = Frame(root, padx=5, pady=5)
# buttons_frame.grid_columnconfigure(0, weight=1)


browse_button = Button(buttons_frame, padx=20, pady=5, text="Load image", command=browse_image)
browse_button.grid(row=0, column=0)

rotate_left_button = Button(buttons_frame, padx=10, pady=5, text="Rotate left", command=lambda: rotate_image("left"))
rotate_left_button.grid(row=0, column=1)

rotate_right_button = Button(buttons_frame, padx=10, pady=5, text="Rotate right", command=lambda: rotate_image("right"))
rotate_right_button.grid(row=0, column=2)

get_exif = Button(buttons_frame, padx=20, pady=5, text="Get EXIF", command=get_exif)
get_exif.grid(row=0, column=3)

exit_button = Button(buttons_frame, padx=20, pady=5, text="Exit", command=root.quit)
exit_button.grid(row=0, column=4)

buttons_frame.pack(side=BOTTOM)


root.mainloop()