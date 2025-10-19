"""
JARVIS AI Assistant - Configuration Manager
Handles all configuration settings, API keys, and user preferences
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
load_dotenv()

@dataclass
class VoiceConfig:
    """Voice configuration settings"""
    wake_word: str = "Hey Jarvis"
    voice_id: str = "com.apple.speech.synthesis.voice.Alex"
    speech_rate: int = 200
    speech_volume: float = 0.9
    use_elevenlabs: bool = False
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"

@dataclass
class UIConfig:
    """UI configuration settings"""
    theme: str = "dark_neon"
    primary_color: str = "#00BFFF"
    secondary_color: str = "#0080FF"
    background_color: str = "#0A0A0A"
    text_color: str = "#FFFFFF"
    accent_color: str = "#FFD700"
    window_opacity: float = 0.95
    animations_enabled: bool = True
    voice_waveform: bool = True

@dataclass
class AIConfig:
    """AI model configuration"""
    primary_model: str = "groq"
    groq_model: str = "llama-3.1-8b-instant"
    openai_model: str = "gpt-4"
    claude_model: str = "claude-3-sonnet-20240229"
    gemini_model: str = "gemini-pro"
    temperature: float = 0.7
    max_tokens: int = 500
    conversation_memory: int = 10

@dataclass
class SystemConfig:
    """System integration settings"""
    notifications_enabled: bool = True
    system_monitoring: bool = True
    auto_startup: bool = False
    log_level: str = "INFO"
    data_retention_days: int = 30

class ConfigManager:
    """Manages all configuration for JARVIS"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / "jarvis_config.json"
        self.voice = VoiceConfig()
        self.ui = UIConfig()
        self.ai = AIConfig()
        self.system = SystemConfig()
        
        self.api_keys = {
            "groq": os.getenv("GROQ_API_KEY", "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"),
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
            "google": os.getenv("GOOGLE_API_KEY", ""),
            "elevenlabs": os.getenv("ELEVENLABS_API_KEY", ""),
            "tavily": os.getenv("TAVILY_API_KEY", "")
        }
        
        self.user_preferences = {
            "name": "Mr. Luthra",
            "timezone": "America/Los_Angeles",
            "language": "en-US",
            "units": "metric"
        }
        
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                if "voice" in config_data:
                    self.voice = VoiceConfig(**config_data["voice"])
                if "ui" in config_data:
                    self.ui = UIConfig(**config_data["ui"])
                if "ai" in config_data:
                    self.ai = AIConfig(**config_data["ai"])
                if "system" in config_data:
                    self.system = SystemConfig(**config_data["system"])
                if "user_preferences" in config_data:
                    self.user_preferences.update(config_data["user_preferences"])
                    
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self) -> None:
        """Save configuration to file"""
        config_data = {
            "voice": asdict(self.voice),
            "ui": asdict(self.ui),
            "ai": asdict(self.ai),
            "system": asdict(self.system),
            "user_preferences": self.user_preferences
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        return self.api_keys.get(service.lower())
    
    def update_user_preference(self, key: str, value: Any) -> None:
        """Update user preference"""
        self.user_preferences[key] = value
        self.save_config()
    
    def get_user_name(self) -> str:
        """Get user's name"""
        return self.user_preferences.get("name", "User")
    
    def reset_to_defaults(self) -> None:
        """Reset all configurations to defaults"""
        self.voice = VoiceConfig()
        self.ui = UIConfig()
        self.ai = AIConfig()
        self.system = SystemConfig()
        self.save_config()

config_manager = ConfigManager()
