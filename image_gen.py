import streamlit as st
from PIL import Image
import tinify
import os
from optimize_images import optimize_image

# Set your Tinify API key
TINIFY_API_KEY = "YOUR_TINIFY_API_KEY"
tinify.key = TINIFY_API_KEY

st.title("🎈 Image Optimizer App")

st.write(
    "Upload your images to optimize them!"
)

uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        
        st.image(image, caption=f"Original {uploaded_file.name}", use_column_width=True)
        
        # Save the image temporarily
        temp_path = f"temp_{uploaded_file.name}"
        image.save(temp_path)
        
        # Optimize image using Tinify
        optimized_path_tinify = f"optimized_tinify_{uploaded_file.name}"
        source = tinify.from_file(temp_path)
        source.to_file(optimized_path_tinify)
        
        # Display optimized image
        optimized_image_tinify = Image.open(optimized_path_tinify)
        st.image(optimized_image_tinify, caption=f"Optimized with Tinify {uploaded_file.name}", use_column_width=True)
        
        # Optimize image using optimize-images
        optimized_path_optimize_images = f"optimized_optimize_images_{uploaded_file.name}"
        optimize_image(temp_path, optimized_path_optimize_images, lossy=True, max_width=1024)
        
        # Display optimized image
        optimized_image_optimize_images = Image.open(optimized_path_optimize_images)
        st.image(optimized_image_optimize_images, caption=f"Optimized with optimize-images {uploaded_file.name}", use_column_width=True)
        
        # Remove temporary files
        os.remove(temp_path)
        os.remove(optimized_path_tinify)
        os.remove(optimized_path_optimize_images)
