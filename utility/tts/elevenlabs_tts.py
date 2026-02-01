from elevenlabs import ElevenLabs


async def generate_audio(text, outputFilename, voice_id, api_key=None):
    """
    Generate audio using ElevenLabs API.
    
    Args:
        text: The text to convert to speech
        outputFilename: The path to save the audio file
        voice_id: The ElevenLabs voice ID to use
        api_key: The ElevenLabs API key (optional, will use config if not provided)
    """
    if api_key is None:
        from utility.config import get_config
        config = get_config()
        api_key = config.get_elevenlabs_api_key()
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        with open(outputFilename, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        
    except Exception as e:
        print(f"Error generating audio with ElevenLabs: {e}")
        raise
