from PIL import Image
import random

def text_to_binary(text) -> str:
    binary_data = ''.join(format(ord(char), '08b') for char in text)
    return binary_data


def create_image_with_random_fill(binary_data, image_width, image_height):
    total_pixels = image_width * image_height

    while(len(binary_data) % 24 != 0):
        binary_data = binary_data + str(random.randint(0,1))

    pixels = [binary_data[i:i+24] for i in range(0, len(binary_data), 24)]

    image = Image.new("RGB", (image_width, image_height))

    pixel_index = 0

    for y in range(image_height):
        for x in range(image_width):
            if pixel_index < len(pixels) :
                r = int(pixels[pixel_index][:8], 2)
                g = int(pixels[pixel_index][8:16], 2)
                b = int(pixels[pixel_index][16:], 2)
                pixel_index += 1
            else:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
            image.putpixel((x, y), (r, g, b))

    return image


def main():
    with open('data.txt', 'r') as file:
        text = file.read().replace('\n', '')
    image_width = 1920
    image_height = 1080

    binary_data = text_to_binary(text)
    image = create_image_with_random_fill(binary_data, image_width, image_height)
    image.save("output_image.png")
    image.show()

if __name__ == "__main__":
    main()
    # TODO: figure out what to do in case there are more words than pixels available
    # TODO: figure out how to recover the text from the image