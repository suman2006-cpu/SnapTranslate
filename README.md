# 🌍 SnapTranslate

### AI-Powered Text & Image Translation Assistant

> **Snap it. Translate it. Read it your way.**

SnapTranslate is an AI-powered multilingual translation assistant built using **Python, Streamlit, Google Gemini, and Twilio WhatsApp API**.

It allows users to translate **text or text contained inside images** into their required language. Users can also choose how the translated result should be displayed — either in the **native script** or in **Romanized form**.

The project also includes **WhatsApp API integration using Twilio**, allowing users to send a generated translation summary directly to WhatsApp.

---

## ✨ Features

### 📝 Text Translation

Enter text directly into SnapTranslate and translate it into your required language.

### 📸 Image Translation

Upload a photo containing readable text and SnapTranslate uses Google Gemini to understand and translate the content.

Supported image formats:

- JPG
- JPEG
- PNG

### 🌍 Multi-Language Translation

SnapTranslate is not restricted to a single language pair.

Currently supported languages include:

- English
- Telugu
- Hindi
- Tamil
- Kannada
- Malayalam
- Bengali
- Marathi
- Gujarati
- Punjabi
- Urdu
- Japanese
- Korean
- Chinese
- French
- German
- Spanish
- Arabic

Examples:

```text
English → Telugu
Telugu → Hindi
Hindi → English
English → Hindi
```

---

## 🔤 Native Script & Romanized Translation

One of the key features of SnapTranslate is the ability to display the translated result in a format that is easier for the user to read.

The application provides two separate language selections.

### 1️⃣ Target Translation Language

This determines the language into which the original text or image content is translated.

### 2️⃣ Display Language

This determines how the translated result should be displayed.

The display language does **not** mean that the meaning is translated again.

### Example

**Input:**

```text
Where are you going?
```

**Target Translation Language:**

```text
Telugu
```

### Native Script Output

```text
మీరు ఎక్కడికి వెళ్తున్నారు?
```

### Romanized Output

```text
Meeru ekkadiki veltunnaru?
```

The Romanized result keeps the **Telugu meaning**, but writes it using English/Latin letters.

This is useful for people who understand a language but cannot comfortably read its native script.

### Hindi Example

**Target Language:** Hindi

**Display Language:** English

```text
Aap kahan ja rahe hain?
```

This is Romanized Hindi, not an English translation.

---

## 🤖 Google Gemini Integration

SnapTranslate uses **Google Gemini** as the AI engine for its translation workflow.

The application uses:

```text
gemini-3.5-flash-lite
```

Gemini is used to:

- Understand text input
- Understand uploaded images
- Read visible text from images
- Translate content
- Follow the selected target language
- Generate native-script translations
- Generate Romanized translations

The application also uses custom prompts to control the translation behavior and output format.

---

## 📱 WhatsApp API Integration

### A Major Feature of SnapTranslate

SnapTranslate integrates the **Twilio WhatsApp API** with the translation application.

After generating a translation, users can send a generated translation summary directly to their WhatsApp.

### WhatsApp Workflow

```text
User
  ↓
Text / Image
  ↓
SnapTranslate
  ↓
Google Gemini
  ↓
Translation Result
  ↓
Generate Summary
  ↓
Twilio WhatsApp API
  ↓
📱 WhatsApp
```

This integration demonstrates how an AI-powered web application can communicate with an external messaging platform using an API.

### WhatsApp Onboarding

During onboarding, the user provides:

- Name
- WhatsApp number

The application uses **+91** as the default country code.

The user enters their 10-digit WhatsApp number, which is validated before the application starts.

Example:

```text
User enters:
9876543210

Country Code:
+91

WhatsApp:
whatsapp:+919876543210
```

---

## 🧠 How SnapTranslate Works

```text
                 USER
                   │
          ┌────────┴────────┐
          │                 │
      TEXT INPUT        IMAGE INPUT
          │                 │
          └────────┬────────┘
                   ↓
            GOOGLE GEMINI
                   ↓
          TEXT UNDERSTANDING
                   ↓
          TARGET LANGUAGE
                   ↓
           DISPLAY LANGUAGE
                   ↓
        ┌──────────┴──────────┐
        │                     │
   Native Script          Romanized
        │                     │
        └──────────┬──────────┘
                   ↓
           TRANSLATED RESULT
                   │
                   ↓
          📤 SEND TO WHATSAPP
                   │
                   ↓
          TWILIO WHATSAPP API
```

---

## 🖥️ User Interface

