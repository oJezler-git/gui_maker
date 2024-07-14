import os
import zipfile
from tkinter import Tk, filedialog
from PIL import Image

def extract_files(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {file_path} to {extract_to}")

def find_file(root_dir, target_dir, filename):
    target_dir = os.path.normpath(target_dir)
    for root, dirs, files in os.walk(root_dir):
        normalized_root = os.path.normpath(root)
        if target_dir in normalized_root:
            if filename in files:
                found_path = os.path.join(root, filename)
                print(f"Found {filename} at {found_path}")
                return found_path
    print(f"{filename} not found in {root_dir}")
    return None

def process_images(extract_to):
    gui_path = find_file(extract_to, os.path.join('textures', 'gui'), 'gui.png')
    icons_path = find_file(extract_to, os.path.join('textures', 'gui'), 'icons.png')

    print(f"Looking for gui.png at: {gui_path}")
    print(f"Looking for icons.png at: {icons_path}")

    if not gui_path:
        print(f"Error: gui.png not found.")
        return
    if not icons_path:
        print(f"Error: icons.png not found.")
        return

    gui_image = Image.open(gui_path)
    icons_image = Image.open(icons_path)

    # Crop specific sections from gui.png
    gui_cropped_1 = gui_image.crop((0, 0, 40, 23)) # first 2 hotbar boxes
    gui_cropped_2 = gui_image.crop((160, 0, 183, 23)) # end hotbar box
    gui_cropped_3 = gui_image.crop((1, 23, 23, 45)) # selector

    # Crop specific sections from icons.png
    icons_cropped_1 = icons_image.crop((52, 0, 61, 9))   # Full Heart
    icons_cropped_2 = icons_image.crop((61, 0, 67, 9))   # Half Heart
    icons_cropped_3 = icons_image.crop((16, 9, 25, 18))  # Armour Background
    icons_cropped_4 = icons_image.crop((25, 9, 34, 18))  # Half Armour
    icons_cropped_5 = icons_image.crop((34, 9, 43, 18))  # Full Armour
    icons_cropped_6 = icons_image.crop((52, 9, 61, 18))  # Heart Background
    # icons_cropped_7 = icons_image.crop((16, 36, 25, 45)) # Hunger
    icons_cropped_8 = icons_image.crop((52, 27, 62, 36)) # Full Hunger
    icons_cropped_9 = icons_image.crop((62, 27, 70, 36)) # Half Hunger
    icons_cropped_10 = icons_image.crop((16, 27, 25, 36)) # Hunger Background
    icons_cropped_11 = icons_image.crop((0, 64, 182, 69)) # XP bar background
    icons_cropped_12 = icons_image.crop((0, 69, 182, 74)) # XP bar

    # Create a new image to arrange the cutouts
    processed_image = Image.new('RGBA', (200, 50))  # Adjust the size as needed

    # Paste the cropped images
    processed_image.paste(gui_cropped_1, (0, 0))
    processed_image.paste(gui_cropped_2, (40, 0))
    processed_image.paste(gui_cropped_3, (65, 0))
    processed_image.paste(icons_cropped_1, (95, 0))
    processed_image.paste(icons_cropped_2, (109, 0))
    processed_image.paste(icons_cropped_3, (118, 0))
    processed_image.paste(icons_cropped_4, (127, 0))
    processed_image.paste(icons_cropped_5, (136, 0))
    processed_image.paste(icons_cropped_6, (145, 0))
    # processed_image.paste(icons_cropped_7, (0, 0))
    processed_image.paste(icons_cropped_8, (154, 0))
    processed_image.paste(icons_cropped_9, (164, 0))
    processed_image.paste(icons_cropped_10, (174, 0))
    processed_image.paste(icons_cropped_11, (0, 25))
    processed_image.paste(icons_cropped_12, (0, 35))


    output_path = os.path.join(extract_to, 'processed_gui.png')
    processed_image.save(output_path)
    print(f"Processed GUI saved to {output_path}")

def main():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Minecraft Packs", "*.zip *.mcpack")])

    if not file_path:
        print("No file selected")
        return

    extract_to = os.path.join(os.path.dirname(file_path), 'temp_extracted')
    os.makedirs(extract_to, exist_ok=True)

    extract_files(file_path, extract_to)

    for root, dirs, files in os.walk(extract_to):
        for name in files:
            print(os.path.join(root, name))

    process_images(extract_to)

if __name__ == "__main__":
    main()
