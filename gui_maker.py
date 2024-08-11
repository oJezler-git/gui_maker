import os
import zipfile
from tkinter import Tk, filedialog, simpledialog, messagebox, Toplevel, Label, Button, Checkbutton, IntVar, StringVar, Radiobutton
from PIL import Image, ImageEnhance

def extract_files(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {file_path} to {extract_to}")

def detect_platform(extract_to):
    # list the directories inside the extracted folder to identify bedrock or java
    subdirectories = [d for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d))]

    if not subdirectories:
        print("Error: No subdirectories found in the extracted folder.")
        return None

    # cause theres one subdirectory (the pack itself)
    pack_subdir = os.path.join(extract_to, subdirectories[0])

    # find manifest.json or pack.mcmeta
    if os.path.exists(os.path.join(pack_subdir, 'manifest.json')):
        print("Bedrock Pack Detected")
        return 'bedrock'
    elif os.path.exists(os.path.join(pack_subdir, 'pack.mcmeta')):
        print("Java Pack Detected")
        return 'java'
    
    print("Error: Could not determine Bedrock or Java texure pack.")
    return None


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

def upscale_image(image, upscale_factor):
    new_size = (int(image.width * upscale_factor), int(image.height * upscale_factor))
    upscaled_image = image.resize(new_size, Image.NEAREST)
    return upscaled_image

def crop_and_save(image, crop_box, save_path, upscale_factor=1):
    cropped_image = image.crop(crop_box)
    if upscale_factor > 1:
        cropped_image = upscale_image(cropped_image, upscale_factor)
    cropped_image.save(save_path)
    return cropped_image


def process_images_separate(extract_to, upscale_factor, platform):
    if platform == 'bedrock':
        gui_filename = 'gui.png'
        icons_filename = 'icons.png'
        gui_path = find_file(extract_to, os.path.join('textures', 'gui'), gui_filename)
        icons_path = find_file(extract_to, os.path.join('textures', 'gui'), icons_filename)
    elif platform == 'java':
        gui_filename = 'widgets.png'
        icons_filename = 'icons.png'
        gui_path = find_file(extract_to, os.path.join('assets', 'minecraft', 'textures', 'gui'), gui_filename)
        icons_path = find_file(extract_to, os.path.join('assets', 'minecraft', 'textures', 'gui'), icons_filename)
    else:
        print("Error: Could not determine platform type.")
        return

    if not gui_path:
        print(f"Error: {gui_filename} not found.")
        return
    if not icons_path:
        print(f"Error: {icons_filename} not found.")
        return

    gui_image = Image.open(gui_path)
    icons_image = Image.open(icons_path)

    # Calculate scaling factor based on the image size
    scale_factor_gui = gui_image.width / 256
    scale_factor_icons = icons_image.width / 256

    # Crop specific sections from gui.png
    gui_crops = [
        (0, 0, 40, 23),   # first 2 hotbar boxes
        (160, 0, 183, 23), # end hotbar box
        (1, 23, 23, 45)   # selector
    ]
    for i, (left, upper, right, lower) in enumerate(gui_crops):
        crop_and_save(gui_image, 
                      (left * scale_factor_gui, upper * scale_factor_gui, right * scale_factor_gui, lower * scale_factor_gui),
                      os.path.join(extract_to, f'gui_cropped_{i+1}.png'), upscale_factor)

    # Crop specific sections from icons.png
    icons_crops = [
        (52, 0, 61, 9),   # Full Heart
        (61, 0, 67, 9),   # Half Heart
        (16, 9, 25, 18),  # Armour Background
        (25, 9, 34, 18),  # Half Armour
        (34, 9, 43, 18),  # Full Armour
        (52, 9, 61, 18),  # Heart Background
        (52, 27, 62, 36), # Full Hunger
        (62, 27, 70, 36), # Half Hunger
        (16, 27, 25, 36), # Hunger Background
        (0, 64, 182, 69), # XP bar background
        (0, 69, 182, 74)  # XP bar
    ]
    for i, (left, upper, right, lower) in enumerate(icons_crops):
        crop_and_save(icons_image, 
                      (left * scale_factor_icons, upper * scale_factor_icons, right * scale_factor_icons, lower * scale_factor_icons),
                      os.path.join(extract_to, f'icons_cropped_{i+1}.png'), upscale_factor)

    print(f"Separate images saved to {extract_to}")

