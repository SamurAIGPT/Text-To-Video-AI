import os
import json

CHECKPOINT_FILE = "pipeline_checkpoint.json"

class PipelineManager:
    def __init__(self, topic=None):
        self.state = {
            "current_stage": "1_script",
            "topic": topic or "",
            "script": "",
            "voiceover_path": "",
            "timed_captions": [],
            "background_music_url": "",
            "background_music_path": "",
            "background_video_urls": [],
            "video_path": ""
        }
        # If checkpoint file does not exist, write the initial state
        if not os.path.exists(CHECKPOINT_FILE):
            self.save_state()
        else:
            self.load_state()
            if topic and self.state["topic"] != topic:
                # If the user passed a new topic, reset state to clean start
                self.state["topic"] = topic
                self.state["current_stage"] = "1_script"
                self.save_state()

    def load_state(self):
        if os.path.exists(CHECKPOINT_FILE):
            try:
                with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    # Merge keys to ensure compatibility
                    for k, v in saved.items():
                        if k in self.state:
                            self.state[k] = v
                print(f"[PipelineManager] Loaded existing checkpoint. Current stage: {self.state['current_stage']}")
            except Exception as e:
                print(f"[PipelineManager] Error loading checkpoint: {e}. Starting fresh.")

    def save_state(self):
        try:
            with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
            print(f"[PipelineManager] Checkpoint saved: stage='{self.state['current_stage']}'")
        except Exception as e:
            print(f"[PipelineManager] Error saving checkpoint: {e}")

    def get_stage(self):
        return self.state["current_stage"]

    def set_stage(self, stage_name):
        self.state["current_stage"] = stage_name
        self.save_state()

    def update_data(self, key, value):
        if key in self.state:
            self.state[key] = value
            self.save_state()
        else:
            raise KeyError(f"Key '{key}' is not a valid pipeline state variable.")

    def get_data(self, key):
        return self.state.get(key)
