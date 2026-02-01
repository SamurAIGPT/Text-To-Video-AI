import whisper_timestamped as whisper
from whisper_timestamped import load_model, transcribe_timestamped
import re


def generate_timed_captions(audio_filename, model_size="base"):
    WHISPER_MODEL = load_model(model_size)
    
    gen = transcribe_timestamped(WHISPER_MODEL, audio_filename, verbose=False, fp16=False)
    
    return getCaptionsWithTime(gen)


def splitWordsBySize(words, maxCaptionSize):
    
    halfCaptionSize = maxCaptionSize / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= halfCaptionSize and words:
                break
        captions.append(caption)
    return captions


def getTimestampMapping(whisper_analysis):
    index = 0
    locationToTimestamp = {}
    text = whisper_analysis['text']
    
    for segment in whisper_analysis['segments']:
        for word in segment['words']:
            clean_text = cleanWord(word['text'])
            newIndex = index + len(clean_text)+1
            locationToTimestamp[(index, newIndex)] = (word['start'], word['end'])
            index = newIndex
    return locationToTimestamp


def cleanWord(word):
    
    return re.sub(r'[^\w\s\-_%\']', '', word)


def interpolateTimeFromDict(word_position, d):
    
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None


def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15, considerPunctuation=False):
    
    CaptionsPairs = []
    last_end = 0
    
    for segment in whisper_analysis['segments']:
        for word_info in segment['words']:
            clean_word = cleanWord(word_info['text'])
            if clean_word:
                start = word_info['start']
                end = word_info['end']
                
                # Fix all timestamp issues including multiple words with same end time
                # Check if there's any problem: zero duration, backwards, or overlap
                if start >= end or start < last_end or end <= last_end:
                    # Set start from last_end to ensure sequential order
                    start = last_end
                    # Set end slightly forward to ensure minimum duration
                    end = last_end + 0.3
                
                # Update last_end for next word
                last_end = end
                
                CaptionsPairs.append(((start, end), clean_word))
    
    return CaptionsPairs
