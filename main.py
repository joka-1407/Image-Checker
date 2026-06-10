from tkinter import * # type: ignore
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import math
import os


current_image_path = ""
image_info = ""
media_info = ""


def open_image_external():
    if not current_image_path:
        messagebox.showwarning("No Image", "Please select an image first.")
        return
    os.startfile(current_image_path)


def copy_info():
    root.clipboard_clear()
    root.clipboard_append(media_info)
    root.update()  # Keeps the clipboard content after the window is closed


def export_info():
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if filename:
        with open(filename, "w") as f:
            f.write(media_info)


def toggle_topmost():
    root.attributes("-topmost", stay_on_top.get())


# Function to open image and display its dimensions and aspect ratio
def open_image():
    global current_image_path, image_info, media_info
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )

    if not file_path:
        return
    current_image_path = file_path
    filename = os.path.basename(current_image_path)

    # Open the image and get dimensions
    try:
        img = Image.open(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image:\n{e}")
        return
    width, height = img.size
    # Get file size
    file_size = os.path.getsize(file_path)
    size_kb = file_size / 1024

    # Aspect ratio calculation
    divisor = math.gcd(width, height)

    aspect_width = width // divisor
    aspect_height = height // divisor

    # Resize preview
    preview = img.copy()
    preview.thumbnail((300, 300))

    photo = ImageTk.PhotoImage(preview)
    image_label.config(image=photo)
    image_label.image = photo # type: ignore

    image_info = (
        f"File Name: {filename}\n"
        f"Width: {width}px\n"
        f"Height: {height}px\n"
        f"Aspect Ratio: {aspect_width}:{aspect_height}\n"
    )

    media_info = (
        f"File Path: {current_image_path}\n"
        f"File Name: {filename}\n"
        f"Width: {width}px\n"
        f"Height: {height}px\n"
        f"Aspect Ratio: {aspect_width}:{aspect_height}\n"
        f"Resolution: {width} x {height}\n"
        f"Format: {img.format}\n"
        f"Mode: {img.mode}\n"
        f"File Size: {size_kb:.2f} KB\n"
    )

    info_label.config(text=image_info)


def show_menu():
    menu.tk_popup(
        three_dot_button.winfo_rootx(),
        three_dot_button.winfo_rooty() + 30
    )


def show_media_info():
    if current_image_path:
        messagebox.showinfo("Media Info", media_info)
    else:
        messagebox.showwarning("No Image", "Please select an image first.")


# Main Window
root = Tk()
stay_on_top = BooleanVar(value=False)
root.title("Image Dimension Checker")
root.geometry("500x800")
root.resizable(False, False)
menu = Menu(root, tearoff=0)

menu.add_command(
    label="Show Media Info",
    command=show_media_info
)

menu.add_command(
    label="Copy Image Information",
    command=copy_info
)

menu.add_command(
    label="Export Image Information",
    command=export_info
)

menu.add_separator()

menu.add_checkbutton(
    label="Always on Top",
    variable=stay_on_top,
    command=toggle_topmost
)

root.attributes("-topmost", False)


three_dot_button = Button(
    root,
    text="⋮",
    font=("Segoe UI", 14),
    command=show_menu
)

three_dot_button.place(x=450, y=10)


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

Button(
    root,
    text="Open in Photos",
    command=open_image_external,
).pack(pady=5)

Button(
    root,
    text="Copy Info",
    command=copy_info,
).pack(pady=5)

Button(
    root,
    text="Export Info",
    command=export_info,
).pack(pady=5)

image_label = Label(root)
image_label.pack(pady=10)

info_label = Label(root, text="Choose an image to see its dimensions and aspect ratio.",
                   font=("Arial", 12), justify=LEFT)
info_label.pack(pady=10)

root.mainloop()
