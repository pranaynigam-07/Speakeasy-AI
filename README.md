# SpeakEasy: Multi-Functional TTS and Blog-to-Audio App

SpeakEasy is a versatile, user-friendly application designed to empower mute individuals and assist anyone with text-to-speech (TTS), blog-to-audio, and translation functionalities. Built using Python and popular libraries like Tkinter, gTTS, and Google Translate API, SpeakEasy provides accessibility and convenience in communication.

---

## Features

### 1. **Text-to-Speech (TTS)**

- Converts typed or pasted text into speech.
- Adjustable speech rate and voice selection.
- Options to pause, resume, and clear speech.
- Save text as an audio file in `.mp3` format for offline playback.

### 2. **Blog-to-Audio Conversion**

- Fetch content from blogs or web articles using a URL.
- Extract and convert the blog content into speech.
- Load blog content into the text input field for editing or translation.

### 3. **Multilingual Translation**

- Translate text into multiple languages including:
  - English
  - French
  - Spanish
  - German
  - Italian
  - Portuguese
  - Russian (Romanized)
- Integration with Google Translate API ensures accurate translations.

### 4. **Customizable User Experience**

- Light and dark themes to suit different preferences.
- Adjustable speech rate slider for fine-tuning.
- Voice customization with support for multiple voices.

---

## How It Works

1. **Download and Install**

   - Ensure Python 3.8+ is installed on your system.
   - Install required libraries:
     ```bash
     pip install gtts googletrans==4.0.0-rc1 beautifulsoup4 requests pyttsx3
     ```

2. **Run the Application**

   - Save the code as `speakeasyAI.py`.
   - Run the file:
     ```bash
     python speakeasyAI.py
     ```

3. **Use the Features**
   - Input text directly or fetch content using a blog URL.
   - Customize speech rate and voice.
   - Translate and listen to the text in the chosen language.
   - Save audio files for future use.

---

## Motivation

SpeakEasy is specifically designed for mute individuals who cannot speak, providing them with a tool to express themselves audibly. It also supports anyone looking for TTS, blog-to-audio conversion, or translation capabilities, offering seamless communication and accessibility.

---

## System Requirements

- Python 3.8+
- Internet connection for:
  - Blog content fetching
  - Translation
  - Saving audio using `gTTS`

---

## Dependencies

- `tkinter`: For building the GUI.
- `pyttsx3`: Offline text-to-speech engine.
- `gTTS`: Text-to-speech using Google TTS API.
- `googletrans`: Language translation.
- `requests`: Fetching blog content.
- `beautifulsoup4`: Parsing HTML for blog content.

---

## Application Interface

- **Menu Bar**: Toggle between light and dark themes.
- **Blog-to-Audio Section**: Input blog URLs and fetch content.
- **Text Input Area**: Type, paste, or load content.
- **Translation Section**: Translate text to the selected language.
- **TTS Controls**:
  - Speak, pause, resume, and save audio.
  - Clear or reset the application.
- **Customization**:
  - Speech rate slider.
  - Voice selection dropdown.

---

## Contributing

Contributions are welcome! If you have suggestions or want to improve this project:

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request with a detailed explanation of your changes.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute this application as per the terms of the license.

---

## Acknowledgments

Special thanks to:

- Python community for libraries like `gTTS`, `pyttsx3`, and `googletrans`.
- Users who inspire us to build tools that enhance communication and accessibility.

---

## Disclaimer

SpeakEasy is an open-source project and may rely on third-party services (e.g., Google APIs). Ensure compliance with terms of these services when using the application.

---
