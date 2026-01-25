from deepgram import DeepgramClient, DeepgramClientOptions, PrerecordedOptions, FileSource
import re


def generate_timed_captions(audio_filename, api_key=None):
    """
    Generate timed captions using Deepgram API.
    Returns same format as Whisper: [((start_time, end_time), "text"), ...]
    """
    if api_key is None:
        from utility.config import get_config
        config = get_config()
        api_key = config.get_deepgram_api_key()
    
    try:
        deepgram = DeepgramClient(api_key)
        
        with open(audio_filename, 'rb') as audio_file:
            buffer_data = audio_file.read()
        
        payload: FileSource = {
            "buffer": buffer_data,
        }
        
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            utterances=True,
            punctuate=True,
            diarize=False,
            timestamps=True,
            paragraphs=False
        )
        
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        
        if not response or not response.results or not response.results.channels:
            print("No transcription results from Deepgram")
            return []
        
        channel = response.results.channels[0]
        words = channel.alternatives[0].words if channel.alternatives else []
        
        if not words:
            print("No words in transcription")
            return []
        
        return _process_deepgram_words(words)
        
    except Exception as e:
        print(f"Error generating captions with Deepgram: {e}")
        raise


def _process_deepgram_words(words):
    """
    Process Deepgram word-level timestamps into caption format.
    Returns: [((start_time, end_time), "text"), ...]
    """
    captions = []
    
    max_caption_size = 15
    half_caption_size = max_caption_size / 2
    
    i = 0
    while i < len(words):
        current_caption = words[i].word.strip()
        start_time = words[i].start
        
        j = i + 1
        while j < len(words):
            next_word = words[j].word.strip()
            if len(current_caption + ' ' + next_word) <= max_caption_size:
                current_caption += ' ' + next_word
                end_time = words[j].end
                j += 1
                
                if len(current_caption) >= half_caption_size and j < len(words):
                    break
            else:
                break
        
        if not end_time:
            end_time = words[j-1].end
        
        caption_text = _clean_word(current_caption)
        if caption_text:
            captions.append(((start_time, end_time), caption_text))
        
        i = j
    
    return captions


def _clean_word(word):
    """
    Clean word by removing special characters except quotes, hyphens, and underscores.
    """
    return re.sub(r'[^\w\s\-_"\'\']', '', word)
