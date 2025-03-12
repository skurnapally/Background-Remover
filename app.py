import streamlit as st
from rembg import remove
from rembg.session_factory import new_session
from PIL import Image, ImageDraw
import face_recognition
import os
import base64

# Cache the U-Net model session
@st.cache_resource
def get_rembg_session():
    return new_session()

session = get_rembg_session()

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

# Function to set background image

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-attachment: scroll;
            }}
            h1 {{
                color: gold !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background
set_background("./static/background.jpg")

# Streamlit UI
st.title("🎨 AI-Powered Image Background Remover & Editor")

# Select input method
input_method = st.radio("Choose Input Method:", ["Upload Your Own Photo", "Generate Samples"])

# Select processing mode
mode = st.radio("Choose Processing Mode:", ["Without Face Detection", "With Face Detection"])

# Select sample type (if applicable)
if input_method == "Generate Samples":
    sample_type = st.radio("Choose Sample Type:", ["Passport Photos", "Party Photos"])

# Select background color
bg_color = st.selectbox("Choose Background Color:", list(colors_rgb.keys()))

def process_image(img):
    output = remove(img, session=session)
    size = max(output.size)
    square_img = Image.new("RGBA", (size, size), colors_rgb[bg_color])
    square_img.paste(output, ((size - output.width) // 2, (size - output.height) // 2), output)

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    round_img = Image.new("RGBA", (size, size), colors_rgb[bg_color])
    round_img.paste(square_img, (0, 0), mask)
    return round_img

if input_method == "Upload Your Own Photo":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        
        if mode == "With Face Detection":
            image = face_recognition.load_image_file(uploaded_file)
            face_locations = face_recognition.face_locations(image)
            if face_locations:
                top, right, bottom, left = face_locations[0]
                padding = 200
                height, width, _ = image.shape
                top, bottom = max(0, top - padding), min(height, bottom + padding)
                left, right = max(0, left - padding), min(width, right + padding)
                img = Image.fromarray(image[top:bottom, left:right])
        
        round_img = process_image(img)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Original Image", use_container_width=True)
        with col2:
            st.image(round_img, caption="Processed Image", use_container_width=True)

elif input_method == "Generate Samples":
    folder = "passportphotos" if sample_type == "Passport Photos" else "partyphotos"
    output_folder = folder + "out"
    os.makedirs(output_folder, exist_ok=True)
    
    image_files = [f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not image_files:
        st.warning(f"No images found in {folder}.")
    else:
        for image_file in image_files:
            input_path = os.path.join(folder, image_file)
            output_path = os.path.join(output_folder, image_file.replace(".jpg", ".png"))
            img = Image.open(input_path)
            round_img = process_image(img)
            round_img.save(output_path)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(img, caption=f"Original: {image_file}", use_container_width=True)
            with col2:
                st.image(round_img, caption=f"Processed: {image_file}", use_container_width=True)