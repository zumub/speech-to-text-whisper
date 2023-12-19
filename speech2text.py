# Copyright (C) 2023 Zumub S.A.
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import platform
import tkinter as tk
from tkinter import ttk
import threading
import pyaudio
import wave
from dotenv import load_dotenv
import os
import openai
import pyperclip
import logging
import subprocess
import time
from pynput import keyboard
from pynput.keyboard import Controller, Key, Listener

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
custom_prompt = os.getenv("CUSTOM_PROMPT")

if platform.system() == "Windows":
    keyboard_binding = os.getenv("KEYBOARD_BINDING","alt_l+\\")
else:
    keyboard_binding = os.getenv("KEYBOARD_BINDING","cmd+\\")
keys = keyboard_binding.split('+')
modifier_key = keys[0].strip().lower()
binding_key = keys[1].strip()

keep_on_top = os.getenv("KEEP_ON_TOP", "false").lower() == "true"
resend_button = os.getenv("RESEND_BUTTON", "false").lower() == "true"

auto_detect_language = os.getenv("AUTO_DETECT_LANGUAGE", "false").lower() == "true"
lang = os.getenv("LANGUAGES")
#If no languages, then change to auto detect language
if not lang: 
    auto_detect_language = 'true'
else: 
    languages = lang.split(',')
listener = None

logging.basicConfig(filename='app.log', level=logging.DEBUG)

def my_custom_export(input_file_path, output_file_path, format):
    logging.debug('Entering my_custom_export')

    command = [
        "ffmpeg",
        "-y",
        "-i", input_file_path,
        "-af", "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-50dB",
        "-vn",
        "-codec:a", "libmp3lame",
        "-q:a", "0",
        output_file_path
    ]

    try:
        if platform.system() == "Windows":
            # Use Windows-specific startup info to hide the window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            with subprocess.Popen(command, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                try:
                    stdout, stderr = process.communicate(timeout=30)
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
        else:  # macOS and others
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                try:
                    stdout, stderr = process.communicate(timeout=30)
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}, Stdout: {stdout}, Stderr: {stderr}")

MAX_RETRIES = 1  # Define a constant for maximum retries

def contains_prompt(partial_prompt, transcript_text):
    # Tokenize the prompt and the transcript
    prompt_tokens = set(partial_prompt.lower().split())
    transcript_tokens = set(transcript_text.lower().split())

    # If the prompt has less than 8 words, simply return False, no need to retry
    if len(prompt_tokens) < 8:
        return False

    # Calculate the number of prompt tokens present in the transcript
    common_tokens = prompt_tokens.intersection(transcript_tokens)

    # Calculate the percentage of prompt in the transcript
    percentage = (len(common_tokens) / len(prompt_tokens)) * 100

    return percentage >= 40

def get_transcript(app):
    try:
        latest_file = 'output.mp3'
        retries = 0

        while retries < MAX_RETRIES:
            with open(latest_file, "rb") as audio_file:
                transcribe_args = {
                    "file": audio_file,
                    "model": "whisper-1",
                    "prompt": custom_prompt
                }
                if not auto_detect_language:
                    transcribe_args["language"] = app.current_language          
                response = openai.Audio.transcribe(**transcribe_args)
            transcript_text = response['text']

            if contains_prompt(custom_prompt, transcript_text):
                # Handle the erroneous situation.
                logging.error(f"Detected partial prompt in transcript. Retry {retries + 1} of {MAX_RETRIES}.")
                retries += 1
                continue
            else:
                # If transcript is successful, break the loop
                break
        else:
            # This block will execute if the loop completes without breaking (all retries exhausted)
            logging.error(f"Failed to get a valid transcript after {MAX_RETRIES} attempts.")
            return
        
        print(transcript_text)
        pyperclip.copy(transcript_text)
        paste_text()
            
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    finally:
        app.color_indicator.config(bg='green')

def paste_text():
    if platform.system() == "Windows":
        with Controller() as keyboard:
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release('v')
            keyboard.release(Key.ctrl)
    else:
        with Listener(on_press=None, on_release=None) as listener:
            with Controller() as keyboard:
                keyboard.press(Key.cmd)
                keyboard.press('v')
                keyboard.release('v')
                keyboard.release(Key.cmd)

class AudioRecorder:
    def __init__(self, root):
        self.width = 200
        self.height = 40
        self.root = root
        self.root.title("Zumub Whisper speech-to-text")
        self.root.geometry(f"{self.width}x{self.height}")
        self.is_recording = False
        self.record_thread = None

        self.start_button = ttk.Button(self.root, text="Start", command=self.toggle_record)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.transcript_label = ttk.Label(self.root, text="", wraplength=350)
        self.transcript_label.grid(row=1, column=0, padx=10, pady=10)
        if keep_on_top:
            self.root.wm_attributes("-topmost", 1)
            self.root.bind('<Unmap>', self.prevent_minimize)		
        self.color_indicator = tk.Canvas(self.root, width=10, height=10, bg='green')
        self.color_indicator.grid(row=0, column=1)
        
        if resend_button:
            self.width += 50
            self.root.geometry(f"{self.width}x{self.height}")
            self.resend_button = ttk.Button(self.root, text="Resend", command=self.handle_resend)
            self.resend_button.grid(row=0, column=2, padx=10, pady=10)
        
        if not auto_detect_language:
            self.width += 60
            self.root.geometry(f"{self.width}x{self.height}")
            self.language_var = tk.StringVar()
            self.language_var.set(languages[0])  # Set the default language
            self.language_dropdown = ttk.Combobox(self.root, textvariable=self.language_var, values=languages, width=3, state="readonly")
            self.language_dropdown.grid(row=0, column=3, padx=10, pady=10)
            self.language_dropdown.bind("<<ComboboxSelected>>", self.on_language_selected)
            self.current_language = languages[0]

        # Initialize the listener
        self.current_keys = set()
        self.key_combination = [
            getattr(keyboard.Key, k, k) if 'Key.' in k else k for k in keys
        ]

        #self.listener = keyboard.Listener(on_press=self.on_press)
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.daemon = True
        listener.start()  # this will run listener in separate thread

    if resend_button:        
        def handle_resend(self):
            self.color_indicator.config(bg='yellow')
            threading.Thread(target=get_transcript, args=(self,)).start()

    def on_language_selected(self, event):
        self.current_language = self.language_var.get()
        self.root.focus_set()

    def prevent_minimize(self, event=None):
        self.root.after(10, self.root.deiconify)		

    def on_press(self, key):
        try:
            key_str = key.char
        except AttributeError:  # Special keys will be of Key type, and won't have 'char' attribute
            key_str = str(key).split('.')[1]
        
        self.current_keys.add(key_str)
        if all(k in self.current_keys for k in self.key_combination):
            self.toggle_record()
            self.current_keys.clear()
    
    def on_release(self,key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key).split('.')[1]
        self.current_keys.discard(key_str)

    def toggle_record(self):
        if self.is_recording:
            self.start_button.config(text="Start")
            self.color_indicator.config(bg='yellow')
            self.is_recording = False
            self.record_thread.join()
            get_transcript(self)
        else:
            self.is_recording = True
            self.record_thread = threading.Thread(target=self.record_audio)
            self.record_thread.start()
            self.start_button.config(text="Stop")
            self.color_indicator.config(bg='yellow')

    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
        frames = []

        while self.is_recording:
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open("output.wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        my_custom_export("output.wav", "output.mp3", "mp3")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorder(root)
    root.mainloop()
