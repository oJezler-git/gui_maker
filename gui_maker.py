import os
import zipfile
from tkinter import Tk, filedialog
from PIL import Image

def extract_files(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def process_images(extract_to):
    gui_path = os.path.join(extract_to, 'textures', 'gui', 'gui.png')
    icons_path = os.path.join(extract_to, 'textures', 'gui', 'icons.png')

    # Open images
    gui_image = Image.open(gui_path)
    icons_image = Image.open(icons_path)

    # Cut out
    gui_cropped = gui_image.crop((0, 0, 100, 100))  # Temporary cut
    icons_cropped = icons_image.crop((0, 0, 50, 50))  # Temporary cut

    # Create a new image to arrange the cutouts
    processed_image = Image.new('RGBA', (150, 100))  # Temporary Paste
    processed_image.paste(gui_cropped, (0, 0))
    processed_image.paste(icons_cropped, (100, 0))

    # Save the processed image
    processed_image.save(os.path.join(extract_to, 'processed_gui.png'))

def main():
    # Create Tkinter file dialog
    Tk().withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Minecraft Packs", "*.zip *.mcpack")])

    if not file_path:
        print("No file selected")
        return

    # Create a temporary directory for extraction
    extract_to = os.path.join(os.path.dirname(file_path), 'temp_extracted')
    os.makedirs(extract_to, exist_ok=True)

    # Extract the files
    extract_files(file_path, extract_to)

    # Process the images
    process_images(extract_to)

    print(f"Processed GUI saved to {os.path.join(extract_to, 'processed_gui.png')}")

if __name__ == "__main__":
    main()
