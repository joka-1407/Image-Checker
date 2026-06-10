from tkinter import *  # type: ignore
from tkinter import filedialog, messagebox, simpledialog, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk, ImageGrab
import requests
from io import BytesIO
import math
import os

# ════════════════════════════════════════════════════════════════════════════
#  Theme
# ════════════════════════════════════════════════════════════════════════════

THEMES = {
    "light": dict(
        bg="#F2F2F7",   surface="#FFFFFF",    border="#D1D1D6",
        accent="#007AFF", accent_h="#0056CC",
        text="#1C1C1E", text_sub="#8E8E93",
        drop_bg="#EEF4FF", drop_bd="#C0D8FF",
        status_bg="#E5E5EA",
        btn_bg="#007AFF", btn_fg="#FFFFFF",
        sec_bg="#E5E5EA", sec_fg="#1C1C1E",
        row_alt="#F7F7FA",
    ),
    "dark": dict(
        bg="#1C1C1E",   surface="#2C2C2E",    border="#3A3A3C",
        accent="#0A84FF", accent_h="#409CFF",
        text="#F2F2F7", text_sub="#98989D",
        drop_bg="#2C2C2E", drop_bd="#48484A",
        status_bg="#111113",
        btn_bg="#0A84FF", btn_fg="#FFFFFF",
        sec_bg="#3A3A3C", sec_fg="#F2F2F7",
        row_alt="#323234",
    ),
}

_theme = "light"
def T(k): return THEMES[_theme][k]

# ════════════════════════════════════════════════════════════════════════════
#  App State
# ════════════════════════════════════════════════════════════════════════════


current_image_path = ""
image_info = ""
media_info = ""
_pil_image = None   # stored original for dynamic re-thumbnailing

# ════════════════════════════════════════════════════════════════════════════
#  Preview Helper
# ════════════════════════════════════════════════════════════════════════════


def _refresh_preview():
    """Re-thumbnail the stored PIL image to fill the current preview card."""
    if _pil_image is None:
        return
    root.update_idletasks()
    pw = max(preview_card.winfo_width() - 24, 100)
    ph = max(preview_card.winfo_height() - 24, 80)
    thumb = _pil_image.copy()
    thumb.thumbnail((pw, ph), Image.LANCZOS)  # type: ignore
    photo = ImageTk.PhotoImage(thumb)
    preview_lbl.config(image=photo, text="")
    preview_lbl.image = photo  # type: ignore

# ════════════════════════════════════════════════════════════════════════════
#  Actions
# ════════════════════════════════════════════════════════════════════════════


def open_image_external():
    if not current_image_path:
        messagebox.showwarning("No Image", "Please select an image first.")
        return
    if current_image_path.startswith("http") or current_image_path == "Clipboard":
        messagebox.showinfo("Unavailable", "This image is not a local file.")
        return
    os.startfile(current_image_path)


def prompt_for_url():
    url = simpledialog.askstring("Analyze Image URL", "Enter an image URL:")
    if url:
        load_image_from_url(url)


def copy_info():
    if not media_info:
        messagebox.showwarning("No Image", "Please select an image first.")
        return
    root.clipboard_clear()
    root.clipboard_append(media_info)
    root.update()
    messagebox.showinfo("Copied", "Image information copied to clipboard.")


def export_info():
    fn = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if fn:
        with open(fn, "w") as f:
            f.write(media_info)
        messagebox.showinfo("Exported", "Image information exported.")


def toggle_topmost():
    root.attributes("-topmost", stay_on_top.get())


def toggle_theme():
    global _theme
    _theme = "dark" if dark_mode.get() else "light"
    apply_theme()


def open_image():
    fp = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                   ("All files", "*.*")]
    )
    if not fp:
        return
    try:
        img = Image.open(fp)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image:\n{e}")
        return
    load_image(img, os.path.basename(fp), fp,
               f"{os.path.getsize(fp) / 1024:.2f} KB")


