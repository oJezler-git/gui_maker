import os
import zipfile
from tkinter import Tk, filedialog, simpledialog, messagebox, Toplevel, Label, Button, Checkbutton, IntVar, StringVar, Radiobutton
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageEnhance
import ttkbootstrap as ttk

def extract_files(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {file_path} to {extract_to}")

def detect_platform(extract_to):
    # check for manifest.json or pack.mcmeta directly in extract_to
    if os.path.exists(os.path.join(extract_to, 'manifest.json')):
        print("Bedrock Pack Detected")
        return 'bedrock'
    elif os.path.exists(os.path.join(extract_to, 'pack.mcmeta')):
        print("Java Pack Detected")
        return 'java'

    # if not found, check in the first-level subdirectory
    subdirectories = [d for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d))]
    
    if not subdirectories:
        print("Error: No subdirectories found in the extracted folder.")
        return None
    
    # assume the first subdirectory is the packs main directory
    pack_subdir = os.path.join(extract_to, subdirectories[0])

    if os.path.exists(os.path.join(pack_subdir, 'manifest.json')):
        print("Bedrock Pack Detected")
        return 'bedrock'
    elif os.path.exists(os.path.join(pack_subdir, 'pack.mcmeta')):
        print("Java Pack Detected")
        return 'java'
    
    print("Error: Could not determine Bedrock or Java texture pack.")
    return None


def find_file(root_dir, target_dir, filename):
    # first, search directly in the root directory
    target_dir = os.path.normpath(target_dir)
    for root, dirs, files in os.walk(root_dir):
        normalized_root = os.path.normpath(root)
        if target_dir in normalized_root:
            if filename in files:
                found_path = os.path.join(root, filename)
                print(f"Found {filename} at {found_path}")
                return found_path

    # if not found, search in the first-level subdirectory
    subdirectories = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    if not subdirectories:
        print(f"Error: No subdirectories found in {root_dir}")
        return None

    # the first subdirectory is the packs main directory
    pack_subdir = os.path.join(root_dir, subdirectories[0])

    for root, dirs, files in os.walk(pack_subdir):
        normalized_root = os.path.normpath(root)
        if target_dir in normalized_root:
            if filename in files:
                found_path = os.path.join(root, filename)
                print(f"Found {filename} at {found_path}")
                return found_path

    print(f"{filename} not found in {root_dir} or its subdirectories")
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

    # Crop specific sections from gui.png with descriptive names
    gui_crops = [
        ((0, 0, 40, 23), 'hotbar_start'),  # first 2 hotbar boxes
        ((160, 0, 183, 23), 'hotbar_end'), # end hotbar box
        ((1, 23, 23, 45), 'selector')     # selector
    ]
    cropped_gui_images = []
    for (left, upper, right, lower), name in gui_crops:
        cropped_image = crop_and_save(gui_image, 
                      (left * scale_factor_gui, upper * scale_factor_gui, right * scale_factor_gui, lower * scale_factor_gui),
                      os.path.join(extract_to, f'{name}.png'), upscale_factor)
        cropped_gui_images.append(cropped_image)

    # Crop specific sections from icons.png with descriptive names
    icons_crops = [
        ((52, 0, 61, 9), 'full_heart'),      # Full Heart
        ((61, 0, 67, 9), 'half_heart'),      # Half Heart
        ((16, 9, 25, 18), 'armor_background'), # Armour Background
        ((25, 9, 34, 18), 'half_armor'),     # Half Armour
        ((34, 9, 43, 18), 'full_armor'),     # Full Armour
        ((52, 9, 61, 18), 'heart_background'), # Heart Background
        ((52, 27, 62, 36), 'full_hunger'),   # Full Hunger
        ((62, 27, 70, 36), 'half_hunger'),   # Half Hunger
        ((16, 27, 25, 36), 'hunger_background'), # Hunger Background
        ((0, 64, 182, 69), 'xp_bar_background'), # XP bar background
        ((0, 69, 182, 74), 'xp_bar')         # XP bar
    ]
    cropped_icons_images = []
    for (left, upper, right, lower), name in icons_crops:
        cropped_image = crop_and_save(icons_image, 
                      (left * scale_factor_icons, upper * scale_factor_icons, right * scale_factor_icons, lower * scale_factor_icons),
                      os.path.join(extract_to, f'{name}.png'), upscale_factor)
        cropped_icons_images.append(cropped_image)

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
        cropped_gui_images.append(gui_image.crop(
            (left * scale_factor_gui, upper * scale_factor_gui, right * scale_factor_gui, lower * scale_factor_gui)))

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
        cropped_icons_images.append(icons_image.crop(
            (left * scale_factor_icons, upper * scale_factor_icons, right * scale_factor_icons, lower * scale_factor_icons)))

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

    new_size = (int(processed_image.width * upscale_factor), int(processed_image.height * upscale_factor))
    upscale_processed_image = processed_image.resize(new_size, Image.NEAREST)

    output_path = os.path.join(os.path.dirname(file_path), f'GUI-Maker-{pack_name}', 'processed_gui_exploded.png')
    upscale_processed_image.save(output_path)

    print(f"Exploded GUI saved to {output_path}")


