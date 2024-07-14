
from PIL import Image

def encode_image(img_path, message, output_img_path):
    image = Image.open(img_path)
    encoded_image = image.copy()
    width, height = image.size
    index = 0
    message += chr(0)  # Add null character to indicate end of message

    for row in range(height):
        for col in range(width):
            pixel = list(image.getpixel((col, row)))

            for n in range(3):  # Iterate through R, G, B values
                if index < len(message) * 8:
                    char_index = index // 8
                    bit_index = index % 8
                    ascii_value = ord(message[char_index])
                    bit_value = (ascii_value >> (7 - bit_index)) & 1

                    pixel[n] = (pixel[n] & ~1) | bit_value
                    index += 1

            encoded_image.putpixel((col, row), tuple(pixel))

    encoded_image.save(output_img_path)
    print(f"Message encoded and saved to {output_img_path}")

def decode_image(img_path):
    image = Image.open(img_path)
    width, height = image.size
    message_bits = []
    
    for row in range(height):
        for col in range(width):
            pixel = image.getpixel((col, row))
            for n in range(3):  # Iterate through R, G, B values
                message_bits.append(pixel[n] & 1)
    
    message = ""
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i+8]
        char = chr(int(''.join(map(str, byte)), 2))
        if char == chr(0):  # Null character indicates end of message
            break
        message += char

    return message

# Usage
if __name__ == "__main__":
    # Encode a message into an image
    encode_image("input_image.png", "Hello, IBM!", "encoded_image.png")
    
    # Decode the message from the image
    decoded_message = decode_image("encoded_image.png")
    print("Decoded message:", decoded_message)
