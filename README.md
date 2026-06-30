# 📁 Terminal File Explorer

A feature-rich **terminal-based File Explorer** built with **Python**, designed to simplify file and folder management through an intuitive command-line interface. The project focuses on efficient navigation, comprehensive file operations, and intelligent file organization while maintaining a clean, modular architecture.

---

## ✨ Features

### 📂 Navigation
    - Browse available drives
    - Navigate through directories
    - Return to parent folders
    - Automatic alphabetical sorting
    - Open supported file types
    - Skip protected/system folders

### 📄 File Operations
    - Create files (`.txt`, `.pdf`, `.docx`, `.xlsx`, `.pptx`)
    - Rename files
    - Copy files
    - Move files
    - Delete files

### 📁 Folder Operations
    - Create folders
    - Rename folders
    - Copy folders
    - Move folders
    - Delete folders

### 🧠 Intelligent File Organizer
Automatically organizes supported files into categorized folders.

**Supported Categories**
    - 🖼 Images
    - 🎥 Videos
    - 🎵 Audio
    - 📄 Documents
    - 📦 Archives

**Organizer Features**
    - Detects file categories automatically
    - Reuses existing category folders
    - Recognizes folder aliases (Photos, Movies, Docs, etc.)
    - Creates missing folders only when needed
    - Automatically moves files
    - Handles duplicate filenames safely
    - Skips unsupported files and protected folders
    - Displays progress updates and a detailed summary

---

## 🛡 Safety Features
    - Automatic duplicate filename handling
    - Invalid filename validation
    - Protected folder detection
    - Filesystem error handling
    - Safe file movement without overwriting existing files

---

## 🏗 Project Structure

    ```text
    File-Explorer/
    │
    ├── main.py          # Entry point
    ├── nav.py           # Navigation system
    ├── utils.py         # File & folder operations
    ├── organiser.py     # Intelligent file organizer
    ├── foldercheck.py   # Protected folder detection
    └── README.md
    ```

---

## 🛠 Technologies Used

    - Python 3
    - pathlib
    - shutil
    - os
    - reportlab
    - python-docx
    - openpyxl
    - python-pptx


---

## 🚀 Installation

### Option 1 — Download the Executable (Recommended)

    1. Go to the **Releases** page.
    2. Download the latest **Terminal File Explorer.exe**.
    3. Run the executable.

    > Windows SmartScreen may display a warning because the application is not digitally signed.
    >
    > Click **More info** → **Run anyway**.

    No installation or Python setup is required.

---

### Option 2 — Run from Source

    Clone the repository:

    ```bash
    git clone https://github.com/yourusername/File-Explorer.git
    cd File-Explorer
    ```

    Create a virtual environment:

    ```bash
    python -m venv .venv
    ```

    Activate it:

    **Windows**

    ```bash
    .venv\Scripts\activate
    ```

    Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    Run the application:

    ```bash
    python main.py
    ```

---

## 📜 License

This project is licensed under the **Apache License 2.0**.

You are free to use, modify, and distribute this project in accordance with the terms of the Apache 2.0 License. A copy of the license is available in the `LICENSE` file.

---

## Author

**Aishik Ghosh**

Built as a learning project to explore Python, filesystem operations, modular software design, and terminal application development.

If you found this project useful or interesting, consider giving it a ⭐ on GitHub!

---

## Icon Attribution

Application icon by <Atif Arshad> from [Flaticon](https://www.flaticon.com/free-icon/folder_13552458?term=file+explorer&page=1&position=3&origin=tag&related_id=13552458)