def process_images_split_build(extract_to, upscale_factor, platform):
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
        cropped_gui_images.append(gui_image.crop(
            (left * scale_factor_gui, upper * scale_factor_gui, right * scale_factor_gui, lower * scale_factor_gui)))

    # Crop specific sections from icons.png
    icons_crops = [
        (52, 0, 61, 9),   # Full Heart
        (61, 0, 66, 9),   # Half Heart
        (16, 9, 25, 18),  # Armour Background
        (25, 9, 34, 18),  # Half Armour
        (34, 9, 43, 18),  # Full Armour
        (52, 9, 61, 18),  # Heart Background
        (52, 27, 62, 36), # Full Hunger
        (62, 27, 70, 36), # Half Hunger
        (16, 27, 25, 36), # Hunger Background
        (0, 64, 182, 69), # XP bar background
        (0, 69, 182, 74),  # XP bar
        (151, 64, 182, 69), # Half XP bar background
        (0, 69, 34, 74) # Half XP bar

    ]
    cropped_icons_images = []
    for left, upper, right, lower in icons_crops:
        cropped_icons_images.append(icons_image.crop(
            (left * scale_factor_icons, upper * scale_factor_icons, right * scale_factor_icons, lower * scale_factor_icons)))
        
    
    # Create a new image for the prebuild
    processed_image = Image.new('RGBA', (500, 150), (255, 255, 255, 0))

    # Pasting images with alpha compositing to preserve transparency
    def paste_with_alpha(base, overlay, position):
        temp_image = Image.new('RGBA', base.size, (255, 255, 255, 0))
        temp_image.paste(overlay, position)
        return Image.alpha_composite(base, temp_image)

    processed_image = paste_with_alpha(processed_image, cropped_gui_images[0], (50, 100))  # First 2 hotbar boxes
    processed_image = paste_with_alpha(processed_image, cropped_gui_images[1], (90, 100))  # End hotbar box
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[0], (50, 84))  # Full Heart
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[0], (60, 84))
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[5], (71, 84))  # Heart Background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[1], (60, 64))  # Half Heart
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[2], (70, 74))  # Armour Background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[3], (70, 64))  # Half Armour
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[4], (60, 74))  # Full Armour
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[4], (50, 74))
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[8], (85, 84))  # Hunger Background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[7], (86, 74))  # Half Hunger
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[6], (95, 84))  # Full Hunger
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[6], (105, 84))
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[9], (50, 94))  # XP bar background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[10], (50, 125))  # XP bar 

    processed_image = paste_with_alpha(processed_image, cropped_gui_images[2], (115, 100))  # Selector

    # Resize and save the image as before
    new_size = (int(processed_image.width * upscale_factor), int(processed_image.height * upscale_factor))
    upscale_processed_image = processed_image.resize(new_size, Image.NEAREST)

    output_path = os.path.join(os.path.dirname(file_path), f'GUI-Maker-{pack_name}', 'processed_gui_split_build.png')
    upscale_processed_image.save(output_path)

    print(f"Split build GUI saved to {output_path}")


