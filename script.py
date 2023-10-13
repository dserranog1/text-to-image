from PIL import Image
from math import sqrt
import random


def text_to_binary(text) -> str:
    binary_data = "".join(format(ord(char), "08b") for char in text)
    return binary_data


def create_image_with_random_fill(binary_data, area_per_pixel):
    if area_per_pixel == 0:
        width_and_height_step = 1
    else:
        width_and_height_step = area_per_pixel
    while len(binary_data) % 24 != 0:
        binary_data = binary_data + str(random.randint(0, 1))

    pixels = [binary_data[i : i + 24] for i in range(0, len(binary_data), 24)]

    number_of_pixels = len(pixels)
    image_width = int(sqrt(number_of_pixels))
    image_height = image_width
    image = Image.new("RGB", (image_width, image_height))

    pixel_index = 0

    for y in range(0, image_height, width_and_height_step):
        for x in range(0, image_width, width_and_height_step):
            if pixel_index >= number_of_pixels:
                return image
            r = int(pixels[pixel_index][:8], 2)
            g = int(pixels[pixel_index][8:16], 2)
            b = int(pixels[pixel_index][16:], 2)
            pixel_index += 1
            image.putpixel((x, y), (r, g, b))
            for i in range(0, area_per_pixel):
                if x + i >= image_width:
                    continue
                for j in range(0, area_per_pixel):
                    if y + j >= image_height:
                        continue
                    image.putpixel((x + i, y + j), (r, g, b))
    return image


def text_to_image():
    with open("data.txt", "r") as file:
        text = file.read().replace("\n", "")

    binary_data = text_to_binary(text)
    image = create_image_with_random_fill(binary_data, 8)
    image.save("output_image.png")
    image.show()


def binary_to_text(binary_data):
    text = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i : i + 8]
        text += chr(int(byte, 2))
    return text


def image_to_text(image_path):
    image = Image.open(image_path)
    width, height = image.size
    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            binary_data += format(r, "08b")
            binary_data += format(g, "08b")
            binary_data += format(b, "08b")

    text = binary_to_text(binary_data)
    return text


def main():
    text_to_image()
    # print(image_to_text("output_image.png")[0:5000])


if __name__ == "__main__":
    main()
    # TODO: figure out what to do in case there are more words than pixels available
    # TODO: figure out how to recover the text from the image
