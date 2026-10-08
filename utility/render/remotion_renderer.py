import os
import json
import shutil
import subprocess
import sys

def find_command(*names):
    for name in names:
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None

def render_with_remotion(audio_file_path, timed_captions, background_video_data, background_music_path=None):
    """
    Renders video using React / Remotion composition.
    
    Args:
        audio_file_path (str): Path to voiceover narration audio.
        timed_captions (list): Whisper timed captions list in format [((start, end), word), ...]
        background_video_data (list): B-roll segments in format [[(start, end), video_url], ...]
        background_music_path (str, optional): Path to background music track.
    
    Returns:
        str: Path to the compiled video output file.
    """
    # 1. Resolve workspace directories
    utility_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace_dir = os.path.dirname(utility_dir)
    composer_dir = os.path.join(workspace_dir, "remotion-composer")
    
    if not os.path.exists(composer_dir):
        raise FileNotFoundError(f"Remotion composer directory not found at: {composer_dir}")

    # 2. Check for Node.js, npm, npx requirements
    node_cmd = find_command("node", "node.exe")
    if not node_cmd:
        raise RuntimeError("Node.js is required to render via Remotion, but was not found on PATH. Install it from https://nodejs.org/")
        
    npm_cmd = find_command("npm.cmd", "npm", "npm.exe")
    npx_cmd = find_command("npx.cmd", "npx", "npx.exe")
    if not npm_cmd or not npx_cmd:
        raise RuntimeError("npm and npx are required but were not found on PATH.")

    # 3. Ensure npm packages are installed in remotion-composer
    node_modules_dir = os.path.join(composer_dir, "node_modules")
    if not os.path.exists(node_modules_dir):
        print("[RemotionRenderer] Installing npm dependencies in remotion-composer...")
        subprocess.run([npm_cmd, "install"], cwd=composer_dir, check=True)

    # Ensure public folder exists
    public_dir = os.path.join(composer_dir, "public")
    os.makedirs(public_dir, exist_ok=True)

    def prepare_local_file(src_path):
        if not src_path:
            return None
        # If it's a URL, return as-is
        if src_path.startswith("http://") or src_path.startswith("https://"):
            return src_path
        # Otherwise, check if it's a local file
        if os.path.exists(src_path):
            basename = os.path.basename(src_path)
            dest_path = os.path.join(public_dir, basename)
            if not os.path.exists(dest_path) or os.path.abspath(src_path) != os.path.abspath(dest_path):
                print(f"[RemotionRenderer] Copying local asset to public folder: {src_path} -> {dest_path}")
                shutil.copy2(src_path, dest_path)
            return basename
        return src_path

    # 4. Map timed captions to Remotion WordCaption schema
    captions_list = []
    if timed_captions:
        for (t1, t2), word in timed_captions:
            captions_list.append({
                "word": word,
                "startMs": int(t1 * 1000),
                "endMs": int(t2 * 1000)
            })

    # 5. Map B-roll videos to Remotion Cut schema
    cuts_list = []
    for i, ((t1, t2), source) in enumerate(background_video_data):
        resolved_source = prepare_local_file(source)
        cuts_list.append({
            "id": f"clip_{i}",
            "source": resolved_source,
            "in_seconds": float(t1),
            "out_seconds": float(t2),
            "source_in_seconds": 0.0
        })

    # 6. Map audio config
    resolved_audio = prepare_local_file(audio_file_path)
    audio_config = {
        "narration": {
            "src": resolved_audio,
            "volume": 1.0
        }
    }
    
    if background_music_path:
        resolved_music = prepare_local_file(background_music_path)
        if resolved_music:
            audio_config["music"] = {
                "src": resolved_music,
                "volume": 0.12,
                "fadeInSeconds": 2.0,
                "fadeOutSeconds": 3.0,
                "offsetSeconds": 0.0,
                "loop": True
            }

    # 7. Package props payload
    props = {
        "cuts": cuts_list,
        "captions": captions_list,
        "audio": audio_config,
        "theme": os.getenv("REMOTION_THEME", "flat-motion-graphics")
    }

    # Write props to public/props.json in remotion-composer
    public_dir = os.path.join(composer_dir, "public")
    os.makedirs(public_dir, exist_ok=True)
    props_file_path = os.path.join(public_dir, "props.json")
    
    print(f"[RemotionRenderer] Writing composition props to {props_file_path}...")
    with open(props_file_path, "w", encoding="utf-8") as f:
        json.dump(props, f, indent=2)

    # 8. Render via Remotion CLI
    out_dir = os.path.join(composer_dir, "out")
    os.makedirs(out_dir, exist_ok=True)
    composer_output_path = os.path.join(out_dir, "video.mp4")
    
    # Clean up old render if exists
    if os.path.exists(composer_output_path):
        try:
            os.remove(composer_output_path)
        except Exception as e:
            print(f"[RemotionRenderer] Warning: Could not remove old render file: {e}")

    print("[RemotionRenderer] Starting Remotion render process...")
    cmd = [
        npx_cmd,
        "remotion",
        "render",
        "src/index.tsx",
        "Explainer",
        composer_output_path,
        "--props",
        "public/props.json",
        "--codec",
        "h264"
    ]
    
    subprocess.run(cmd, cwd=composer_dir, check=True)

    # 9. Copy rendered output back to Text-To-Video-AI root directory
    final_output_path = os.path.join(workspace_dir, "rendered_video.mp4")
    
    if os.path.exists(composer_output_path):
        print(f"[RemotionRenderer] Copying rendered video to: {final_output_path}")
        shutil.copy2(composer_output_path, final_output_path)
        return final_output_path
    else:
        raise RuntimeError(f"Remotion render finished, but output file not found at: {composer_output_path}")
