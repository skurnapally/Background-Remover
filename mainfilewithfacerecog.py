import cv2
import numpy as np
from rembg import remove
from PIL import Image, ImageDraw
import face_recognition
import os

# Load the image
colors_rgb = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128),
    "Silver": (192, 192, 192),
    "Red": (255, 0, 0),
    "Dark Red": (139, 0, 0),
    "Firebrick": (178, 34, 34),
    "Crimson": (220, 20, 60),
    "Tomato": (255, 99, 71),
    "Indian Red": (205, 92, 92),
    "Green": (0, 255, 0),
    "Dark Green": (0, 100, 0),
    "Forest Green": (34, 139, 34),
    "Lime": (0, 255, 0),
    "Olive": (128, 128, 0),
    "Sea Green": (46, 139, 87),
    "Blue": (0, 0, 255),
    "Navy": (0, 0, 128),
    "Royal Blue": (65, 105, 225),
    "Sky Blue": (135, 206, 235),
    "Dodger Blue": (30, 144, 255),
    "Teal": (0, 128, 128),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Yellow": (255, 255, 0),
    "Gold": (255, 215, 0),
    "Dark Orange": (255, 140, 0),
    "Orange": (255, 165, 0),
    "Light Yellow": (255, 255, 224),
    "Purple": (128, 0, 128),
    "Violet": (238, 130, 238),
    "Orchid": (218, 112, 214),
    "Hot Pink": (255, 105, 180)
}

for input_folder, output_folder in zip(["partyphotos","passportphotos"],["partyphotosout","passportphotosout"]):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    # Get all image files from the folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for i in image_files:
        # Load the input image
        input_path = input_folder+'/'+i
        output_path = (output_folder+'/'+i).replace(".jpg",".png")
        # Load image with face_recognition
        image = face_recognition.load_image_file(input_path)
        face_locations = face_recognition.face_locations(image)

        if not face_locations:
            print("No face detected!")
        else:
            # Get the first detected face (top, right, bottom, left)
            top, right, bottom, left = face_locations[0]

            # Add some padding around the face
            padding = 200  # Adjust this as needed
            height, width, _ = image.shape

            top = max(0, top - padding)
            bottom = min(height, bottom + padding)
            left = max(0, left - padding)
            right = min(width, right + padding)

            # Crop the image around the face
            cropped_image = Image.fromarray(image[top:bottom, left:right])

            # Remove background
            output = remove(cropped_image)

            # Create a square canvas based on the cropped face size
            size = max(output.size)  # Get max dimension to make it square
            square_img = Image.new("RGBA", (size, size), colors_rgb['White'])  # Transparent background
            square_img.paste(output, ((size - output.width) // 2, (size - output.height) // 2), output)

            # Create a circular mask
            mask = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)  # Create a circular mask

            # Apply the circular mask
            round_img = Image.new("RGBA", (size, size), (255, 255, 255, 0))  # Transparent background
            round_img.paste(square_img, (0, 0), mask)

            # Show the processed image before saving
            round_img.show(title="Processed Image")

            # Save the final round image
            round_img.save(output_path)

            print("Round profile picture saved successfully!")
