import os
from dotenv import load_dotenv
from typing import Optional, Literal
from openai import OpenAI

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class ConfigurationError(Exception):
    pass


class Config:
    _instance: Optional['Config'] = None
    
    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        load_dotenv()
        
        self._validate_env_file()
        self._validate_configuration()
        
        self._llm_client = None
        self._initialized = True
    
    def _validate_env_file(self) -> None:
        env_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(env_path):
            raise ConfigurationError(
                ".env file not found. Please create a .env file based on .env.example\n"
                f"Expected location: {env_path}"
            )
    
    def _validate_configuration(self) -> None:
        errors = []
        
        llm_provider = os.getenv('LLM_PROVIDER', '').lower()
        if llm_provider not in ['openai', 'groq', 'gemini']:
            errors.append(
                f"Invalid LLM_PROVIDER: '{llm_provider}'. Must be one of: openai, groq, gemini"
            )
        
        if llm_provider == 'openai':
            if not os.getenv('OPENAI_API_KEY'):
                errors.append("Missing required API key: OPENAI_API_KEY (required for LLM_PROVIDER=openai)")
            if not os.getenv('OPENAI_MODEL'):
                errors.append("Missing required configuration: OPENAI_MODEL (required for LLM_PROVIDER=openai)")
        
        elif llm_provider == 'groq':
            if not os.getenv('GROQ_API_KEY'):
                errors.append("Missing required API key: GROQ_API_KEY (required for LLM_PROVIDER=groq)")
            if not os.getenv('GROQ_MODEL'):
                errors.append("Missing required configuration: GROQ_MODEL (required for LLM_PROVIDER=groq)")
        
        elif llm_provider == 'gemini':
            if not os.getenv('GEMINI_API_KEY'):
                errors.append("Missing required API key: GEMINI_API_KEY (required for LLM_PROVIDER=gemini)")
            if not os.getenv('GEMINI_MODEL'):
                errors.append("Missing required configuration: GEMINI_MODEL (required for LLM_PROVIDER=gemini)")
        
        if not os.getenv('PEXELS_API_KEY'):
            errors.append("Missing required API key: PEXELS_API_KEY (always required)")
        
        stt_provider = os.getenv('STT_PROVIDER', '').lower()
        if stt_provider not in ['whisper', 'deepgram']:
            errors.append(
                f"Invalid STT_PROVIDER: '{stt_provider}'. Must be one of: whisper, deepgram"
            )
        elif stt_provider == 'deepgram':
            if not os.getenv('DEEPGRAM_API_KEY'):
                errors.append("Missing required API key: DEEPGRAM_API_KEY (required for STT_PROVIDER=deepgram)")
        
        tts_provider = os.getenv('TTS_PROVIDER', '').lower()
        if tts_provider not in ['edgetts', 'elevenlabs']:
            errors.append(
                f"Invalid TTS_PROVIDER: '{tts_provider}'. Must be one of: edgetts, elevenlabs"
            )
        elif tts_provider == 'edgetts':
            if not os.getenv('EDGETTS_VOICE'):
                errors.append("Missing required configuration: EDGETTS_VOICE (required for TTS_PROVIDER=edgetts)")
        elif tts_provider == 'elevenlabs':
            if not os.getenv('ELEVENLABS_API_KEY'):
                errors.append("Missing required API key: ELEVENLABS_API_KEY (required for TTS_PROVIDER=elevenlabs)")
            if not os.getenv('ELEVENLABS_VOICE_ID'):
                errors.append("Missing required configuration: ELEVENLABS_VOICE_ID (required for TTS_PROVIDER=elevenlabs)")
        
        if errors:
            error_message = "Configuration validation failed:\n\n"
            for error in errors:
                error_message += f"  - {error}\n"
            error_message += "\nPlease check your .env file and ensure all required keys are set."
            raise ConfigurationError(error_message)
    
    def get_llm_provider(self) -> Literal['openai', 'groq', 'gemini']:
        return os.getenv('LLM_PROVIDER', '').lower()
    
    def get_llm_model(self) -> str:
        provider = self.get_llm_provider()
        if provider == 'openai':
            return os.getenv('OPENAI_MODEL', 'gpt-4o')
        elif provider == 'groq':
            return os.getenv('GROQ_MODEL', 'llama3-70b-8192')
        elif provider == 'gemini':
            return os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        raise ConfigurationError(f"Unknown LLM provider: {provider}")
    
    def get_llm_client(self):
        if self._llm_client is not None:
            return self._llm_client
        
        provider = self.get_llm_provider()
        
        if provider == 'openai':
            self._llm_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        elif provider == 'groq':
            if not GROQ_AVAILABLE:
                raise ConfigurationError("Groq library not installed. Run: pip install groq")
            self._llm_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        elif provider == 'gemini':
            if not GEMINI_AVAILABLE:
                raise ConfigurationError("Gemini library not installed. Run: pip install google-generativeai")
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
            self._llm_client = genai.GenerativeModel(model_name)
        
        return self._llm_client
    
    def get_stt_provider(self) -> Literal['whisper', 'deepgram']:
        return os.getenv('STT_PROVIDER', 'whisper').lower()
    
    def get_tts_provider(self) -> Literal['edgetts', 'elevenlabs']:
        return os.getenv('TTS_PROVIDER', 'edgetts').lower()
    
    def get_tts_voice(self) -> str:
        provider = self.get_tts_provider()
        if provider == 'edgetts':
            return os.getenv('EDGETTS_VOICE', 'en-AU-WilliamNeural')
        elif provider == 'elevenlabs':
            return os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
        raise ConfigurationError(f"Unknown TTS provider: {provider}")
    
    def get_pexels_api_key(self) -> str:
        key = os.getenv('PEXELS_API_KEY')
        if not key:
            raise ConfigurationError("PEXELS_API_KEY not found in .env file")
        return key
    
    def get_video_orientation(self) -> bool:
        """
        Returns True for landscape (horizontal) or False for portrait (vertical)
        Portrait (vertical, 1080x1920) is recommended for mobile platforms
        Landscape (horizontal, 1920x1080) is for traditional video
        """
        orientation = os.getenv('VIDEO_ORIENTATION', 'portrait').lower()
        if orientation not in ['portrait', 'landscape']:
            raise ConfigurationError(
                f"Invalid VIDEO_ORIENTATION: '{orientation}'. Must be 'portrait' or 'landscape'"
            )
        return orientation == 'landscape'

    def get_deepgram_api_key(self) -> str:
        key = os.getenv('DEEPGRAM_API_KEY')
        if not key:
            raise ConfigurationError("DEEPGRAM_API_KEY not found in .env file")
        return key
    
    def get_elevenlabs_api_key(self) -> str:
        key = os.getenv('ELEVENLABS_API_KEY')
        if not key:
            raise ConfigurationError("ELEVENLABS_API_KEY not found in .env file")
        return key


def get_config() -> Config:
    try:
        return Config()
    except ConfigurationError as e:
        print(f"\n{'='*70}")
        print("ERROR: Configuration Failed")
        print('='*70)
        print(f"\n{str(e)}\n")
        print("Please fix these issues and try again.")
        print('='*70 + '\n')
        raise