def load_image(img, source_name="Clipboard", source_path="", file_size_info="Unknown"):
    global current_image_path, image_info, media_info, _pil_image

    current_image_path = source_path
    _pil_image = img.copy()
    width, height = img.size
    d = math.gcd(width, height)
    aw, ah = width // d, height // d
    ratio_type = {
        (16, 9):  "Widescreen",
        (9,  16): "Vertical Video",
        (1,  1):  "Square",
        (4,  3):  "Standard",
        (3,  2):  "Photography",
        (21, 9):  "Ultrawide",
    }.get((aw, ah), "Custom")

    _refresh_preview()
    placeholder_lbl.pack_forget()
    preview_lbl.pack(expand=True, fill=BOTH)

    media_info = (
        f"File Path: {source_path}\n"
        f"File Name: {source_name}\n"
        f"Width: {width}px\n"
        f"Height: {height}px\n"
        f"Aspect Ratio: {aw}:{ah}\n"
        f"Resolution: {width} x {height}\n"
        f"Format: {img.format}\n"
        f"Mode: {img.mode}\n"
        f"File Size: {file_size_info}"
    )
    image_info = (
        f"File Name: {source_name}\n"
        f"Width: {width}px\n"
        f"Height: {height}px\n"
        f"Aspect Ratio: {aw}:{ah}\n"
        f"Type: {ratio_type}"
    )

    _set_info_rows([
        ("File Name",    source_name),
        ("Dimensions",   f"{width} x {height} px"),
        ("Aspect Ratio", f"{aw}:{ah}"),
        ("Type",         ratio_type),
        ("Format",       str(img.format or "-")),
        ("Color Mode",   img.mode),
        ("File Size",    file_size_info),
        ("Source",       source_path or "-"),
    ])

    status_var.set(f"  {source_name}   *   {width} x {height} px")


def copy_path():
    if not current_image_path:
        messagebox.showwarning("No Image", "Please select an image first.")
        return
    root.clipboard_clear()
    root.clipboard_append(current_image_path)
    root.update()
    messagebox.showinfo("Copied", "Image path copied to clipboard.")


def paste_image(event=None):
    try:
        cc = ImageGrab.grabclipboard()
        if isinstance(cc, Image.Image):
            load_image(cc, "Clipboard Image", "Clipboard", "N/A")
            return
        if isinstance(cc, list):
            fp = cc[0]
            if not fp.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")):
                messagebox.showwarning(
                    "Invalid File", "Not a supported image format.")
                return
            try:
                img = Image.open(fp)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image:\n{e}")
                return
            load_image(img, os.path.basename(fp), fp,
                       f"{os.path.getsize(fp) / 1024:.2f} KB")
            return
        try:
            ct = root.clipboard_get().strip()
            if ct.startswith("http://") or ct.startswith("https://"):
                load_image_from_url(ct)
                return
        except TclError:
            pass
        messagebox.showwarning("No Image", "Clipboard has no image or URL.")
    except Exception as e:
        messagebox.showerror("Paste Error", str(e))


def drop_image(event):
    fp = root.tk.splitlist(event.data)[0]
    if not fp.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp")):
        messagebox.showwarning("Invalid File", "Not a supported image format.")
        return
    try:
        img = Image.open(fp)
        load_image(img, os.path.basename(fp), fp,
                   f"{os.path.getsize(fp) / 1024:.2f} KB")
    except Exception as e:
        messagebox.showerror("Drop Error", str(e))


