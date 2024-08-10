import os
import zipfile
from tkinter import Tk, filedialog
from PIL import Image
import matplotlib.pyplot as plt

def extract_files(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {file_path} to {extract_to}")

def find_file(root_dir, target_dir, filename):
    for root, dirs, files in os.walk(root_dir):
        if target_dir in root:
            if filename in files:
                return os.path.join(root, filename)
    return None

def display_image_for_coordinates(image_path):
    image = Image.open(image_path)
    plt.imshow(image)
    coords = []

    def onclick(event):
        x, y = event.xdata, event.ydata
        coords.append((x, y))
        print(f"Clicked at: ({x}, {y})")
        if len(coords) == 2:
            plt.close()

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.imshow(image)
    plt.show()

    return coords

def process_images(extract_to):
    gui_path = find_file(extract_to, 'textures\\gui', 'gui.png')
    icons_path = find_file(extract_to, 'textures\\gui', 'icons.png')

    if not gui_path:
        print(f"Error: gui.png not found.")
        return
    if not icons_path:
        print(f"Error: icons.png not found.")
        return

    gui_image = Image.open(gui_path)
    icons_image = Image.open(icons_path)

    # Crop coordinates based on interactive clicks
    print("Click two points on the GUI image to get the top-left and bottom-right coordinates of the area to crop.")
    gui_coords = display_image_for_coordinates(gui_path)
    gui_cropped = gui_image.crop((*gui_coords[0], *gui_coords[1]))

    print("Click two points on the ICONS image to get the top-left and bottom-right coordinates of the first area to crop.")
    icons_coords_1 = display_image_for_coordinates(icons_path)
    icons_cropped_1 = icons_image.crop((*icons_coords_1[0], *icons_coords_1[1]))

    # Add more cropping as needed for other sections, using the same method.

    # Example for arranging the cropped sections
    processed_image = Image.new('RGBA', (150, 50))
    processed_image.paste(gui_cropped, (0, 0))
    processed_image.paste(icons_cropped_1, (60, 0))

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
