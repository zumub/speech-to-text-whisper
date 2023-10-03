# Zumub Speech-to-Text App Using Whisper API
### Description
Zumub Speech-to-Text Whisper presents a highly efficient, Windows-based application developed to harness the power of OpenAI's Whisper API, aiming to transform speech into text seamlessly. With this application, users can dictate text directly into any text input field, effectively replacing the need for manual typing, ideal for sending emails, instant messaging, creating documents, or transcribing meetings and phone calls..

### Features
- **Hotkey Activation**: Swiftly start and stop transcription using a customizable hotkey
- **Quick Transcription**: Leveraging Open AI’s Whisper API for quick and accurate transcriptions in multiple languages and offers AI corrections.
- **Versatile Use**: Seamlessly inserts transcribed text into any selected text input field.
- **Customizable**: Adjust hotkey bindings and prompts as per your convenience.

# Installation & Setup
## For Windows:
### Step 1: Clone or Download the Repository:
```bash
git clone https://github.com/zumub/speech-to-text-whisper
```
### Step 2: Install Python:
- To install manually: 
  -- Go to the [Python Downloads](https://www.python.org/downloads/) page and download the installer for the latest Python version.
  -- Run the installer and follow the prompts to install Python. 
  > [!NOTE] Click 'Add Python to PATH' when installing.
  
- To install with terminal: 
  -- Install **Chocolatey** (Package Manager)
  ```bash
  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((Invoke-WebRequest -Uri https://chocolatey.org/install.ps1).Content)
  ```
  -- Install **Python**
  ```bash
  choco install python
  ```
  -- Confirm the installation and check the Python version:
  ```bash
  python --version
  ```
	> [!NOTE] 
	> - The paths to the Python and FFmpeg executables should be automatically added to the System PATH by Chocolatey. If not, you might need to add them manually or restart your computer to apply the changes.
    > - For more information or troubleshooting during installation, you can visit the [Chocolatey](https://chocolatey.org/install) and [Python](https://www.python.org/) official documentation.

### Step 3: Install FFmpeg:
- To download FFmpeg manually: [FFmpeg downloads](https://ffmpeg.org/download.html) 
- To install with terminal: 
  -- Install **Chocolatey** (Package Manager), if not installed for python.
  ```bash
  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((Invoke-WebRequest -Uri https://chocolatey.org/install.ps1).Content)
  ```
  -- Install **FFmpeg**
  ```bash
  choco install ffmpeg
  ```
  -- Confirm the installation and check the FFmpeg version:
  ```bash
  ffmpeg -version
  ```
	> [!NOTE] 
	> - The paths to the FFmpeg executables should be automatically added to the System PATH by Chocolatey. If not, you might need to add them manually or restart your computer to apply the changes.
    > - For more information or troubleshooting during installation, you can visit the [Chocolatey](https://chocolatey.org/install) and [FFmpeg](https://ffmpeg.org/) official documentation.
### Step 4: Install project dependencies
- Open terminal in project directory and run the following command:
  ```bash
  pip install -r requirements.txt
  ```
### Step 5: Create an executeable file
> [!NOTE] PyInstaller is required to create an executeable file. .
- Open terminal and run the following command:
  ```bash
  pip install pyinstaller
  ```
- Confirm the installation and check pyinstaller version:
  ```bash
  pyinstaller --version
  ```
- Navigate to project directory and run the following command:
  ```bash
  pyinstaller --onefile --noconsole speech2text.py
  ```
> [!WARNING]  Windows security/Anitivirus may prompt for virus, Allow on device to complete installation.

> [!NOTE] 
> - Once the process is complete, you can find the generated executable in the dist folder within your project directory.
> - After installation, users should have a .env file generated along with the executable, which they will need to configure with their OpenAI API Key and other settings
### Step 6: Configure .env File:
- Register at [OpenAI](https://platform.openai.com/signup) and obtain an API key.
- Update the [.env](/.env) file with the OpenAI API key, modify the hotkey binding and the custom prompt as required.
  ```
  OPENAI_API_KEY="YOUR_OPENAI_API_HERE"
  CUSTOM_PROMPT=""
  KEYBOARD_BINDING="control+\\"
  ```

  

## For Mac:
### Step 1: Clone or Download the Repository:
```bash
git clone https://github.com/zumub/speech-to-text-whisper
```

### Step 2: Install Python:
- To install manually: 
  -- Go to the [Python Downloads](https://www.python.org/downloads/macos/) page and download the installer for the latest Python version.
  -- Run the installer and follow the prompts to install Python.  
- To install with terminal: 
  -- Install **Homebrew** (Package Manager)
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  
  ```
  -- Install **Python**
  ```bash
  brew install python
  ```
  -- Confirm the installation and check the Python version:
  ```bash
  python3 --version
  ```
	> [!NOTE] 
	> - For more information or troubleshooting during installation, you can visit the [Homebrew](https://brew.sh/) and [Python](https://www.python.org/) official documentation.

### Step 3: Install FFmpeg:
- To download FFmpeg manually: [FFmpeg downloads](https://ffmpeg.org/download.html) 
- To install with terminal: 
  -- Install **Homebrew** (Package Manager), if not installed for python.
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  
  ```
  -- Install FFmpeg
  ```bash
  brew install ffmpeg
  ```
  -- Confirm the installation and check the FFmpeg version:
  ```bash
  ffmpeg -version
  ```
	> [!NOTE] 
	> - For more information or troubleshooting during installation, you can visit the [Homebrew](https://brew.sh/) and [FFmpeg](https://ffmpeg.org/) official documentation.
### Step 4: Install project dependencies
- Open terminal in project directory and run the following command:
  ```bash
  pip3 install -r requirements.txt
  ```
### Step 5: Create an executeable file
> [!NOTE] PyInstaller is required to create an executeable file. .
- Open terminal and run the following command:
  ```bash
  pip3 install pyinstaller
  ```
- Confirm the installation and check pyinstaller version:
  ```bash
  pyinstaller --version
  ```
- Navigate to project directory and run the following command:
  ```bash
  pyinstaller --onefile --noconsole speech2text.py
  ```
> [!WARNING]  Mac security/Anitivirus may prompt for virus, Allow on device to complete installation.

> [!NOTE] 
> - Once the process is complete, you can find the generated executable in the dist folder within your project directory.
> - After installation, users should have a .env file generated along with the executable, which they will need to configure with their OpenAI API Key and other settings
### Step 6: Configure .env File:
- Register at [OpenAI](https://platform.openai.com/signup) and obtain an API key.
- Update the [.env](/.env) file with the OpenAI API key, modify the hotkey binding and the custom prompt as required.
  ```
  OPENAI_API_KEY="YOUR_OPENAI_API_HERE"
  CUSTOM_PROMPT=""
  KEYBOARD_BINDING="control+\\"
  ```

## Usage
- Position the cursor in any text input field where you wish to insert the transcribed text.
- Activate the application using the configured hotkey to start transcribing.
- Speak clearly and once done, use the hotkey again to stop the transcription.
- Review the Transcription: The transcribed text will be automatically inserted at the cursor position.

# Support Zumub

We are elated to contribute to the community by providing this software completely free of charge! If you find value in this app, consider exploring what Zumub has to offer in high-quality supplements. Visit [Zumub](http://www.zumub.com) for more details on our products, follow us on our social media platforms, or share your experience with our app to support our endeavors.

**Connect with us:**
| Platform | Link |
| :------------- | :------------- |
| Website | https://www.zumub.com/ |
| Instagram | https://www.instagram.com/zumub.pt/ |
| Facebook | https://www.facebook.com/zumub.pt/ |
| Twitter | https://twitter.com/zumub_pt |

**Troubleshooting:**
For any issues encountered while using the app, refer to the app.log file in the project directory for error logs and information, or connect with our community for support.

**License**
Copyright (C) 2023 Zumub S.A.

This project is released under an MIT license. Users are encouraged to modify and distribute their versions of the application, respecting the terms stated in the LICENSE file.

💚 Heartfelt Thanks from Zumub! Elevate your fitness journey with us! 💚
