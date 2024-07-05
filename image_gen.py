import streamlit as st
from PIL import Image
import tinify
import os

# Set your Tinify API key from environment variable
TINIFY_API_KEY = os.getenv("TINIFY_API_KEY")
if not TINIFY_API_KEY:
    st.error("Tinify API key not found. Please set the TINIFY_API_KEY environment variable.")
else:
    tinify.key = TINIFY_API_KEY
    
st.title("🎈 Image Optimizer App")

st.write(
    "Upload your images to optimize them!"
)

uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            st.write(f"Processing {uploaded_file.name}")
            
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Original {uploaded_file.name}", use_column_width=True)
            
            # Save the image temporarily
            temp_path = f"temp_{uploaded_file.name}"
            image.save(temp_path)
            st.write(f"Saved {uploaded_file.name} temporarily at {temp_path}")
            
            # Optimize image using Tinify
            optimized_path_tinify = f"optimized_tinify_{uploaded_file.name}"
            source = tinify.from_file(temp_path)
            source.to_file(optimized_path_tinify)
            st.write(f"Optimized {uploaded_file.name} using Tinify and saved at {optimized_path_tinify}")
            
            # Display optimized image
            optimized_image_tinify = Image.open(optimized_path_tinify)
            st.image(optimized_image_tinify, caption=f"Optimized with Tinify {uploaded_file.name}", use_column_width=True)
            
            # Manually optimize image using Pillow (resize and quality adjustment)
            optimized_path_pillow = f"optimized_pillow_{uploaded_file.name}"
            image = Image.open(temp_path)
            image = image.resize((image.width // 2, image.height // 2), Image.ANTIALIAS)
            image.save(optimized_path_pillow, quality=85)
            st.write(f"Optimized {uploaded_file.name} using Pillow and saved at {optimized_path_pillow}")
            
            # Display optimized image
            optimized_image_pillow = Image.open(optimized_path_pillow)
            st.image(optimized_image_pillow, caption=f"Optimized with Pillow {uploaded_file.name}", use_column_width=True)
            
            # Remove temporary files
            os.remove(temp_path)
            os.remove(optimized_path_tinify)
            os.remove(optimized_path_pillow)
            st.write(f"Cleaned up temporary files for {uploaded_file.name}")
        
        except tinify.Error as e:
            st.write(f"An error occurred while processing {uploaded_file.name}: {e}")
            print(f"An error occurred while processing {uploaded_file.name}: {e}")
        
        except Exception as e:
            st.write(f"An error occurred while processing {uploaded_file.name}: {e}")
            print(f"An error occurred while processing {uploaded_file.name}: {e}")

st.write("Done processing all images.")
