import os
import time
import requests

class MuapiClient:
    def __init__(self):
        self.base_url = os.getenv("MUAPI_BASE_URL", "https://api.muapi.ai").rstrip("/")
        self.api_key = os.getenv("MUAPI_API_KEY")
        if not self.api_key:
            raise ValueError("MUAPI_API_KEY environment variable is not set in your .env file.")

    def get_headers(self):
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def trigger_suno_music(self, prompt, style, instrumental=True):
        """
        Trigger Suno music generation.
        """
        url = f"{self.base_url}/api/v1/suno-create-music"
        payload = {
            "prompt": prompt,
            "style": style,
            "custom_mode": True,
            "instrumental": instrumental,
            "model": "V5"
        }
        print(f"[MuapiClient] Requesting Suno music generation: style='{style}', prompt='{prompt}'")
        response = requests.post(url, headers=self.get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()
        request_id = data.get("request_id")
        if not request_id:
            raise ValueError(f"Failed to trigger Suno music. Response: {data}")
        return request_id

    def trigger_video_generation(self, model_name, prompt, aspect_ratio="9:16"):
        """
        Trigger video generation using specified model (e.g., veo3-fast-text-to-video).
        """
        url = f"{self.base_url}/api/v1/{model_name}"
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "resolution": "720p"
        }
        print(f"[MuapiClient] Requesting video generation ({model_name}): prompt='{prompt}', aspect_ratio='{aspect_ratio}'")
        response = requests.post(url, headers=self.get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()
        request_id = data.get("request_id")
        if not request_id:
            raise ValueError(f"Failed to trigger video generation. Response: {data}")
        return request_id

    def poll_prediction(self, request_id, interval=15, timeout=600):
        """
        Poll predictions endpoint until completed or failed.
        """
        url = f"{self.base_url}/api/v1/predictions/{request_id}/result"
        headers = self.get_headers()
        start_time = time.time()
        print(f"[MuapiClient] Polling prediction result for request {request_id}...")

        while time.time() - start_time < timeout:
            response = requests.get(url, headers=headers)
            # Prediction failed API call might return status code 400 with failure detail
            if response.status_code == 400:
                error_data = response.json()
                error_msg = error_data.get("error", "Unknown prediction error")
                raise RuntimeError(f"Prediction failed: {error_msg}")
            
            response.raise_for_status()
            data = response.json()
            status = data.get("status")

            if status == "completed":
                outputs = data.get("outputs", [])
                if not outputs:
                    raise ValueError(f"Prediction completed but returned no output URLs: {data}")
                return outputs
            elif status == "failed":
                error_msg = data.get("error", "Unknown prediction error")
                raise RuntimeError(f"Prediction failed: {error_msg}")
            
            print(f"[MuapiClient] Still processing (status: {status}). Waiting {interval} seconds...")
            time.sleep(interval)

        raise TimeoutError(f"Prediction timed out after {timeout} seconds.")
