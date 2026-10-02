from google import genai
from google.genai import types
import streamlit as st
from twilio.rest import Client
import json

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FROM = st.secrets["TWILIO_WHATSAPP_FROM"]
TWILIO_CONTENT_SID = st.secrets["TWILIO_CONTENT_SID"]


MODEL_NAME = "gemini-3.5-flash-lite"


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)

@st.cache_resource
def get_twilio_client():
    return Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)


gemini_client = get_gemini_client()
twilio_client = get_twilio_client()


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):
    message = {
        "role": role,
        "kind": kind,
        "content": content,
    }
    st.session_state.messages.append(message)
    render_message(message)


def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}"

def clean_whatsapp_text(text):
    if not text:
        return "No Translation summary available."

    text = " ".join(text.split())  # collapse whitespace/newlines
    return text[:1500] + "..." if len(text) > 1500 else text

    

def send_whatsapp(to_number, user_name, summary):
    try:
        content_variables = json.dumps(
            {"1": user_name, "2": clean_whatsapp_text(summary)}, ensure_ascii=False
        )

        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to_number}",
            content_sid=TWILIO_CONTENT_SID,
            content_variables=content_variables,
        )

        return True, message.sid
    except Exception as error:
        return False, f"Something went wrong:{error}"    



if "onboarded" not in st.session_state:

    st.title("SnapTranslate 🌍")
    st.caption("Snap it. Translate it. Read it your way.")

    with st.form("on_boarding_form"):

        name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
        )

        col1, col2 = st.columns([1, 4])

        with col1:
            st.text_input(
                "Code",
                value="+91",
                disabled=True,
            )

        with col2:
            whatsapp_number = st.text_input(
                "WhatsApp Number",
                placeholder="9876543210",
                max_chars=10,
                help="Enter your 10-digit WhatsApp number.",
            )

        submitted = st.form_submit_button("Let's Go")

    if submitted:

        if not name.strip():
            st.warning("⚠️ Please enter your name.")

        elif not whatsapp_number.strip():
            st.warning("⚠️ Please enter your WhatsApp number.")

        elif not whatsapp_number.isdigit():
            st.warning("⚠️ WhatsApp number should contain only digits.")

        elif len(whatsapp_number) != 10:
            st.warning("⚠️ Please enter a valid 10-digit WhatsApp number.")

        else:
            st.session_state.name = name.strip()
            st.session_state.whatsapp_number = "+91" + whatsapp_number.strip()

            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            st.session_state.messages = []
            st.session_state.pending_photo = None
            st.session_state.pending_text = ""
            st.session_state.onboarded = True

            st.rerun()

    st.stop()


header_col, button_col = st.columns(
    [5, 2],
    vertical_alignment="center",
)

with header_col:
    st.title("🌍 SnapTranslate")

with button_col:
    send_disabled = len(st.session_state.messages) <= 1
    if st.button("📤 Send to WhatsApp", disabled=send_disabled, use_container_width=True):
        with st.spinner("Sending to Your WhatsApp..."):
            summary = ask_gemini(SUMMARY_REQUEST_PROMPT)
            success,info = send_whatsapp(st.session_state.whatsapp_number, st.session_state.name, summary,)
        if success:
            st.success("Sent! Check your WhatsApp 📲")
        else:
            st.error(f"Couldn't send that: {info}")    


st.caption(
    f"Logged in as {st.session_state.name} "
    f"- updates go to {st.session_state.whatsapp_number}"
)


if "pending_photo" not in st.session_state:
    st.session_state.pending_photo = None

if "pending_text" not in st.session_state:
    st.session_state.pending_text = ""


if not st.session_state.messages:
    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        ),
    )
else:
    for message in st.session_state.messages:
        render_message(message)


user_input = st.chat_input(
    "Type text or attach an image to translate...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)


if user_input:

    photo = user_input.files[0] if user_input.files else None
    text = user_input.text

    if photo is not None:
        st.session_state.pending_photo = {
            "bytes": photo.getvalue(),
            "mime_type": photo.type,
        }

    if text:
        st.session_state.pending_text = text

    if photo is not None or text:
        st.rerun()


if st.session_state.pending_photo or st.session_state.pending_text:

    if st.session_state.pending_photo:
        st.image(
            st.session_state.pending_photo["bytes"],
            caption="Image ready to translate",
            width=400,
        )

    if st.session_state.pending_text:
        st.text_area(
            "Text ready to translate",
            value=st.session_state.pending_text,
            disabled=True,
        )

    st.subheader("🌍 Translation Settings")

    languages = [
        "English",
        "Telugu",
        "Hindi",
        "Tamil",
        "Kannada",
        "Malayalam",
        "Bengali",
        "Marathi",
        "Gujarati",
        "Punjabi",
        "Urdu",
        "Japanese",
        "Korean",
        "Chinese",
        "French",
        "German",
        "Spanish",
        "Arabic",
    ]

    translation_language = st.selectbox(
        "1️⃣ Which language should I translate it into?",
        languages,
    )

    display_language = st.selectbox(
        "2️⃣ Which language should I use to show the translation?",
        languages,
    )

    translate = st.button(
        "🌍 Translate",
        type="primary",
        use_container_width=True,
    )

    if translate:

        parts = []

        if st.session_state.pending_photo:

            photo_bytes = st.session_state.pending_photo["bytes"]
            mime_type = st.session_state.pending_photo["mime_type"]

            add_message(
                "user",
                "image",
                photo_bytes,
            )

            parts.append(
                types.Part.from_bytes(
                    data=photo_bytes,
                    mime_type=mime_type,
                )
            )

        if st.session_state.pending_text:

            add_message(
                "user",
                "text",
                st.session_state.pending_text,
            )

            parts.append(
                st.session_state.pending_text
            )

        instruction = (
            f"Translate the provided content into "
            f"{translation_language}.\n\n"
            f"Then show that translated result using "
            f"{display_language}.\n\n"
            f"The first selection is the actual translation language. "
            f"The second selection controls how the translated result "
            f"is displayed.\n\n"
            f"Do not translate the meaning into the display language "
            f"again. Preserve the meaning of the translation.\n\n"
            f"If an image is provided, read and translate its readable "
            f"text. If text is provided, translate that text. "
            f"If both are provided, process both.\n\n"
            f"Preserve names, numbers, dates, prices, measurements, "
            f"symbols, warnings, and important formatting where possible. "
            f"Do not invent unreadable text."
        )

        parts.append(instruction)

        with st.spinner("🌍 Translating..."):
            answer = ask_gemini(parts)

        add_message(
            "assistant",
            "text",
            answer,
        )

        st.session_state.pending_photo = None
        st.session_state.pending_text = ""

        st.rerun()