Zumub Speech-to-Text App Using Whisper API

Description

Zumub Speech-to-Text Whisper presents a highly efficient, Windows-based application developed to harness the power of OpenAI's Whisper API, aiming to transform speech into text seamlessly. With this application, users can dictate text directly into any text input field, effectively replacing the need for manual typing, ideal for sending emails, instant messaging, creating documents, or transcribing meetings and phone calls.

Features

    Hotkey Activation: Swiftly start and stop transcription using a customizable hotkey
    Quick Transcription: Leveraging Open AI’s Whisper API for quick and accurate transcriptions in multiple languages and offers AI corrections.
    Versatile Use: Seamlessly inserts transcribed text into any selected text input field.
    Customizable: Adjust hotkey bindings and prompts as per your convenience.

Installation & Setup

Clone or Download the Repository:
    
    git clone <repository-link>

Install Python: Ensure Python is installed on your system.
Install FFMPEG
Install Required Libraries:

    pip install -r requirements.txt

Generate an Installer with PyInstaller:

    Install PyInstaller: If not already installed, you can install PyInstaller by running the following command:
    
      pip install pyinstaller
    
    Navigate to the Project Directory: Open a command prompt/terminal window and navigate to the directory containing your project files.
    
    Generate the Executable: Run the following command to create a standalone executable with no console window:
    
      pyinstaller --onefile --noconsole speech2text.py
      
    Locate the Executable: Once the process is complete, you can find the generated executable in the dist folder within your project directory.
    
    Note:
    Access Permissions: If you encounter an 'Access is denied' error while running PyInstaller, ensure that the command prompt/terminal is run as an Administrator.
    .env File: After installation, users should have a .env file generated along with the executable, which they will need to configure with their OpenAI API Key and other settings.

Get OpenAI API Key:

    Register at OpenAI and obtain an API key.

Configure .env File:

    Update the .env file with the OpenAI API key, modify the hotkey binding and the custom prompt as required.

    env
        OPENAI_API_KEY="Your_API_Key"
        KEYBOARD_BINDING="control+\\"
        CUSTOM_PROMPT="Your Custom Prompt"




Usage

    Position the cursor in any text input field where you wish to insert the transcribed text.
    Activate the application using the configured hotkey to start transcribing.
    Speak clearly and once done, use the hotkey again to stop the transcription.
    Review the Transcription: The transcribed text will be automatically inserted at the cursor position.

Support Zumub

We are elated to contribute to the community by providing this software completely free of charge! If you find value in this app, consider exploring what Zumub has to offer in high-quality supplements. 
Visit www.zumub.com for more details on our products, follow us on our social media platforms, or share your experience with our app to support our endeavors.

Connect with us:

Instagram | Facebook | Twitter

Troubleshooting

For any issues encountered while using the app, refer to the app.log file in the project directory for error logs and information, or connect with our community for support.

License

This project is released under an open-source license. Users are encouraged to modify and distribute their versions of the application, respecting the terms stated in the LICENSE file.

💚 Heartfelt Thanks from Zumub! Elevate your fitness journey with us! 💚
