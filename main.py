from tkinter import *  # type: ignore
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
from PIL import ImageGrab
import requests
from io import BytesIO
import math
import os


current_image_path = ""
image_info = ""
media_info = ""


def open_image_external():

    if not current_image_path:
        messagebox.showwarning(
            "No Image",
            "Please select an image first."
        )
        return

    if (
        current_image_path.startswith("http://")
        or current_image_path.startswith("https://")
        or current_image_path == "Clipboard"
    ):
        messagebox.showinfo(
            "Unavailable",
            "This image does not exist as a local file."
        )
        return

    os.startfile(current_image_path)


def prompt_for_url():

    url = simpledialog.askstring(
        "Analyze Image URL",
        "Enter an image URL:"
    )

    if not url:
        return

    load_image_from_url(url)


def copy_info():
    if not media_info:
        messagebox.showwarning(
            "No Image",
            "Please select an image first."
        )
        return
    
    root.clipboard_clear()
    root.clipboard_append(media_info)
    root.update()  # Keeps the clipboard content after the window is closed

    messagebox.showinfo(
        "Copied",
        "Image information copied to clipboard."
    )


def export_info():
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if filename:
        with open(filename, "w") as f:
            f.write(media_info)
        messagebox.showinfo("Export Successful", "Image information exported.")


def toggle_topmost():
    root.attributes("-topmost", stay_on_top.get())


# Function to open image and display its dimensions and aspect ratio
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"), ("All files", "*.*")]
    )

    if not file_path:
        return

    # Open the image and get dimensions
    try:
        img = Image.open(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image:\n{e}")
        return

    # Get file size
    file_size = os.path.getsize(file_path)
    size_kb = file_size / 1024
    file_size_info = f"{size_kb:.2f} KB"

    load_image(
        img, source_name=os.path.basename(file_path), source_path=file_path, file_size_info=file_size_info
    )


def load_image(img, source_name="Clipboard", source_path="", file_size_info="Unknown"):

    global current_image_path, image_info, media_info

    current_image_path = source_path

    width, height = img.size

    divisor = math.gcd(width, height)

    aspect_width = width // divisor
    aspect_height = height // divisor

    ratio_names = {
        (16, 9): "Widescreen",
        (9, 16): "Vertical Video",
        (1, 1): "Square",
        (4, 3): "Standard",
        (3, 2): "Photography",
        (21, 9): "Ultrawide"
    }

    ratio_type = ratio_names.get(
        (aspect_width, aspect_height),
        "Custom"
    )

    preview = img.copy()
    preview.thumbnail((300, 300))

    photo = ImageTk.PhotoImage(preview)

    image_label.config(image=photo, text="")
    image_label.image = photo  # type: ignore

    image_info = (
        f"File Name: {source_name}\n"
        f"Width: {width}px\n"
        f"Height: {height}px\n"
        f"Aspect Ratio: {aspect_width}:{aspect_height}\n"
        f"Type: {ratio_type}"
    )

    media_info = (
        f"File Path: {source_path}\n"
        f"File Name: {source_name}\n"
        f"Width: {width}px\n"
        f"Height: {height}px\n"
        f"Aspect Ratio: {aspect_width}:{aspect_height}\n"
        f"Resolution: {width} x {height}\n"
        f"Format: {img.format}\n"
        f"Mode: {img.mode}\n"
        f"File Size: {file_size_info}\n"
    )

    info_label.config(text=image_info)


def copy_path():
    if not current_image_path:
        messagebox.showwarning(
            "No Image",
            "Please select an image first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(current_image_path)
    root.update()
    messagebox.showinfo(
        "Copied",
        "Image path copied to clipboard."
    )


def paste_image(event=None):

    try:
        clipboard_content = ImageGrab.grabclipboard()

        # Case 1: Actual image data
        if isinstance(clipboard_content, Image.Image):

            load_image(
                clipboard_content,
                source_name="Clipboard Image",
                source_path="Clipboard",
                file_size_info="Clipboard Image"
            )

            return

        if isinstance(clipboard_content, list):
            file_path = clipboard_content[0]

            valid_extensions = (".jpg", ".jpeg", ".png",
                                ".bmp", ".gif", ".webp")
            if not file_path.lower().endswith(valid_extensions):
                messagebox.showwarning(
                    "Invalid File",
                    "The dropped file is not a supported image format."
                )
                return

            img = Image.open(file_path)

            load_image(
                img,
                source_name=os.path.basename(file_path),
                source_path=file_path,
                file_size_info=f"{os.path.getsize(file_path)/1024:.2f} KB"
            )
            return

        # Case 2: Text in clipboard
        try:
            clipboard_text = root.clipboard_get().strip()

            if (
                clipboard_text.startswith("http://")
                or clipboard_text.startswith("https://")
            ):

                load_image_from_url(clipboard_text)
                return

        except TclError:
            pass

        messagebox.showwarning(
            "No Image Found",
            "Clipboard does not contain an image or image URL."
        )

    except Exception as e:
        messagebox.showerror(
            "Paste Error",
            str(e)
        )


def drop_image(event):
    global current_image_path
    file_path = root.tk.splitlist(
        event.data
    )[0]
    
    try:
        img = Image.open(file_path)
        filename = os.path.basename(file_path)
        current_image_path = file_path
        file_size = os.path.getsize(file_path)
        load_image(
            img,
            filename,
            file_path,
            f"{file_size/1024:.2f} KB"
        )
    except Exception as e:
        messagebox.showerror("Drop Error", str(e))


def load_image_from_url(url):

    if not (
        url.startswith("http://")
        or url.startswith("https://")
    ):
        messagebox.showerror(
            "Invalid URL",
            "Please enter a valid URL."
        )
        return

    try:
        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()
        
        content_type = response.headers.get("Content-Type", "")
        
        if not content_type.startswith("image/"):
            raise Exception(
                "URL does not point to an image."
            )

        img = Image.open(
            BytesIO(response.content)
        )

        filename = url.split("/")[-1]
        if "." not in filename:
            filename = "Image from URL"

        load_image(
            img,
            source_name=filename,
            source_path=url,
            file_size_info=f"{len(response.content)/1024:.2f} KB"
        )

    except Exception as e:
        messagebox.showerror(
            "URL Error",
            f"Could not load image:\n{e}"
        )


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
root = TkinterDnD.Tk()
stay_on_top = BooleanVar(value=False)
root.title("Image Dimension Checker")
root.geometry("500x600")
root.resizable(False, False)
root.bind("<Control-v>", paste_image)
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

menu.add_command(
    label="Copy as Path",
    command=copy_path
)

menu.add_command(
    label="Analyze Image URL",
    command=prompt_for_url
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
    text="Analyze URL",
    command=prompt_for_url
).pack(pady=5)

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

image_label = Label(root, text="Drop Image Here\n\n or \n\nPaste (Ctrl+V)",
                    font=("Arial", 14), width=40, height=15, bg="#f0f0f0", relief="groove")
image_label.pack(pady=10)

image_label.drop_target_register(DND_FILES) # type: ignore
image_label.dnd_bind("<<Drop>>", drop_image) # type: ignore


info_label = Label(root, text="Choose an image to see its dimensions and aspect ratio.",
                   font=("Arial", 12), justify=LEFT)
info_label.pack(pady=10)

root.mainloop()
