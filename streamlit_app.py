import streamlit as st
from openai import OpenAI
from PIL import Image, UnidentifiedImageError
import io
import base64

st.title("🍴 Food Image Analyzer")

# Create an OpenAI client
client = OpenAI(api_key=st.secrets.get("OPENAI_KEY"))

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a file uploader for images
uploaded_image = st.file_uploader("Upload an image of food", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # Attempt to open the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to base64 format (this is one possible way to send the image in a prompt)
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Create a prompt for OpenAI based on the uploaded image
        prompt = f"Analyze the following image of food:\n\n{img_base64}"

        # Send the prompt to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze the ingredients of food in this image or state if ther is no detectable food:"},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img_base64}",
                        "detail": "high"
                    },
                    },
                ],
                }
            ],
            max_tokens=300,
        )

        # Display the response
        reply = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

    except UnidentifiedImageError:
        st.error("The uploaded file could not be identified as a valid image. Please try another image.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")




def comm():
    '''response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    "detail": "high"
                },
                },
            ],
            }
        ],
        max_tokens=300,
    )

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})'''