def process_images_prebuild(extract_to, upscale_factor, platform, selector_position):
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

    gui_image = Image.open(gui_path).convert('RGBA')
    icons_image = Image.open(icons_path).convert('RGBA')

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
        cropped_gui_images.append(gui_image.crop(
            (left * scale_factor_gui, upper * scale_factor_gui, right * scale_factor_gui, lower * scale_factor_gui)))

    # Crop specific sections from icons.png
    icons_crops = [
        (52, 0, 61, 9),   # Full Heart
        (61, 0, 66, 9),   # Half Heart
        (16, 9, 25, 18),  # Armour Background
        (25, 9, 34, 18),  # Half Armour
        (34, 9, 43, 18),  # Full Armour
        (52, 9, 61, 18),  # Heart Background
        (52, 27, 62, 36), # Full Hunger
        (62, 27, 70, 36), # Half Hunger
        (16, 27, 25, 36), # Hunger Background
        (0, 64, 182, 69), # XP bar background
        (0, 69, 182, 74),  # XP bar
        (151, 64, 182, 69), # Half XP bar background
        (0, 69, 34, 74) # Half XP bar

    ]
    cropped_icons_images = []
    for left, upper, right, lower in icons_crops:
        cropped_icons_images.append(icons_image.crop(
            (left * scale_factor_icons, upper * scale_factor_icons, right * scale_factor_icons, lower * scale_factor_icons)))
        
    
    # Create a new image for the prebuild
    processed_image = Image.new('RGBA', (200, 150), (255, 255, 255, 0))

    # Pasting images with alpha compositing to preserve transparency
    def paste_with_alpha(base, overlay, position):
        temp_image = Image.new('RGBA', base.size, (255, 255, 255, 0))
        temp_image.paste(overlay, position)
        return Image.alpha_composite(base, temp_image)

    processed_image = paste_with_alpha(processed_image, cropped_gui_images[0], (50, 100))  # First 2 hotbar boxes
    processed_image = paste_with_alpha(processed_image, cropped_gui_images[1], (90, 100))  # End hotbar box
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[0], (50, 84))  # Full Heart
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[0], (60, 84))
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[5], (71, 84))  # Heart Background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[1], (70, 84))  # Half Heart
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[2], (70, 74))  # Armour Background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[3], (70, 74))  # Half Armour
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[4], (60, 74))  # Full Armour
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[4], (50, 74))
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[8], (85, 84))  # Hunger Background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[7], (86, 84))  # Half Hunger
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[6], (95, 84))  # Full Hunger
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[6], (105, 84))
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[11], (82, 94))  # XP bar background
    processed_image = paste_with_alpha(processed_image, cropped_icons_images[12], (50, 94))  # XP bar 

    if selector_position:
        print(f"Pasting selector image at position {selector_position}")
        processed_image = paste_with_alpha(processed_image, cropped_gui_images[2], selector_position) # the selector

    new_size = (int(processed_image.width * upscale_factor), int(processed_image.height * upscale_factor))
    upscale_processed_image = processed_image.resize(new_size, Image.NEAREST)

    output_path = os.path.join(os.path.dirname(file_path), f'GUI-Maker-{pack_name}', 'processed_gui_prebuild.png')
    upscale_processed_image.save(output_path)

    print(f"Prebuild GUI saved to {output_path}")

def add_essential_items(extract_to, upscale_factor, processed_dir, platform):
    essential_items_dir = os.path.join(processed_dir, 'essential_items')
    os.makedirs(essential_items_dir, exist_ok=True)

    if platform == 'bedrock':
        target_dir = os.path.join('textures', 'items')
    elif platform == 'java':
        target_dir = os.path.join('assets', 'minecraft', 'textures', 'item')
    else:
        print("Error: Unsupported platform.")
        return

    essential_items = [
        'bow_pulling_0.png', 
        'diamond_sword.png', 
        'diamond_pickaxe.png', 
        'iron_pickaxe.png', 
        'apple_golden.png', 
        'ender_pearl.png',
        'fireball.png',
        'fire_charge.png'
    ]
    
    for item in essential_items:
        item_path = find_file(extract_to, target_dir, item)
        if item_path:
            item_image = Image.open(item_path)
            crop_and_save(item_image, (0, 0, item_image.width, item_image.height), os.path.join(essential_items_dir, f'essential_{item}'), upscale_factor)
        else:
            print(f"Error: {item} not found.")


