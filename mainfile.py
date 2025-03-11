from rembg import remove
from PIL import Image,ImageOps,ImageDraw
import os


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
is_Background_color = True
color = "White"
'''
if is_Background_color:
    # Convert transparent parts to white
    white_bg = Image.new("RGB", output.size, colors_rgb[color])  # Create a white background
    white_bg.paste(output, mask=output.split()[3])  # Use alpha channel as mask
    # Resize to passport size (600x600 pixels, adjust as needed)
    passport_size = (600, 600)  # Standard passport size in pixels
    resized = ImageOps.fit(white_bg, passport_size, method=Image.LANCZOS)

    # Save the final passport photo
    resized.save(output_path)
else:
    output.save(output_path)  # Save the result
'''
# Path to your folder containing images
for input_folder, output_folder in zip(["partyphotos","passportphotos"],["partyphotosout","passportphotosout"]):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    # Get all image files from the folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for i in image_files:
        # Load the input image
        input_path = input_folder+'/'+i
        output_path = (output_folder+'/'+i).replace(".jpg",".png")

        img = Image.open(input_path)
        output = remove(img)  # Remove background

        # Create a square canvas (resize to fit)
        size = max(output.size)  # Get the largest dimension
        square_img = Image.new("RGBA", (size, size), colors_rgb[color])  # Transparent background
        square_img.paste(output, ((size - output.width) // 2, (size - output.height) // 2), output)

        # Create a circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)  # Draw a circle

        # Apply the circular mask
        round_img = Image.new("RGBA", (size, size), colors_rgb[color])  # Transparent background
        round_img.paste(square_img, (0, 0), mask)

        # Show the processed image before saving
        round_img.show(title="Processed Image")

        # Save the final round image
        round_img.save(output_path)

        print("Round profile picture saved successfully!")
        