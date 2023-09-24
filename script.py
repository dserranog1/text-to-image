from PIL import Image
import random


def text_to_binary(text) -> str:
    binary_data = "".join(format(ord(char), "08b") for char in text)
    return binary_data


def create_image_with_random_fill(binary_data, image_width, image_height):
    while len(binary_data) % 24 != 0:
        binary_data = binary_data + str(random.randint(0, 1))

    pixels = [binary_data[i : i + 24] for i in range(0, len(binary_data), 24)]

    image = Image.new("RGB", (image_width, image_height))

    pixel_index = 0

    for y in range(image_height):
        for x in range(image_width):
            if pixel_index < len(pixels):
                r = int(pixels[pixel_index][:8], 2)
                g = int(pixels[pixel_index][8:16], 2)
                b = int(pixels[pixel_index][16:], 2)
                pixel_index += 1
            else:
                r = random.randint(254, 255)
                g = random.randint(254, 255)
                b = random.randint(254, 255)
            image.putpixel((x, y), (r, g, b))

    return image


def text_to_image(width=700, height=500):
    with open("data.txt", "r") as file:
        text = file.read().replace("\n", "")
    width = 700
    height = 500

    binary_data = text_to_binary(text)
    image = create_image_with_random_fill(binary_data, width, height)
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
