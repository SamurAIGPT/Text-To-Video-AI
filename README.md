# Text To Video AI

[![Powered by MuAPI](https://img.shields.io/badge/Powered%20by-MuAPI-6366f1?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMSAxNHYtNGgtMnYtMmg0djZoLTJ6bTAtOFY2aDJ2MmgtMnoiLz48L3N2Zz4=)](https://muapi.ai?utm_source=github&utm_medium=badge&utm_campaign=text-to-video-ai)


Generate engaging videos from text prompts using AI. Perfect for creating YouTube Shorts, Instagram Reels, TikTok videos, and more.

[![GitHub stars](https://img.shields.io/github/stars/SamurAIGPT/Text-To-Video-AI?style=social)](https://github.com/SamurAIGPT/Text-To-Video-AI/stargazers)

> **Want to skip the setup?** Use our [Premium API](https://docs.vadoo.tv/docs/guide/ai-story/create-an-ai-video) to generate videos instantly - no installation required, production-ready, and scales with your needs.

<p align="center"><a href="https://www.youtube.com/watch?v=SOXsxqnQGlc"><img src="https://i.ytimg.com/vi/SOXsxqnQGlc/maxresdefault.jpg" width="720"></a></p>
<p align="center"><a href="https://www.youtube.com/watch?v=SOXsxqnQGlc"><b>▶ Watch: Best AI Video Generator (API) in 2026 (Quality, Price, Uncensored, Editing)</b></a></p>

## Demo

https://github.com/user-attachments/assets/1e440ace-8560-4e12-850e-c532740711e7

## Sample Videos

Here are sample videos generated end-to-end directly by this project using the React/Remotion composition engine:

<div align="center">
  <video src="https://github.com/user-attachments/assets/752c1d80-e011-4d2e-bc23-0dea2a091244" width="100%" controls></video>
</div>

> **"Wonders of Outer Space"** — An educational video about the cosmos, galaxies, and black holes. Generated using local EdgeTTS voiceover, whisper-timestamped local word captions, Suno AI background music, and Veo3 AI B-roll video segments.

<div align="center">
  <video src="https://github.com/user-attachments/assets/9718fba7-f9a4-45a6-bc7c-c7e5fa21c8cf" width="100%" controls></video>
</div>

> **"Exploring the Deep Ocean"** — A cinematic short exploring deep sea depths, bioluminescent creatures, and thermal vents. Generated using local EdgeTTS voiceover, whisper-timestamped local word captions, Suno AI background music, and Veo3 AI B-roll video segments.


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

### AI Video Generation (Muapi)

```env
# Muapi API credentials
MUAPI_BASE_URL=https://api.muapi.ai
MUAPI_API_KEY=your_key

# Video Model to use
MUAPI_VIDEO_MODEL=veo3-fast-text-to-video
```

**Supported Muapi Video Models:**
- **Google Veo:** `veo3-fast-text-to-video`, `veo3-text-to-video`, `veo3.1-fast-text-to-video`, `veo3.1-text-to-video`, `veo3.1-lite-text-to-video`
- **xAI Grok:** `grok-imagine-text-to-video`
- **ByteDance Seedance:** `sd-2-t2v` (Seedance 2), `seedance-2-vip-text-to-video`, `seedance-pro-t2v`, `seedance-lite-t2v`
- **Wan:** `wan2.7-text-to-video`, `wan2.6-text-to-video`, `wan2.5-text-to-video`, `wan2.1-text-to-video`
- **LTX:** `ltx-2.3-text-to-video`, `ltx-2-pro-text-to-video`, `ltx-2-fast-text-to-video`
- **Kling:** `kling-v3.0-pro-text-to-video`, `kling-v3.0-standard-text-to-video`
- **Vidu:** `vidu-q3-pro-text-to-video`, `vidu-q2-pro-text-to-video`
- **OpenAI Sora:** `openai-sora-2-pro-text-to-video`, `openai-sora-2-standard-text-to-video`
- **MiniMax:** `minimax-hailuo-2.3-pro-t2v`, `minimax-hailuo-2.3-standard-t2v`
- **Alibaba:** `happy-horse-1-text-to-video-1080p`


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

- [MuAPI video-generation docs](https://muapi.ai/docs/video-generation) — API patterns for text-to-video generation.
- [Veo 3 text-to-video playground](https://muapi.ai/playground/veo3-text-to-video) — Try a production video model in the browser.

| Project | Description |
|---------|-------------|
| [AI Influencer Generator](https://github.com/SamurAIGPT/AI-Influencer-Generator) | Create AI-powered virtual influencers |
| [AI YouTube Shorts Generator](https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator/) | Automated YouTube Shorts creation |
| [Faceless Video Generator](https://github.com/SamurAIGPT/Faceless-Video-Generator) | Create videos without showing your face |
| [AI B-roll Generator](https://github.com/Anil-matcha/AI-B-roll) | Generate B-roll footage with AI |

- [awesome-ai-video-models](https://github.com/Anil-matcha/awesome-ai-video-models) — compare AI video models by API, price & speed
- [ai-creator-academy](https://github.com/Anil-matcha/ai-creator-academy) — free curriculum teaching creators how to monetize AI-generated video content

### Vadoo AI Tools

- [AI Video Generator](https://www.vadoo.tv/ai-video-generator)
- [Text to Video AI](https://www.vadoo.tv/text-to-video-ai)
- [Autoshorts AI](https://www.vadoo.tv/autoshorts-ai)
- [Pixverse Alternative](https://www.vadoo.tv/pixverse-ai)
- [Hailuo AI Alternative](https://www.vadoo.tv/hailuo-ai)
- [Minimax AI Alternative](https://www.vadoo.tv/minimax-ai)

---

## Support

If you find this project useful, please consider giving it a star! Your support helps us continue improving the project.

[![GitHub stars](https://img.shields.io/github/stars/SamurAIGPT/Text-To-Video-AI?style=social)](https://github.com/SamurAIGPT/Text-To-Video-AI/stargazers)