def load_image_from_url(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        messagebox.showerror("Invalid URL", "Please enter a valid URL.")
        return
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        if not r.headers.get("Content-Type", "").startswith("image/"):
            raise Exception("URL does not point to an image.")
        img = Image.open(BytesIO(r.content))
        fn = url.split("/")[-1]
        if "." not in fn:
            fn = "Image from URL"
        load_image(img, fn, url, f"{len(r.content) / 1024:.2f} KB")
    except Exception as e:
        messagebox.showerror("URL Error", f"Could not load image:\n{e}")


def show_menu():
    menu.tk_popup(menu_btn.winfo_rootx(), menu_btn.winfo_rooty() + 34)


def show_media_info():
    if current_image_path:
        messagebox.showinfo("Media Info", media_info)
    else:
        messagebox.showwarning("No Image", "Please select an image first.")

# ════════════════════════════════════════════════════════════════════════════
#  Info Panel
# ════════════════════════════════════════════════════════════════════════════


_rows = []  # [(row_frame, key_label, val_label)]


def _set_info_rows(data):
    global _rows
    for rf, _, __ in _rows:
        rf.destroy()
    _rows = []

    for i, (k, v) in enumerate(data):
        bg = T("surface") if i % 2 == 0 else T("row_alt")
        rf = Frame(info_inner, bg=bg)
        rf.pack(fill=X)

        kl = Label(rf, text=k, font=("Segoe UI", 9),
                   bg=bg, fg=T("text_sub"), width=13,
                   anchor=W, padx=10, pady=9)
        kl.pack(side=LEFT)

        Frame(rf, width=1, bg=T("border")).pack(side=LEFT, fill=Y, pady=4)

        vl = Label(rf, text=v, font=("Segoe UI", 9, "bold"),
                   bg=bg, fg=T("text"), anchor=W, padx=10)
        vl.pack(side=LEFT, fill=X, expand=True)

        _rows.append((rf, kl, vl))

    info_inner.update_idletasks()
    info_canvas.configure(scrollregion=info_canvas.bbox("all"))

# ════════════════════════════════════════════════════════════════════════════
#  Theme Application
# ════════════════════════════════════════════════════════════════════════════


def apply_theme():
    root.config(bg=T("bg"))
    header_frame.config(bg=T("surface"))
    title_lbl.config(bg=T("surface"), fg=T("text"))
    menu_btn.config(bg=T("surface"), fg=T("text"),
                    activebackground=T("border"), activeforeground=T("text"))
    header_div.config(bg=T("border"))
    toolbar_frame.config(bg=T("bg"))

    for btn, acc in _btns:
        if acc:
            btn.config(bg=T("btn_bg"), fg=T("btn_fg"),
                       activebackground=T("accent_h"), activeforeground=T("btn_fg"))
        else:
            btn.config(bg=T("sec_bg"), fg=T("sec_fg"),
                       activebackground=T("border"), activeforeground=T("sec_fg"))

    preview_card.config(bg=T("drop_bg"), highlightbackground=T("drop_bd"))
    preview_lbl.config(bg=T("drop_bg"))
    placeholder_lbl.config(bg=T("drop_bg"), fg=T("text_sub"))

    info_section.config(bg=T("bg"))
    info_header_lbl.config(bg=T("bg"), fg=T("text_sub"))
    info_wrap.config(bg=T("bg"))
    info_canvas.config(bg=T("surface"), highlightbackground=T("border"))
    info_inner.config(bg=T("surface"))

    for i, (rf, kl, vl) in enumerate(_rows):
        bg = T("surface") if i % 2 == 0 else T("row_alt")
        rf.config(bg=bg)
        kl.config(bg=bg, fg=T("text_sub"))
        vl.config(bg=bg, fg=T("text"))
        for child in rf.winfo_children():
            if isinstance(child, Frame):
                child.config(bg=T("border"))

    status_bar.config(bg=T("status_bg"))
    status_lbl.config(bg=T("status_bg"), fg=T("text_sub"))

    menu.config(bg=T("surface"), fg=T("text"),
                activebackground=T("accent"), activeforeground=T("btn_fg"))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Thin.Vertical.TScrollbar",
                    background=T("border"),
                    troughcolor=T("surface"),
                    arrowcolor=T("text_sub"),
                    bordercolor=T("surface"),
                    lightcolor=T("surface"),
                    darkcolor=T("surface"),
                    arrowsize=12)
    style.map("Thin.Vertical.TScrollbar",
              background=[("active", T("accent"))])

# ════════════════════════════════════════════════════════════════════════════
#  UI Construction
# ════════════════════════════════════════════════════════════════════════════


root = TkinterDnD.Tk()
root.title("Peekture")
root.geometry("520x760")
root.resizable(False, False)
root.bind("<Control-v>", paste_image)

stay_on_top = BooleanVar(value=False)
dark_mode = BooleanVar(value=False)

# ── Header ────────────────────────────────────────────────────────────────────

header_frame = Frame(root, height=52)
header_frame.pack(fill=X)
header_frame.pack_propagate(False)

title_lbl = Label(header_frame, text="Peekture",
                  font=("Segoe UI", 13, "bold"))
title_lbl.pack(side=LEFT, padx=16)

menu_btn = Button(header_frame, text="...", font=("Segoe UI", 13, "bold"),
                  bd=0, relief=FLAT, cursor="hand2",
                  command=show_menu, padx=10, pady=2)
menu_btn.pack(side=RIGHT, padx=6)

header_div = Frame(root, height=1)
header_div.pack(fill=X)

# ── Toolbar ───────────────────────────────────────────────────────────────────

toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X, padx=16, pady=12)

_btns = []


