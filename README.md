# Text To Video AI

Generate engaging videos from text prompts using AI. Perfect for creating YouTube Shorts, Instagram Reels, TikTok videos, and more.

[![GitHub stars](https://img.shields.io/github/stars/SamurAIGPT/Text-To-Video-AI?style=social)](https://github.com/SamurAIGPT/Text-To-Video-AI/stargazers)

> **Want to skip the setup?** Use our [Premium API](https://docs.vadoo.tv/docs/guide/ai-story/create-an-ai-video) to generate videos instantly - no installation required, production-ready, and scales with your needs.

## Demo

https://github.com/user-attachments/assets/1e440ace-8560-4e12-850e-c532740711e7

## Features

- **AI-Powered Script Generation** - Automatically generates engaging scripts from any topic
- **Multiple LLM Providers** - Choose from OpenAI, Groq, or Google Gemini
- **Text-to-Speech** - Natural-sounding voiceovers with EdgeTTS (free) or ElevenLabs
- **Automatic B-Roll** - Fetches relevant background videos from Pexels
- **Customizable Captions** - Full control over font, color, position, and styling
- **Multiple Orientations** - Portrait (9:16) for shorts or Landscape (16:9) for traditional video
- **Speech-to-Text** - Accurate caption timing with Whisper or Deepgram

## Quick Start

**Option 1: Use the Premium API (Recommended)**

Skip all setup and generate videos with a single API call:
- [Premium API Documentation](https://docs.vadoo.tv/docs/guide/ai-story/create-an-ai-video)

**Option 2: Google Colab**

Run directly in your browser with our [Colab Notebook](Text_to_Video_example.ipynb)

**Option 3: Local Installation**

See installation instructions below.

## Installation

### Prerequisites

- Python 3.8+
- FFmpeg
- ImageMagick

**Windows users:** See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for detailed setup instructions.

### Setup

```bash
# Clone the repository
git clone https://github.com/SamurAIGPT/Text-To-Video-AI.git
cd Text-To-Video-AI

# Install dependencies
pip install -r requirements.txt

# Create your configuration file
cp .env.example .env
```

Edit `.env` with your API keys (see Configuration below).

### Usage

```bash
python app.py "Your topic here"
```

Output will be saved as `rendered_video.mp4`

## Configuration

All settings are configured via the `.env` file. Copy `.env.example` to get started.

### API Keys

| Service | Required | Get API Key |
|---------|----------|-------------|
| Pexels | Always | [pexels.com/api](https://www.pexels.com/api/new/) |
| OpenAI | If using OpenAI | [platform.openai.com](https://platform.openai.com/api-keys) |
| Groq | If using Groq | [console.groq.com](https://console.groq.com/keys) |
| Google Gemini | If using Gemini | [makersuite.google.com](https://makersuite.google.com/app/apikey) |
| Deepgram | If using Deepgram STT | [console.deepgram.com](https://console.deepgram.com/) |
| ElevenLabs | If using ElevenLabs TTS | [elevenlabs.io](https://elevenlabs.io/) |

### Provider Selection

```env
# LLM Provider: openai, groq, or gemini
LLM_PROVIDER=openai

# Text-to-Speech: edgetts (free) or elevenlabs
TTS_PROVIDER=edgetts

# Speech-to-Text: whisper (free) or deepgram
STT_PROVIDER=whisper
```

### Video Settings

```env
# Orientation: portrait (1080x1920) or landscape (1920x1080)
# Portrait recommended for YouTube Shorts, Instagram Reels, TikTok
VIDEO_ORIENTATION=portrait
```

### Caption Settings

```env
# Enable or disable captions
CAPTIONS_ENABLED=true

# Caption styling
CAPTION_FONT_SIZE=100
CAPTION_FONT_COLOR=white
CAPTION_FONT_FACE=Arial-Bold
CAPTION_STROKE_WIDTH=3
CAPTION_STROKE_COLOR=black
CAPTION_POSITION=bottom_center
```

**Caption Position Options:** `center`, `top`, `bottom`, `bottom_center`, `bottom_left`, `bottom_right`

**Font Color Options:** `white`, `yellow`, `cyan`, `red`, `green`, `blue`, `magenta`

### Voice Configuration

**EdgeTTS (Free):**
```env
EDGETTS_VOICE=en-AU-WilliamNeural
```

Popular voices:
- `en-US-ChristopherNeural` - American male
- `en-US-JennyNeural` - American female
- `en-GB-RyanNeural` - British male
- `en-GB-SoniaNeural` - British female
- `en-AU-WilliamNeural` - Australian male

**ElevenLabs:**
```env
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=your_voice_id
```

## Tutorials

- [YouTube Tutorial](https://www.youtube.com/watch?v=AXo6VfRUgic)
- [Medium Guide](https://medium.com/@anilmatcha/text-to-video-ai-how-to-create-videos-for-free-a-complete-guide-a25c91de50b8)

## Contributing

We welcome contributions! To get started:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Premium API

Looking for a production-ready solution? Our [Premium API](https://docs.vadoo.tv/docs/guide/ai-story/create-an-ai-video) offers:

- No installation or setup required
- Multiple video durations (30s to 10 minutes)
- Advanced voice and language options
- Custom styling and branding
- Scalable infrastructure

[Get Started with the API](https://docs.vadoo.tv/docs/guide/ai-story/create-an-ai-video)

---

## Related Projects

| Project | Description |
|---------|-------------|
| [AI Influencer Generator](https://github.com/SamurAIGPT/AI-Influencer-Generator) | Create AI-powered virtual influencers |
| [AI YouTube Shorts Generator](https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator/) | Automated YouTube Shorts creation |
| [Faceless Video Generator](https://github.com/SamurAIGPT/Faceless-Video-Generator) | Create videos without showing your face |
| [AI B-roll Generator](https://github.com/Anil-matcha/AI-B-roll) | Generate B-roll footage with AI |

### Vadoo AI Tools

- [AI Video Generator](https://www.vadoo.tv/ai-video-generator)
- [Text to Video AI](https://www.vadoo.tv/text-to-video-ai)
- [Autoshorts AI](https://www.vadoo.tv/autoshorts-ai)

---

## Support

If you find this project useful, please consider giving it a star! Your support helps us continue improving the project.

[![GitHub stars](https://img.shields.io/github/stars/SamurAIGPT/Text-To-Video-AI?style=social)](https://github.com/SamurAIGPT/Text-To-Video-AI/stargazers)
