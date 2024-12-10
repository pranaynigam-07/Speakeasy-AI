import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from gtts import gTTS
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
import pyttsx3
import threading
import queue


class SpeakEasyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SpeakEasy: Multi-Functional TTS and Blog-to-Audio App")
        self.root.geometry("800x600")

        # Initialize pyttsx3 TTS Engine
        self.engine = pyttsx3.init()
        self.configure_tts_engine()

        # Initialize Translator
        self.translator = Translator()

        # UI State Variables
        self.languages = {
            "English": "en",
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Hindi": "hi",
            "Japanese (Romanized)": "ja",
            "Italian": "it",
            "Portuguese": "pt",
            "Russian (Romanized)": "ru"
        }
        self.current_theme = tk.StringVar(value="Light")
        self.text_to_speak = ""
        self.is_speaking = False
        self.speech_queue = queue.Queue()
        self.speech_thread = None
        self.pause_event = threading.Event()

        # Build GUI
        self.setup_gui()

    def configure_tts_engine(self):
        """Configure pyttsx3 TTS engine."""
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 1.0)

    def setup_gui(self):
        """Setup the user interface."""
        # Menu Bar for Themes
        menubar = tk.Menu(self.root)
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_radiobutton(label="Light Theme", variable=self.current_theme, command=self.apply_theme)
        theme_menu.add_radiobutton(label="Dark Theme", variable=self.current_theme, command=self.apply_theme)
        menubar.add_cascade(label="Themes", menu=theme_menu)
        self.root.config(menu=menubar)

        # Blog-to-Audio Section
        blog_frame = tk.Frame(self.root)
        blog_frame.pack(pady=10)

        tk.Label(blog_frame, text="Blog URL:").grid(row=0, column=0, padx=5)
        self.blog_url_entry = tk.Entry(blog_frame, width=50)
        self.blog_url_entry.grid(row=0, column=1, padx=5)
        ttk.Button(blog_frame, text="Convert Blog to Audio", command=self.blog_to_audio).grid(row=0, column=2, padx=5)
        ttk.Button(blog_frame, text="Clear", command=self.clear_blog_url).grid(row=0, column=3, padx=5)

        # Text Input Section
        self.text_input = ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 14), height=12)
        self.text_input.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Translation & Language Controls
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=10)

        tk.Label(lang_frame, text="Translate to:").grid(row=0, column=0, padx=5)
        self.lang_selector = ttk.Combobox(lang_frame, values=list(self.languages.keys()), state="readonly", width=20)
        self.lang_selector.grid(row=0, column=1, padx=5)
        self.lang_selector.set("English")

        ttk.Button(lang_frame, text="Translate", command=self.translate_text).grid(row=0, column=2, padx=5)

        # TTS Controls
        tts_frame = tk.Frame(self.root)
        tts_frame.pack(pady=10)

        ttk.Button(tts_frame, text="Speak", command=self.speak_text).grid(row=0, column=0, padx=10)
        ttk.Button(tts_frame, text="Pause", command=self.pause_audio).grid(row=0, column=1, padx=10)
        ttk.Button(tts_frame, text="Resume", command=self.resume_audio).grid(row=0, column=2, padx=10)
        ttk.Button(tts_frame, text="Save Audio", command=self.save_audio).grid(row=0, column=3, padx=10)
        ttk.Button(tts_frame, text="Clear", command=self.clear_text).grid(row=0, column=4, padx=10)
        ttk.Button(tts_frame, text="Reset", command=self.reset_app).grid(row=0, column=5, padx=10)

        # Voice Customization
        customization_frame = tk.Frame(self.root)
        customization_frame.pack(pady=10)

        tk.Label(customization_frame, text="Speech Rate:").grid(row=0, column=0, padx=5)
        self.rate_slider = ttk.Scale(customization_frame, from_=50, to=300, orient=tk.HORIZONTAL, command=self.update_speech_rate)
        self.rate_slider.set(150)
        self.rate_slider.grid(row=0, column=1, padx=5)

        tk.Label(customization_frame, text="Voice:").grid(row=1, column=0, padx=5)
        self.voice_selector = ttk.Combobox(customization_frame, values=[v.name for v in self.voices], state="readonly", width=20)
        self.voice_selector.grid(row=1, column=1, padx=5)
        self.voice_selector.set(self.voices[0].name)

    def update_speech_rate(self, event=None):
        """Update the speech rate dynamically."""
        new_rate = int(self.rate_slider.get())
        self.engine.setProperty("rate", new_rate)

    def blog_to_audio(self):
        """Convert blog content to audio."""
        url = self.blog_url_entry.get()
        if not url:
            messagebox.showinfo("Info", "Please enter a blog URL.")
            return

        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join(p.get_text() for p in soup.find_all('p'))
            if not text:
                raise ValueError("No text could be extracted from the blog.")
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, text)
            messagebox.showinfo("Success", "Blog content loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch blog: {e}")

    def clear_blog_url(self):
        """Clear the blog URL field."""
        self.blog_url_entry.delete(0, tk.END)

    def translate_text(self):
        """Translate text to the selected language."""
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            target_lang = self.languages.get(self.lang_selector.get(), "en")
            try:
                translated = self.translator.translate(text, dest=target_lang)
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, translated.text)
                messagebox.showinfo("Success", "Text translated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Translation failed: {e}")

    def speak_text(self):
        """Start speaking the text."""
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            self.speech_queue.queue.clear()
            sentences = text.split('.')
            for sentence in sentences:
                self.speech_queue.put(sentence.strip())

            if not self.is_speaking:
                self.is_speaking = True
                self.pause_event.set()
                self.speech_thread = threading.Thread(target=self._speak)
                self.speech_thread.start()

    def _speak(self):
        """Speak text in a background thread."""
        selected_voice = self.voices[self.voice_selector.current()]
        self.engine.setProperty("voice", selected_voice.id)

        while not self.speech_queue.empty():
            if not self.pause_event.is_set():
                self.pause_event.wait()

            sentence = self.speech_queue.get()
            self.engine.say(sentence)
            self.engine.runAndWait()

        self.is_speaking = False

    def pause_audio(self):
        """Pause the audio playback."""
        if self.is_speaking:
            self.pause_event.clear()

    def resume_audio(self):
        """Resume audio playback."""
        if self.is_speaking:
            self.pause_event.set()

    def save_audio(self):
        """Save text as an audio file."""
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
            if file_path:
                tts = gTTS(text=text, lang='en')
                tts.save(file_path)
                messagebox.showinfo("Success", "Audio saved successfully!")

    def clear_text(self):
        """Clear the text input field."""
        self.text_input.delete("1.0", tk.END)

    def reset_app(self):
        """Reset the application state."""
        self.pause_audio()
        self.clear_text()
        self.clear_blog_url()
        self.rate_slider.set(150)
        self.lang_selector.set("English")
        self.voice_selector.set(self.voices[0].name)

    def apply_theme(self):
        """Apply the selected theme."""
        theme = self.current_theme.get()
        if theme == "Dark":
            self.root.config(bg="#333333")
            self.text_input.config(bg="#444444", fg="white", insertbackground="white")
        else:
            self.root.config(bg="#FFFFFF")
            self.text_input.config(bg="white", fg="black", insertbackground="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeakEasyApp(root)
    root.mainloop()