def process_images_exploded(extract_to, upscale_factor, platform):
    if platform == 'bedrock':
        gui_filename = 'gui.png'
        icons_filename = 'icons.png'
        gui_path = find_file(extract_to, os.path.join('textures', 'gui'), gui_filename)
        icons_path = find_file(extract_to, os.path.join('textures', 'gui'), icons_filename)
    elif platform == 'java':
        gui_filename = 'widgets.png'
        icons_filename = 'icons.png'
        gui_path = find_file(extract_to, os.path.join('assets', 'minecraft', 'textures', 'gui'), gui_filename)
        icons_path = find_file(extract_to, os.path.join('assets', 'minecraft', 'textures', 'gui'), icons_filename)
    else:
        print("Error: Could not determine platform type.")
        return

    if not gui_path:
        print(f"Error: {gui_filename} not found.")
        return
    if not icons_path:
        print(f"Error: {icons_filename} not found.")
        return

    gui_image = Image.open(gui_path)
    icons_image = Image.open(icons_path)

    # Calculate scaling factor based on the image size
    scale_factor_gui = gui_image.width / 256
    scale_factor_icons = icons_image.width / 256

    # Crop specific sections from gui.png
    gui_crops = [
        (0, 0, 40, 23),   # first 2 hotbar boxes
        (160, 0, 183, 23), # end hotbar box
        (1, 23, 23, 45)   # selector
    ]
    cropped_gui_images = []
    for left, upper, right, lower in gui_crops:
        cropped_gui_images.append(crop_and_save(gui_image,
            (left * scale_factor_gui, upper * scale_factor_gui, right * scale_factor_gui, lower * scale_factor_gui),
            os.path.join(extract_to, f'gui_cropped_exploded_{left}_{upper}_{right}_{lower}.png'), upscale_factor))

    # Crop specific sections from icons.png
    icons_crops = [
        (52, 0, 61, 9),   # Full Heart
        (61, 0, 67, 9),   # Half Heart
        (16, 9, 25, 18),  # Armour Background
        (25, 9, 34, 18),  # Half Armour
        (34, 9, 43, 18),  # Full Armour
        (52, 9, 61, 18),  # Heart Background
        (52, 27, 62, 36), # Full Hunger
        (62, 27, 70, 36), # Half Hunger
        (16, 27, 25, 36), # Hunger Background
        (0, 64, 182, 69), # XP bar background
        (0, 69, 182, 74)  # XP bar
    ]
    cropped_icons_images = []
    for left, upper, right, lower in icons_crops:
        cropped_icons_images.append(crop_and_save(icons_image,
            (left * scale_factor_icons, upper * scale_factor_icons, right * scale_factor_icons, lower * scale_factor_icons),
            os.path.join(extract_to, f'icons_cropped_exploded_{left}_{upper}_{right}_{lower}.png'), upscale_factor))

    # Calculate total width and height for the new image
    total_width = sum(img.width for img in cropped_gui_images + cropped_icons_images) + (len(cropped_gui_images) + len(cropped_icons_images) - 1) * 5
    total_height = max(img.height for img in cropped_gui_images + cropped_icons_images) * 2 + 15  # 10 extra for gap between XP bar and background

    # Create a new image to arrange the cutouts
    processed_image = Image.new('RGBA', (total_width, total_height))

    # Paste the cropped images with padding
    x_offset = 0
    for cropped_image in cropped_gui_images:
        processed_image.paste(cropped_image, (x_offset, 0))
        x_offset += cropped_image.width + 5

    x_offset = 0
    for cropped_image in cropped_icons_images[:-2]:  # Exclude the last two (XP bar background and XP bar)
        processed_image.paste(cropped_image, (x_offset, cropped_gui_images[0].height + 5))
        x_offset += cropped_image.width + 5

    # Paste the XP bar background and XP bar separately with a gap
    xp_bar_background = cropped_icons_images[-2]
    xp_bar = cropped_icons_images[-1]
    xp_bar_y_offset = cropped_gui_images[0].height + xp_bar_background.height + 10
    processed_image.paste(xp_bar_background, (x_offset, cropped_gui_images[0].height + 5))
    processed_image.paste(xp_bar, (x_offset, xp_bar_y_offset))

    output_path = os.path.join(extract_to, 'processed_gui_exploded.png')
    processed_image.save(output_path)
    print(f"Exploded GUI saved to {output_path}")

def add_essential_items(extract_to, upscale_factor, processed_dir):
    essential_items_dir = os.path.join(processed_dir, 'essential_items')
    os.makedirs(essential_items_dir, exist_ok=True)

    essential_items = [
        'bow_pulling_0.png', 
        'diamond_sword.png', 
        'diamond_pickaxe.png', 
        'iron_pickaxe.png', 
        'apple_golden.png', 
        'ender_pearl.png',
        'fireball.png' #thank larrzy lol skibidi sigma 
    ]
    for item in essential_items:
        item_path = find_file(extract_to, os.path.join('textures', 'items'), item)
        if item_path:
            item_image = Image.open(item_path)
            crop_and_save(item_image, (0, 0, item_image.width, item_image.height), os.path.join(essential_items_dir, f'essential_{item}'), upscale_factor)
        else:
            print(f"Error: {item} not found.")