def apply_options(extract_to, file_path, pack_name, output_version, upscale_factor, delete_extracted, add_essential, options_window):
    processed_dir = os.path.join(os.path.dirname(file_path), f'GUI-Maker-{pack_name}')
    os.makedirs(processed_dir, exist_ok=True)

    platform = detect_platform(extract_to)

    if platform is None:
        print("Error: Unable to detect the platform (Bedrock or Java).")
        return

    def process_images_prebuild_with_slot(selector_position):
        process_images_prebuild(extract_to, upscale_factor.get(), platform, selector_position)
        
        # Add essential items if selected
        if add_essential.get():
            add_essential_items(extract_to, upscale_factor.get(), processed_dir, platform)

        # Cleanup if selected
        if delete_extracted.get():
            cleanup_extracted_files(extract_to, processed_dir)

    if output_version.get() == "exploded":
        process_images_exploded(extract_to, upscale_factor.get(), platform)
    elif output_version.get() == "split-build":
        process_images_split_build(extract_to, upscale_factor.get(), platform)
    elif output_version.get() == "prebuild":
        choose_selector_slot(process_images_prebuild_with_slot)
    else:
        process_images_separate(extract_to, upscale_factor.get(), platform)

        # Add essential items for non-prebuild options
        if add_essential.get():
            add_essential_items(extract_to, upscale_factor.get(), processed_dir, platform)

        # Cleanup for non-prebuild options
        if delete_extracted.get():
            cleanup_extracted_files(extract_to, processed_dir)

    options_window.destroy()

def cleanup_extracted_files(extract_to, processed_dir):
    import shutil
    processed_files = [f for f in os.listdir(extract_to) if os.path.isfile(os.path.join(extract_to, f))]
    for file in processed_files:
        shutil.move(os.path.join(extract_to, file), processed_dir)
        print(f"Moved {file} to {processed_dir}")
    shutil.rmtree(extract_to)
    print(f"Deleted {extract_to}")

def choose_selector_slot(process_images_prebuild_callback):
    selector_window = ttk.Toplevel()
    selector_window.title("Choose Selector Slot")
    selector_window.geometry('400x300')

    slot_choice = StringVar(value="1")

    ttk.Label(selector_window, text="Choose a slot for the selector (1, 2, 3) or 'none':").pack(pady=20)

    ttk.Radiobutton(selector_window, text="Slot 1", variable=slot_choice, value="1").pack(anchor='w', padx=20)
    ttk.Radiobutton(selector_window, text="Slot 2", variable=slot_choice, value="2").pack(anchor='w', padx=20)
    ttk.Radiobutton(selector_window, text="Slot 3", variable=slot_choice, value="3").pack(anchor='w', padx=20)
    ttk.Radiobutton(selector_window, text="None", variable=slot_choice, value="none").pack(anchor='w', padx=20)

    def confirm_slot_choice():
        chosen_slot = slot_choice.get()
        if chosen_slot == "none":
            selector_position = None
        elif chosen_slot == "1":
            selector_position = (50, 100)
        elif chosen_slot == "2":
            selector_position = (70, 100)
        elif chosen_slot == "3":
            selector_position = (90, 100)
        else:
            selector_position = None

        selector_window.destroy()
        process_images_prebuild_callback(selector_position)

    ttk.Button(selector_window, text="Confirm", command=confirm_slot_choice).pack(pady=20)

    selector_window.transient(Tk().mainloop())
    selector_window.grab_set()
    selector_window.wait_window(selector_window)

