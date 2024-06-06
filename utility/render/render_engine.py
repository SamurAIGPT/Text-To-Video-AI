import time
from moviepy.editor import (AudioFileClip, CompositeVideoClip,CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip, vfx,)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import os
import platform
import sys
import subprocess
import subprocess
import tempfile
import numpy as np

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

OUTPUT_FILE_NAME = "rendered_video_{}.mp4".format(round(time.time()*1000)) 
def get_output_media(audio_file_path,timed_captions,background_video_data,video_server):
    magick_path = get_program_path("magick")
    print(magick_path)
    if magick_path:
        os.environ['IMAGEMAGICK_BINARY'] = magick_path
    visual_clips = []
    for (t1, t2), video_url in background_video_data:
        video_clip = VideoFileClip(video_url)
        video_clip = video_clip.set_start(t1)
        video_clip = video_clip.set_end(t2)
        visual_clips.append(video_clip)

    audio_clips = []
    audio_file_clip = AudioFileClip(audio_file_path)
    audio_clips.append(audio_file_clip)

    for (t1, t2), text in timed_captions:
        text_clip = TextClip(txt=text,fontsize=100,color="white",stroke_width=3,stroke_color="black",method="label")
        text_clip = text_clip.set_start(t1)
        text_clip = text_clip.set_end(t2)
        text_clip = text_clip.set_position(["center",800])
        visual_clips.append(text_clip)

    video = CompositeVideoClip(visual_clips)
    if(audio_clips):
            audio = CompositeAudioClip(audio_clips)
            video.duration = audio.duration
            video.audio = audio

    video.write_videofile(OUTPUT_FILE_NAME, codec='libx264', audio_codec='aac', fps=25, preset='veryfast')
    return OUTPUT_FILE_NAME
