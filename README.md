# Image Summary and Safety Check App using LLaMA and Llama Guard Models

This is a Streamlit application that allows users to upload an image or provide an image URL, and then uses the LLaMA v1.5 7B model and Llama Guard 3 8B model to analyze the image content and check for safety. Here's a breakdown of the code:

**Functions**

1. `encode_image(image)`: Encodes an image to base64 format.
2. `analyze_image(image, prompt, is_url=False)`: Analyzes an image using the LLaMA v1.5 7B model. If the image is a URL, it downloads the image and encodes it to base64. Returns the analyzed text.
3. `check_content_safety(image_description)`: Analyzes an image description using the Llama Guard 3 8B model to check for safety. Returns a safety check result.
4. `process_image(image, url, prompt)`: Processes an image (either uploading or downloading) and analyzes it using the `analyze_image` function. Also checks the content safety using the `check_content_safety` function.
5. `launch()`: The main function that sets up the Streamlit app, defines the UI components, and runs the image analysis and safety check when the user clicks the "Analyze Image" button.

**UI Components**

1. `st.set_page_config()`: Sets the page title and layout to centered.
2. `st.markdown()`: Displays a markdown text with instructions on how to use the app.
3. `st.container()`: Creates a container for the UI components.
4. `st.columns()`: Defines two columns for the image uploader and URL text input.
5. `st.file_uploader()`: Allows users to upload an image file.
6. `st.text_input()`: Allows users to enter an image URL or a custom prompt for image analysis.
7. `st.button()`: Creates a "Analyze Image" button.
8. `st.text_area()`: Displays the analysis output and safety check result.

**Main Code**

The `launch()` function is the main entry point of the app. It sets up the UI components, defines the functions, and runs the image analysis and safety check when the user clicks the "Analyze Image" button.

**Note**: This code assumes that you have a `.env` file with a `GROQ_API_KEY` variable set. You'll need to replace this with your actual Groq API key. Additionally, this code uses the `requests` library to download images from URLs, so you may want to add error handling for cases where the image URL is invalid.