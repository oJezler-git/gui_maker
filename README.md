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

Run the automated setup using `run.bat`, or manually install the dependencies:


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
