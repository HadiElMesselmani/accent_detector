# 📘 Accent Detector
---
## 🚀 Features

    🎥 Accepts YouTube or direct video URLs

    🎵 Extracts audio from video using yt-dlp

    ⏰ Trims audio to 60 seconds (due to API limitations)

    🔊 Transcribes speech using Google Web Speech API (no API key required)

    🌍 Detects spoken language using langdetect

    🎧 Identifies English accents using a fine-tuned SpeechBrain model from HuggingFace

    ✅ Designed to work on low-spec PCs

    ⭐ 100% offline after first model download, using only free tools

---
## Clone the repository
    git clone https://github.com/HadiElMesselmani/accent_detector.git
    cd accent_detector

---

## Create virtual environment 
    python -m venv venv
    .\venv\Scripts\activate (Windows)

---

## Install dependencies
    pip install -r requirements.txt

---

## ⚙️ Usage
    First-time Setup (important)

    ⚠️ The accent recognition model (Jzuluaga/accent-id-commonaccent_xlsr-en-english) requires admin rights on first run due to symbolic link creation in Windows. This is a Hugging Face backend issue.

    1. Open PowerShell as Administrator.

    2. Navigate to the project folder.

    3. Activate your virtual environment: .\venv\Scripts\activate

    4. Run the backend: python backend/app.py

    5. Open frontend/index.html in your browser (double-click or open with browser).

    After the model is downloaded once, you can use VS Code Terminal or any normal shell to run the backend again (admin is no longer needed).

---

## 🤖 How to Use

    1. Paste a valid YouTube or MP4 URL into the input box

    2. Click Analyze

    3. Wait for the backend to:

        a. Download and extract audio
        b. Trim to the first 60 seconds (Google Web Speech free tier has a 60s limit)
        c. Transcribe and detect language
        d. Run accent classification (if English)

    You will get a list of accents and their confidence scores

---

## 🛠️ Installation
    This code requires having ffmpeg installed.

    1. Go to the official build page https://www.gyan.dev/ffmpeg/builds/ and download “ffmpeg-release-full.7z” under Release builds › latest release (Version 7.1.1).

    2. Extract it, e.g. to C:\ffmpeg.

    3. Add C:\ffmpeg\bin to PATH:
        1. Press Win + X → System → Advanced system settings (or search “Edit the system environment variables”).
        2. Click Environment Variables….
        3. Under System variables select Path → Edit → New.
        4. Paste C:\ffmpeg\bin, click OK all the way out.

    4. Restart VS-Code and verify: 
        ffmpeg -version

---

## 📂 Project Structure

    Accent-Detector/
    ├── backend/
    │   ├── app.py                 # Flask API
    │   ├── helpers.py             # Audio, transcription, and accent detection logic
    │   └── temp_audio/           # Temporary audio files
    ├── frontend/
    │   └── index.html            # User interface for input and results
    ├── requirements.txt
    └── README.md

---

## 🧠 How It Works

    - Audio Extraction: yt-dlp pulls audio from the URL

    - Trimming: Only the first 60 seconds are kept due to Google’s free API limit

    - Transcription: Uses speech_recognition's recognize_google() (no key needed, but limited)

    - Language Detection: langdetect analyzes the returned transcript

    - Accent Classification: If English, SpeechBrain model classifies the accent (us, canada, england, etc.)

    - Model Note: Hugging Face model requires admin to write a symbolic link on first run

---

## 🧪 Example

    Test video:

    http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4
    
    ![image](https://github.com/user-attachments/assets/3fa1cd15-92ee-4b48-ac0f-a28699ade7e6)

---

## Output example 

---

## 👤 Author

    Hadi El Messelmani

    https://github.com/HadiElMesselmani

---