def _btn(parent, label, cmd, accent=True):
    b = Button(parent, text=label, font=("Segoe UI", 10),
               bd=0, relief=FLAT, cursor="hand2",
               padx=14, pady=8, command=cmd)
    _btns.append((b, accent))
    b.bind("<Enter>", lambda e: b.config(
        bg=T("accent_h") if accent else T("border")))
    b.bind("<Leave>", lambda e: b.config(
        bg=T("btn_bg") if accent else T("sec_bg")))
    return b


_btn(toolbar_frame, "Select Image",   open_image,
     True).pack(side=LEFT, padx=(0, 8))
_btn(toolbar_frame, "Analyze URL",    prompt_for_url,
     False).pack(side=LEFT, padx=(0, 8))
_btn(toolbar_frame, "Open in Photos", open_image_external, False).pack(side=LEFT)

# ── Preview Card ──────────────────────────────────────────────────────────────

preview_card = Frame(root, height=300, highlightthickness=2)
preview_card.pack(fill=X, padx=16, pady=(0, 10))
preview_card.pack_propagate(False)

placeholder_lbl = Label(
    preview_card,
    text="Drop image here\n\nor  Ctrl+V  to paste",
    font=("Segoe UI", 12),
    justify=CENTER
)
placeholder_lbl.pack(expand=True)

preview_lbl = Label(preview_card)
# Not packed until an image is loaded

preview_card.drop_target_register(DND_FILES)   # type: ignore
preview_card.dnd_bind("<<Drop>>", drop_image)  # type: ignore


def _drag_enter(e): preview_card.config(highlightbackground=T("accent"))
def _drag_leave(e): preview_card.config(highlightbackground=T("drop_bd"))


try:
    preview_card.dnd_bind("<<DropEnter>>", _drag_enter)  # type: ignore
    preview_card.dnd_bind("<<DropLeave>>", _drag_leave)  # type: ignore
except Exception:
    pass

# ── Info Section ──────────────────────────────────────────────────────────────

info_section = Frame(root)
info_section.pack(fill=BOTH, expand=True, padx=16, pady=(0, 8))

info_header_lbl = Label(info_section, text="IMAGE INFO",
                        font=("Segoe UI", 8, "bold"), anchor=W, pady=6)
info_header_lbl.pack(fill=X)

info_wrap = Frame(info_section)
info_wrap.pack(fill=BOTH, expand=True)

info_canvas = Canvas(info_wrap, bd=0, highlightthickness=1)
info_canvas.pack(side=LEFT, fill=BOTH, expand=True)

info_scroll = ttk.Scrollbar(info_wrap, orient=VERTICAL,
                            command=info_canvas.yview,
                            style="Thin.Vertical.TScrollbar")
info_scroll.pack(side=RIGHT, fill=Y)
info_canvas.configure(yscrollcommand=info_scroll.set)

info_inner = Frame(info_canvas)
_info_win = info_canvas.create_window((0, 0), window=info_inner, anchor=NW)

info_canvas.bind("<Configure>",
                 lambda e: info_canvas.itemconfig(_info_win, width=e.width))
info_inner.bind("<Configure>",
                lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all")))
info_canvas.bind("<MouseWheel>",
                 lambda e: info_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

# ── Status Bar ────────────────────────────────────────────────────────────────

status_bar = Frame(root, height=30)
status_bar.pack(fill=X, side=BOTTOM)
status_bar.pack_propagate(False)

status_var = StringVar(value="  No image selected")
status_lbl = Label(status_bar, textvariable=status_var,
                   font=("Segoe UI", 9), anchor=W, padx=6)
status_lbl.pack(fill=BOTH, expand=True)

# ── Context Menu ──────────────────────────────────────────────────────────────

menu = Menu(root, tearoff=0, font=("Segoe UI", 10))
menu.add_command(label="Show Media Info",         command=show_media_info)
menu.add_command(label="Copy Image Information",  command=copy_info)
menu.add_command(label="Export Information",      command=export_info)
menu.add_command(label="Copy File Path",          command=copy_path)
menu.add_command(label="Analyze Image URL",       command=prompt_for_url)
menu.add_separator()
menu.add_checkbutton(label="Always on Top",
                     variable=stay_on_top, command=toggle_topmost)
menu.add_checkbutton(label="Dark Mode",
                     variable=dark_mode,   command=toggle_theme)

# ── Boot ──────────────────────────────────────────────────────────────────────

apply_theme()
root.mainloop()