def apply_options():
    # create a new directory for processed files
    processed_dir = os.path.join(os.path.dirname(file_path), f'GUI-Maker-{pack_name}')
    os.makedirs(processed_dir, exist_ok=True)

    platform = detect_platform(extract_to)

    if platform is None:
        print("Error: Unable to detect the platform (Bedrock or Java).")
        return

    if output_version.get() == "exploded":
        process_images_exploded(extract_to, upscale_factor.get(), platform)
    else:
        process_images_separate(extract_to, upscale_factor.get(), platform)

    if add_essential.get():
        add_essential_items(extract_to, upscale_factor.get(), processed_dir)

    if delete_extracted.get():
        import shutil
        # Move processed files to the new directory
        processed_files = [f for f in os.listdir(extract_to) if os.path.isfile(os.path.join(extract_to, f))]
        for file in processed_files:
            shutil.move(os.path.join(extract_to, file), processed_dir)
            print(f"Moved {file} to {processed_dir}")

        shutil.rmtree(extract_to)
        print(f"Deleted {extract_to}")

    options_window.destroy()

def main():
    global file_path, pack_name
    main_window = Tk()
    main_window.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Minecraft Packs", "*.zip *.mcpack")])

    if not file_path:
        print("No file selected")
        return

    pack_name = os.path.splitext(os.path.basename(file_path))[0]
    extract_to = os.path.join(os.path.dirname(file_path), f'{pack_name}_extracted')
    os.makedirs(extract_to, exist_ok=True)

    extract_files(file_path, extract_to)

    def show_options():

        options_window = Toplevel()
        options_window.title('tk')
        options_window.title("Options")

        # Variables
        output_version = StringVar(value="separate")
        upscale_factor = IntVar(value=1)
        delete_extracted = IntVar(value=0)
        add_essential = IntVar(value=0)

        tk_found = False

        for window in main_window.winfo_children():
            if window.winfo_class() == 'Toplevel':
                if window.title() == 'tk':
                    window.destroy()
                    tk_found = True

        if not tk_found:
            print("No 'tk' window found")

        Label(options_window, text="Choose Output Version:").pack(anchor='w')
        Radiobutton(options_window, text="Exploded", variable=output_version, value="exploded").pack(anchor='w')
        Radiobutton(options_window, text="Separate", variable=output_version, value="separate").pack(anchor='w')

        Label(options_window, text="Upscale Factor:").pack(anchor='w')
        upscale_options = [1, 2, 3, 4, 8]
        for option in upscale_options:
            Radiobutton(options_window, text=str(option), variable=upscale_factor, value=option).pack(anchor='w')

        Checkbutton(options_window, text="Delete Extracted Pack (recommended)", variable=delete_extracted).pack(anchor='w')
        Checkbutton(options_window, text="Add Essential Items (Bow, Sword, Pickaxe, Gapple, Pearl)", variable=add_essential).pack(anchor='w')

        def apply_options():
            # create a new directory for processed files
            processed_dir = os.path.join(os.path.dirname(file_path), f'GUI-Maker-{pack_name}')
            os.makedirs(processed_dir, exist_ok=True)

            platform = detect_platform(extract_to)

            if platform is None:
                print("Error: Unable to detect the platform (Bedrock or Java).")
                return

            if output_version.get() == "exploded":
                process_images_exploded(extract_to, upscale_factor.get(), platform)
            else:
                process_images_separate(extract_to, upscale_factor.get(), platform)

            if add_essential.get():
                add_essential_items(extract_to, upscale_factor.get(), processed_dir)

            if delete_extracted.get():
                import shutil
                # Move processed files to the new directory
                processed_files = [f for f in os.listdir(extract_to) if os.path.isfile(os.path.join(extract_to, f))]
                for file in processed_files:
                    shutil.move(os.path.join(extract_to, file), processed_dir)
                    print(f"Moved {file} to {processed_dir}")

                shutil.rmtree(extract_to)
                print(f"Deleted {extract_to}")

            options_window.destroy()


        Button(options_window, text="Apply", command=apply_options).pack()

        options_window.transient(Tk().mainloop())
        options_window.grab_set()
        options_window.wait_window(options_window)

    show_options()

if __name__ == "__main__":
    main()