def main():
    global file_path, pack_name

    main_window = ttk.Window(themename="superhero")
    main_window.withdraw()

    while True:
        file_path = filedialog.askopenfilename(filetypes=[("Minecraft Packs", "*.zip *.mcpack")])

        if not file_path:
            print("No file selected")
            break

        pack_name = os.path.splitext(os.path.basename(file_path))[0]
        extract_to = os.path.join(os.path.dirname(file_path), f'{pack_name}_extracted')

        # check if extraction directory already exists
        if os.path.exists(extract_to):
            response = messagebox.askyesno(
                "Overwrite Existing Files",
                f"The directory '{extract_to}' already exists. Do you want to overwrite it?"
            )
            if not response:
                continue  # skip to the next iteration

        os.makedirs(extract_to, exist_ok=True)
        extract_files(file_path, extract_to)

        def show_options():
            # Create options window
            options_window = ttk.Toplevel()
            options_window.title("Options")
            options_window.geometry('600x500')

            # Variables
            output_version = StringVar(value="separate")
            upscale_factor = IntVar(value=8)
            delete_extracted = IntVar(value=1)
            add_essential = IntVar(value=0)

            # Widgets with modern styling and colors
            ttk.Label(options_window, text="Choose Output Version:").pack(anchor='w', pady=10, padx=10)
            ttk.Radiobutton(options_window, text="Exploded (Exploded Diagram, everything is exported to one PNG.)", variable=output_version, value="exploded", bootstyle="primary").pack(anchor='w', padx=20)
            ttk.Radiobutton(options_window, text="Separate (Separated, everything is exported into separate individual PNGs.)", variable=output_version, value="separate", bootstyle="primary").pack(anchor='w', padx=20)
            ttk.Radiobutton(options_window, text="Splitbuild (Made GUI but with icons seperated. EXPERIMENTAL LIMITED TO 16x PACKS)", variable=output_version, value="split-build", bootstyle="primary").pack(anchor='w', padx=20)
            ttk.Radiobutton(options_window, text="Prebuild (Fully made GUI. EXPERIMENTAL, NOT RECOMMENDED)", variable=output_version, value="prebuild", bootstyle="primary").pack(anchor='w', padx=20)

            ttk.Label(options_window, text="Upscale Factor:").pack(anchor='w', pady=10, padx=10)
            upscale_options = [1, 2, 4, 8]
            for option in upscale_options:
                ttk.Radiobutton(options_window, text=str(option), variable=upscale_factor, value=option).pack(anchor='w', padx=20)

            ttk.Checkbutton(options_window, text="Delete Extracted Pack (recommended)", variable=delete_extracted, bootstyle="success").pack(anchor='w', pady=10, padx=10)
            ttk.Checkbutton(options_window, text="Add Essential Items (Bow, Sword, Pickaxe, Gapple, Pearl)", variable=add_essential, bootstyle="success").pack(anchor='w', padx=10)

            def apply_options():
                processed_dir = os.path.join(os.path.dirname(file_path), f'GUI-Maker-{pack_name}')
                os.makedirs(processed_dir, exist_ok=True)

                platform = detect_platform(extract_to)

                if platform is None:
                    print("Error: Unable to detect the platform (Bedrock or Java).")
                    return

                def process_images_prebuild_with_slot(selector_position):
                    process_images_prebuild(extract_to, upscale_factor.get(), platform, selector_position)
                    if delete_extracted.get():
                        cleanup_extracted_files(extract_to, processed_dir)

                if output_version.get() == "exploded":
                    process_images_exploded(extract_to, upscale_factor.get(), platform)
                
                elif output_version.get() == "split-build":
                    process_images_split_build(extract_to, upscale_factor.get(), platform)

                elif output_version.get() == "prebuild":
                    choose_selector_slot(process_images_prebuild_with_slot)
                else:
                    process_images_separate(extract_to, upscale_factor.get(), platform)

                if add_essential.get():
                    add_essential_items(extract_to, upscale_factor.get(), processed_dir, platform)

                if output_version.get() != "prebuild" and delete_extracted.get():
                    cleanup_extracted_files(extract_to, processed_dir)

                options_window.destroy()

            ttk.Button(options_window, text="Apply", command=apply_options).pack(pady=20)

            options_window.transient(Tk().mainloop())
            options_window.grab_set()
            options_window.wait_window(options_window)

        show_options()

    main_window.destroy()

if __name__ == "__main__":
    main()