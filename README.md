# Peekture 🔍

A lightweight, modern image inspection utility for Windows. Instantly view dimensions, aspect ratio, file size, color mode, and more — just drop an image in.

---

## Features

- **Drag & Drop** — drop any image directly onto the app
- **Clipboard Support** — paste images or URLs with `Ctrl+V`
- **URL Analysis** — load and inspect images directly from a web URL
- **Detailed Info Panel** — dimensions, aspect ratio, format, color mode, file size, and source path
- **Aspect Ratio Detection** — automatically identifies Widescreen, Square, Portrait, Ultrawide, and more
- **Dark Mode** — full light/dark theme toggle
- **Copy & Export** — copy image info to clipboard or export as a `.txt` file
- **Open in Photos** — launch the image in your default photo viewer
- **Always on Top** — pin the window above all others
- **Status Bar** — quick-glance filename and dimensions at the bottom

---

## Supported Formats

`JPG` `JPEG` `PNG` `BMP` `GIF` `WEBP`

---

## Installation

### Option 1 — Installer (Recommended)
Download the latest `PeektureSetup.exe` from the [Releases](../../releases) page and run it.

### Option 2 — Run from Source

**Requirements**
- Python 3.10+
- pip

**Install dependencies**
```bash
pip install pillow requests tkinterdnd2
```

**Run**
```bash
python main.py
```

---

## Building from Source

**1. Install PyInstaller**
```bash
pip install pyinstaller
```

**2. Compile**
```bash
pyinstaller --onefile --windowed --icon="Peaklogo Icon.ico" --add-data "Peaklogo_Icon.ico;." --add-data "Peaklogo Icon.ico;." main.py
```

**3. Build the installer**

Open `PeektureSetup.iss` in [Inno Setup](https://jrsoftware.org/isinfo.php) and hit `Ctrl+F9`.

---

## Usage

| Action | How |
|---|---|
| Open an image | Click **Select Image** or drag & drop onto the preview area |
| Paste from clipboard | `Ctrl+V` |
| Load from URL | Click **Analyze URL** or paste a URL with `Ctrl+V` |
| Copy image info | `⋮` menu → Copy Image Information |
| Export info to file | `⋮` menu → Export Information |
| Toggle dark mode | `⋮` menu → Dark Mode |
| Pin window on top | `⋮` menu → Always on Top |

---

## Screenshots

> Coming soon

---

## License

MIT License — see [LICENSE.txt](LICENSE.txt) for details.

---

## Author

**James Orhin Agyin**