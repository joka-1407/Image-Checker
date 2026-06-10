from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import math


# Function to open image and display its dimensions and aspect ratio
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )

    if not file_path:
        return

    # Open the image and get dimensions
    img = Image.open(file_path)
    width, height = img.size

    # Aspect ratio calculation
    divisor = math.gcd(width, height)

    aspect_width = width // divisor
    aspect_height = height // divisor

    # Resize preview
    preview = img.copy()
    preview.thumbnail((300, 300))

    photo = ImageTk.PhotoImage(preview)
    image_label.config(image=photo)
    image_label.image = photo

    info_label.config(
        text=f"Width: {width}px\nHeight: {height}px\nAspect Ratio: {aspect_width}:{aspect_height}\nResolution: {width}x{height}"
    )


# Main Window
root = Tk()
root.title("Image Dimension Checker")
root.geometry("500x600")
root.resizable(False, False)


title_label = Label(
    root,
    text="Image Dimension Checker",
    font=("Arial", 20, "bold"),
)
title_label.pack(pady=10)

Button(
    root,
    text="Select Image",
    font=("Arial", 14),
    command=open_image,
).pack(pady=10)

image_label = Label(root)
image_label.pack(pady=10)

info_label = Label(root, text="Choose an image to see its dimensions and aspect ratio.",
                   font=("Arial", 12), justify=LEFT)
info_label.pack(pady=10)

root.mainloop()
