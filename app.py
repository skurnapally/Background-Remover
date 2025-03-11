import streamlit as st
from rembg import remove
from PIL import Image, ImageDraw
import face_recognition
import os

# Define available background colors
colors_rgb = {
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128),
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
}

# Streamlit UI
st.title("🖼 Background Remover & Circular Image Generator")

# Select processing mode
mode = st.radio("Choose Processing Mode:", ["Without Face Detection", "With Face Detection"])

# Select input folder
folder_choice = st.radio("Choose Image Folder:", ["partyphotos", "passportphotos"])
output_folder = folder_choice + "out"

# Select background color
bg_color = st.selectbox("Choose Background Color:", list(colors_rgb.keys()))

# Create output folder if it doesn’t exist
os.makedirs(output_folder, exist_ok=True)

# Get all images from the folder
image_files = [f for f in os.listdir(folder_choice) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

if not image_files:
    st.warning("No images found in the selected folder.")
else:
    for image_file in image_files:
        input_path = os.path.join(folder_choice, image_file)
        output_path = os.path.join(output_folder, image_file.replace(".jpg", ".png"))

        # Load and process the image
        img = Image.open(input_path)

        if mode == "Without Face Detection":
            output = remove(img)  # Remove background
        else:
            # Face detection logic
            image = face_recognition.load_image_file(input_path)
            face_locations = face_recognition.face_locations(image)

            if not face_locations:
                st.warning(f"No face detected in {image_file}. Skipping...")
                continue

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
            img = Image.fromarray(image[top:bottom, left:right])
            output = remove(img)

        # Create a square canvas
        size = max(output.size)
        square_img = Image.new("RGBA", (size, size), colors_rgb[bg_color])
        square_img.paste(output, ((size - output.width) // 2, (size - output.height) // 2), output)

        # Create circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        # Apply mask
        round_img = Image.new("RGBA", (size, size), colors_rgb[bg_color])
        round_img.paste(square_img, (0, 0), mask)

        # Save the processed image
        round_img.save(output_path)

        # Display images side by side
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Original Image", use_container_width=True)
        with col2:
            st.image(round_img, caption="Processed Image", use_container_width=True)

        #st.success(f"✅ Image processed and saved: {output_path}")
