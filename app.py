import base64
import io
import streamlit as st
from groq import Groq
from PIL import Image
import requests

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def analyze_image(image, prompt, is_url=False):
    client = Groq(api_key=st.secrets['GROQ_API_KEY'])

    if is_url:
        image_content = {"type": "image_url", "image_url": {"url": image}}
    else:
        base64_image = encode_image(image)
        image_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        image_content,
                    ],
                }
            ],
            model="llava-v1.5-7b-4096-preview",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def check_content_safety(image_description):
    client = Groq(api_key=st.secrets['GROQ_API_KEY'])

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a content safety classifier. Analyze the given text and determine if it contains any unsafe or inappropriate content."},
                {"role": "user", "content": f"Please analyze this image description for any unsafe or inappropriate content: {image_description}"}
            ],
            model="llama-guard-3-8b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def process_image(image, url, prompt):
    if image is not None:
        return analyze_image(image, prompt), check_content_safety(analyze_image(image, prompt))
    elif url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))
            return analyze_image(image, prompt, is_url=True), check_content_safety(analyze_image(image, prompt, is_url=True))
        except:
            return "Invalid image URL. Please provide a direct link to an image.", ""
    else:
        return "Please provide an image to analyze.", ""

def launch():
    st.set_page_config(page_title="Image Summariser and Safety Checker", layout="centered")
    st.markdown("<h1 style='text-align: center;'>Image Summariser and Safety Checker</h1>", unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        **How to use this app:**
        1. Upload an image file or paste an image URL.
        2. Use default prompt or enter a custom prompt for image analysis.
        3. Click "Analyze Image" to check for content safety.
        """)

    prompt = st.text_input("Image Analysis Prompt:", value="Describe the image content.")

    col1, col2 = st.columns(2)
    image = None
    with col1:
        image_file = st.file_uploader("Upload Image:", type=["jpg", "png", "jpeg"])
        if image_file:
            image = Image.open(image_file)
            st.image(image, caption="Uploaded Image Preview", use_column_width=True)

    with col2:
        url = st.text_input("Or Paste Image URL:")

    if st.button("Analyze Image"):
        if image or url:
            analysis_output, safety_output = process_image(image, url, prompt)
            st.text_area("Image Analysis with LlaVA 1.5 7B:", analysis_output, height=150)
            st.text_area("Safety Check with Llama Guard 3 8B:", safety_output, height=150)
        else:
            st.warning("Please upload an image or provide a valid URL before analyzing.")

if __name__ == "__main__":
    launch()
