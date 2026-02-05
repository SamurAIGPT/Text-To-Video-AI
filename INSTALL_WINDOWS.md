# Windows Installation Guide

## Prerequisites

### 1. Install Python 3.10 or 3.11

Download and install from https://www.python.org/downloads/

**Important:** During installation, check ✅ "Add Python to PATH"

Verify installation:
```cmd
python --version
```

---

### 2. Install FFmpeg

**Option A: Using Scoop (Recommended)**
```powershell
# Install Scoop first (run in PowerShell as Administrator)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install ffmpeg
scoop install ffmpeg
```

**Option B: Using Chocolatey**
```powershell
# Install Chocolatey first (run in PowerShell as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install ffmpeg
choco install ffmpeg
```

**Option C: Manual Installation**
1. Download from https://www.gyan.dev/ffmpeg/builds/ (get `ffmpeg-release-essentials.zip`)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH:
   - Search "Environment Variables" in Windows
   - Click "Environment Variables"
   - Under "System variables", select "Path" → Edit
   - Add `C:\ffmpeg\bin`
   - Click OK and restart terminal

Verify installation:
```cmd
ffmpeg -version
```

---

### 3. Install ImageMagick

1. Download from https://imagemagick.org/script/download.php#windows
   - Choose the installer ending with `-Q16-HDRI-x64-dll.exe`

2. During installation:
   - ✅ Check "Install legacy utilities (e.g. convert)"
   - ✅ Check "Add application directory to your system path"

3. **Configure for MoviePy** - Create/edit the file `C:\Users\<YourUsername>\.moviepy\config_defaults.py`:
   ```python
   IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
   ```
   (Adjust the path to match your installed version)

Verify installation:
```cmd
magick -version
```

---

## Project Setup

```cmd
# Clone the repository
git clone https://github.com/SamurAIGPT/Text-To-Video-AI.git
cd Text-To-Video-AI

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment file
copy .env.example .env
# Edit .env with your API keys (use notepad or any text editor)
notepad .env
```

## Required API Keys

Get these API keys and add them to your `.env` file:

| Service | Get API Key From |
|---------|------------------|
| OpenAI / Groq / Gemini | Choose one LLM provider |
| Pexels | https://www.pexels.com/api/new/ |
| Deepgram (optional) | https://console.deepgram.com/ |
| ElevenLabs (optional) | https://elevenlabs.io/ |

## Run the Application

```cmd
python app.py "Your topic here"
```

Output will be saved as `rendered_video.mp4`

---

## Troubleshooting

### "ffmpeg not found"
- Restart your terminal/command prompt after installation
- Verify PATH is set correctly: `echo %PATH%`

### "ImageMagick not found" or text not rendering
- Make sure you installed with "legacy utilities" option
- Create the MoviePy config file as shown above
- Try running `magick -version` to verify installation

### "PEXELS_API_KEY not found" or "KeyError: 'videos'"
- Make sure your `.env` file has a valid `PEXELS_API_KEY`
- Get a free key from https://www.pexels.com/api/new/
