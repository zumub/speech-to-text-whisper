# Copyright (C) 2023 Zumub S.A.
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
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
import keyboard  
from global_hotkeys import *

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
custom_prompt = os.getenv("CUSTOM_PROMPT")
keyboard_binding = os.getenv("KEYBOARD_BINDING")

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

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    try:
        with subprocess.Popen(command, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            try:
                stdout, stderr = process.communicate(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
    except Exception as e:
        #logging.error("An error occurred:", str(e))
        logging.error(f"An error occurred: {str(e)}, Stdout: {stdout}, Stderr: {stderr}")        
#logging.debug('This will get logged')

def get_transcript(app):
    try:
        latest_file = 'output.mp3'
        with open(latest_file, "rb") as audio_file:
             response = openai.Audio.transcribe("whisper-1", audio_file, prompt=custom_prompt)
        transcript_text = response['text']
        print(custom_prompt)
        print(transcript_text)
        pyperclip.copy(transcript_text)
        keyboard.send('ctrl+v')
    finally:
        app.color_indicator.config(bg='green')

class AudioRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Zumub Whisper speech-to-text")
        self.root.geometry("200x40")
        self.is_recording = False
        self.record_thread = None

        self.start_button = ttk.Button(self.root, text="Start", command=self.toggle_record)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.transcript_label = ttk.Label(self.root, text="", wraplength=350)
        self.transcript_label.grid(row=1, column=0, padx=10, pady=10)

        self.root.wm_attributes("-topmost", 1)
        
        self.color_indicator = tk.Canvas(self.root, width=10, height=10, bg='green')
        self.color_indicator.grid(row=0, column=1)
        
        bindings = [
            [keyboard_binding, None, self.toggle_record, False],
        ]
        register_hotkeys(bindings)
        threading.Thread(target=start_checking_hotkeys).start() 

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
