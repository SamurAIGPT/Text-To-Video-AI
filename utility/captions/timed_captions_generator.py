from utility.config import get_config


def generate_timed_captions(audio_filename):
    config = get_config()
    stt_provider = config.get_stt_provider()
    
    if stt_provider == 'whisper':
        from utility.stt.whisper_stt import generate_timed_captions as whisper_captions
        return whisper_captions(audio_filename)
    elif stt_provider == 'deepgram':
        from utility.stt.deepgram_stt import generate_timed_captions as deepgram_captions
        return deepgram_captions(audio_filename)
    else:
        raise ValueError(f"Unknown STT provider: {stt_provider}")
