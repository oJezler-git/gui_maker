# Minecraft Texture Pack GUI Maker

This script extracts, processes, and modifies Minecraft texture packs to create GUI elements to help aid with thumbnail making process. It supports both Bedrock and Java edition texture packs.

## Features

- Automatically detects platform type (Java or Bedrock).
- Extracts specific images for GUI elements.
- Allows separate or exploded output versions.
- Optionally adds essential items like swords and pickaxes.
- Upscales images based on user input.
- Deletes extracted files after processing if desired.

## Requirements

- Python 3.x
- Pillow library for image processing
- Tkinter for GUI dialogs

## Installation

# FULLY AUTOMATED INSTALLATION:

![tutorial](https://github.com/user-attachments/assets/07a7aa23-1fb8-4fcc-952a-f591b2a1c3e1)

- Download the ZIP file
- Extract the contents
- Run the automated setup using `run.bat`, or manually install the dependencies:


# MANUAL INSTALLATION AND RUN:
Install Python

Install Pillow using pip:
```bash
pip install pillow
```
Open cmd and run the python file
```bash
python3 gui_maker.py
```

## Usage

1. Run the script.
2. Select a Minecraft texture pack file (`.zip` or `.mcpack`) when prompted.
3. Choose your options in the dialog:
   - **Output Version**: Choose between "Exploded" or "Separate".
   - **Upscale Factor**: Select a factor (1, 2, 3, 4, 8) to upscale images.
   - **Delete Extracted Pack**: Optionally delete the extracted files after processing.
   - **Add Essential Items**: Include additional essential items like bow, sword, etc.

4. The processed files will be saved in a new directory named `GUI-Maker-<PackName>`.

## Notes

- Exploded means like an exploded diagram, all assets are spread on 1 png.
- Separate means they are cut out into separate pngs.
- Ensure all dependencies are installed before running.
- The script requires user interaction via GUI dialogs.
- Credits to Dailzay for the idea.

## License

This project is licensed under the MIT License.
```
Copyright 2024 Jezler

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