The complete website interface is built using **Python Streamlit**.

The application provides a chat-based experience where users can:

1. Enter their name.
2. Enter their WhatsApp number.
3. Type text or upload an image.
4. Select the target translation language.
5. Select the display language.
6. Translate the content.
7. View the translated result.
8. Send the translation summary to WhatsApp.

The goal is to keep the translation process simple and interactive.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Main programming language |
| 🎨 Streamlit | Complete web application UI |
| 🤖 Google Gemini | AI translation and image understanding |
| 📱 Twilio | WhatsApp API integration |
| 🐙 GitHub | Source code and version control |

---

## 📂 Project Structure

```text
SnapTranslate/
│
├── app.py
├── prompts.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `app.py`

Contains the main Streamlit application, including:

- User onboarding
- Chat interface
- Text input
- Image upload
- Translation settings
- Gemini integration
- WhatsApp integration
- Session state management

### `prompts.py`

Contains the AI prompts used by the application, including:

- System translation instructions
- Welcome message template
- Translation summary prompt

### `requirements.txt`

Contains the Python packages required to run the application.

### `.gitignore`

Prevents sensitive and unnecessary files from being uploaded to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/suman2006-cpu/SnapTranslate.git
```

### 2. Open the project

```bash
cd SnapTranslate
```

### 3. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration

SnapTranslate uses API credentials for Google Gemini and Twilio.

These credentials should be stored securely using **Streamlit Secrets**.

Required secrets:

```text
GEMINI_API_KEY
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_WHATSAPP_FROM
TWILIO_CONTENT_SID
```

Example:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_FROM = "YOUR_TWILIO_WHATSAPP_NUMBER"
TWILIO_CONTENT_SID = "YOUR_TWILIO_CONTENT_SID"
```

> ⚠️ **Never upload real API keys, authentication tokens, or other private credentials to GitHub.**

---

## ▶️ Run Locally

After installing the dependencies and configuring the required secrets, run:

```bash
streamlit run app.py
```

The SnapTranslate web application will start through Streamlit.

---

## 🚀 Deployment

SnapTranslate is built as a Streamlit application and can be deployed using a Streamlit-compatible hosting platform.

Basic deployment workflow:

```text
GitHub Repository
       ↓
Connect Repository
       ↓
Select app.py
       ↓
Configure Secrets
       ↓
Deploy
       ↓
🌍 SnapTranslate Web App
```

Make sure all required API credentials are configured in the deployment platform's secrets.

---

## 🧪 Example

### Input

```text
How are you?
```

### Target Translation Language

```text
Telugu
```

### Display Language

```text
English
```

### Result

```text
Meeru ela unnaru?
```

If the display language is Telugu:

```text
మీరు ఎలా ఉన్నారు?
```

---


## 🎯 Project Goal

The goal of SnapTranslate was to build a practical AI application by combining multiple technologies into one useful platform.

```text
Python
   +
Streamlit
   +
Google Gemini
   +
Image Understanding
   +
Multi-Language Translation
   +
Romanized Output
   +
WhatsApp API
   =
🌍 SnapTranslate
```

---

## 🔮 Future Improvements

Possible future improvements include:

- 🎙️ Voice input
- 🔊 Text-to-speech
- 📄 PDF and document translation
- 🗂️ Translation history
- 📱 Dedicated mobile application
- 🧠 Better handling of difficult or low-quality images
- 🌐 Additional language support
- 💬 More messaging-platform integrations
- ⚡ Faster processing
- 👤 User accounts and saved preferences

---

## ⚠️ Current Limitations

- Image translation depends on the readability of the uploaded image.
- The currently available languages are defined in the application.
- WhatsApp messaging requires a valid Twilio configuration.
- Translation requests depend on Gemini API availability and limits.
- The application currently accepts JPG, JPEG, and PNG images.
- 📱 **WhatsApp:** In the current free/trial setup, WhatsApp messages can only be sent to a **verified/approved recipient number** associated with the Twilio WhatsApp account. Sending messages to any user is not available until a production WhatsApp setup is configured.

---

## 👨‍💻 Developer

### Suman

SnapTranslate was built as a practical project to explore:

**Generative AI • Python • Streamlit • Multimodal AI • Translation • Prompt Engineering • WhatsApp API • Twilio • GitHub**

---

## ⭐ Support

If you find SnapTranslate interesting, consider giving the repository a ⭐ on GitHub.

---

# 🌍 SnapTranslate

### **Snap it. Translate it. Read it your way.**
