from PIL import Image
from colorama import Fore, Style
import math
ASCII_CHARS = ' .:-=+*#%@'

def scale_image(image, new_width=100):
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width / 2)

    new_image = image.resize((new_width, new_height))
    return new_image

def color_distance(color1, color2):
    # Calculate Euclidean distance between two RGB colors
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

def closest_color(pixel_color):
    colorrama_colors = [(0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 255, 255, 255), 
    (255, 255, 0, 255), (0, 255, 255, 255), (255, 0, 255, 255), (255, 255, 255, 255)]
    pixel_rgb = pixel_color

    distances = [color_distance(pixel_rgb, color) for color in colorrama_colors]

    closest_index = distances.index(min(distances))
    closest_colorama_color = colorrama_colors[closest_index]
    colorrama_names = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]
    return colorrama_names[closest_index]

def map_pixels_to_ascii(image, new_width=100):
    pixels = image.getdata()

    ascii_str = Style.BRIGHT
    range_width = 25.5
    i = 0
    for pixel_value in pixels:
        intensity = (0.299 * pixel_value[0] 
            + 0.587 * pixel_value[1] + 0.114 * pixel_value[2])
        index = int(intensity//range_width)
        if index >= len(ASCII_CHARS):
            index = len(ASCII_CHARS) - 1
        ascii_str += closest_color(pixel_value)
        ascii_str += ASCII_CHARS[index]
        if i % new_width == 0:
            ascii_str += '\n'
        i += 1
    ascii_str += Fore.RESET
    return ascii_str

def convert_image_to_ascii(image_path, new_width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return

    image = scale_image(image, new_width=new_width)

    ascii_str = map_pixels_to_ascii(image, new_width=new_width)
    return ascii_str

print(convert_image_to_ascii('asuka.jpg'))