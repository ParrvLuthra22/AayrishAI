"""
JARVIS AI Assistant - Voice Handler
Handles speech recognition and text-to-speech functionality
"""

import logging
import asyncio
import threading
from typing import Optional, Callable, Any
from dataclasses import dataclass

@dataclass
class VoiceCommand:
    """Voice command data"""
    text: str
    confidence: float
    timestamp: float

class VoiceHandler:
    """Handles speech recognition and text-to-speech"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("VOICE_HANDLER")
        
        self.recognizer = None
        self.microphone = None
        self.listening = False
        self.listen_thread = None
        
        self.tts_engine = None
        
        self.on_command_callback: Optional[Callable[[str], None]] = None
        self.on_listening_callback: Optional[Callable[[bool], None]] = None
        
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize speech recognition and TTS components"""
        try:
            self._initialize_speech_recognition()
            self._initialize_tts()
            self.logger.info("✅ Voice handler initialized successfully")
        except Exception as e:
            self.logger.error(f"❌ Voice handler initialization failed: {e}")
    
    def _initialize_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            import speech_recognition as sr
            
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.logger.info("✅ Speech recognition initialized")
            
        except ImportError:
            self.logger.warning("⚠️ SpeechRecognition not available - voice input disabled")
        except Exception as e:
            self.logger.error(f"❌ Speech recognition initialization failed: {e}")
    
    def _initialize_tts(self):
        """Initialize text-to-speech"""
        try:
            import pyttsx3
            
            self.tts_engine = pyttsx3.init()
            
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > 0:
                male_voice = None
                for voice in voices:
                    try:
                        if voice and hasattr(voice, 'name') and hasattr(voice, 'id') and voice.name:
                            if ('male' in voice.name.lower() or 'daniel' in voice.name.lower()):
                                male_voice = voice.id
                                break
                    except AttributeError:
                        continue
                
                if male_voice:
                    self.tts_engine.setProperty('voice', male_voice)
                else:
                    for voice in voices:
                        try:
                            if voice and hasattr(voice, 'id') and voice.id:
                                self.tts_engine.setProperty('voice', voice.id)
                                break
                        except AttributeError:
                            continue
            
            try:
                self.tts_engine.setProperty('rate', self.config.voice.speech_rate)
                self.tts_engine.setProperty('volume', self.config.voice.speech_volume)
            except Exception as prop_error:
                self.logger.warning(f"⚠️ Could not set TTS properties: {prop_error}")
            
            self.logger.info("✅ Text-to-speech initialized")
            
        except ImportError:
            self.logger.warning("⚠️ pyttsx3 not available - text-to-speech disabled")
        except Exception as e:
            self.logger.error(f"❌ TTS initialization failed: {e}")
            self.tts_engine = None
    
    def set_command_callback(self, callback: Callable[[str], None]):
        """Set callback for voice commands"""
        self.on_command_callback = callback
    
    def set_listening_callback(self, callback: Callable[[bool], None]):
        """Set callback for listening state changes"""
        self.on_listening_callback = callback
    
    def start_listening(self):
        """Start continuous voice recognition"""
        if not self.recognizer or not self.microphone:
            self.logger.warning("⚠️ Speech recognition not available")
            return
        
        if self.listening:
            self.logger.warning("⚠️ Already listening")
            return
        
        self.listening = True
        self.listen_thread = threading.Thread(target=self._listen_continuously, daemon=True)
        self.listen_thread.start()
        
        self.logger.info("🎤 Started voice recognition")
        
        if self.on_listening_callback:
            self.on_listening_callback(True)
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.listening = False
        
        if self.listen_thread:
            self.listen_thread.join(timeout=1)
        
        self.logger.info("🔇 Stopped voice recognition")
        
        if self.on_listening_callback:
            self.on_listening_callback(False)
    
    def _listen_continuously(self):
        """Continuously listen for voice commands"""
        try:
            import speech_recognition as sr
        except ImportError:
            self.logger.error("❌ SpeechRecognition not available")
            return
            
        while self.listening:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    language = "en-US"  
                    if self.config and hasattr(self.config, 'user_preferences') and self.config.user_preferences:
                        language = self.config.user_preferences.get("language", "en-US")
                    text = self.recognizer.recognize_google(audio, language=language)
                    
                    if self._contains_wake_word(text):
                        command = self._clean_command(text)
                        if command and self.on_command_callback:
                            self.logger.info(f"🎤 Voice command: {command}")
                            self.on_command_callback(command)
                    
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    self.logger.error(f"❌ Speech recognition error: {e}")
                    
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                self.logger.error(f"❌ Listening error: {e}")
                break
    
    def _contains_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        text_lower = text.lower()
        
        if not self.config or not hasattr(self.config, 'voice'):
            wake_words = ["hey jarvis", "jarvis"]  
        elif hasattr(self.config.voice, 'wake_words'):
            wake_words = [word.lower() for word in self.config.voice.wake_words]
        else:
            wake_words = [self.config.voice.wake_word.lower()]
        
        return any(wake_word in text_lower for wake_word in wake_words)
    
    def _clean_command(self, text: str) -> str:
        """Remove wake word from command"""
        text_lower = text.lower()
        
        if not self.config or not hasattr(self.config, 'voice'):
            wake_words = ["hey jarvis", "jarvis"]  
        elif hasattr(self.config.voice, 'wake_words'):
            wake_words = self.config.voice.wake_words
        else:
            wake_words = [self.config.voice.wake_word]
            
        for wake_word in wake_words:
            wake_word_lower = wake_word.lower()
            if wake_word_lower in text_lower:
                cleaned = text_lower.replace(wake_word_lower, "").strip()
                return cleaned
        
        return text.strip()
    
    async def speak(self, text: str) -> bool:
        """Speak text using TTS"""
        try:
            self.logger.info(f"🎤 Starting TTS for: '{text[:50]}...'")
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._speak_sync, text)
            
            self.logger.info(f"🔊 Completed TTS for: '{text[:50]}...'")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ TTS error: {e}")
            try:
                import subprocess
                subprocess.run(['say', text], check=True)
                self.logger.info(f"🔊 Emergency fallback TTS successful")
                return True
            except Exception as fallback_e:
                self.logger.error(f"❌ All TTS methods failed: {fallback_e}")
                return False
    
    def _speak_sync(self, text: str):
        """Synchronous TTS method"""
        try:
            self.logger.info(f"🔊 TTS: Speaking '{text[:30]}...'")
            
            import subprocess
            result = subprocess.run(['say', text], check=True, capture_output=True)
            self.logger.info(f"✅ System TTS: Successfully spoke using 'say' command")
            
        except Exception as system_error:
            self.logger.warning(f"⚠️ System 'say' failed: {system_error}, trying pyttsx3...")
            try:
                if self.tts_engine:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                    self.logger.info(f"✅ Pyttsx3 TTS: Finished speaking")
                else:
                    self.logger.error(f"❌ No TTS engine available")
            except Exception as pyttsx3_error:
                self.logger.error(f"❌ Both TTS methods failed: pyttsx3={pyttsx3_error}, system={system_error}")
    
    def speak_sync(self, text: str) -> bool:
        """Synchronous speak method"""
        if not self.tts_engine:
            return False
        
        try:
            self._speak_sync(text)
            return True
        except Exception as e:
            self.logger.error(f"❌ TTS error: {e}")
            return False
    
    def set_voice_settings(self, rate: int = None, volume: float = None):
        """Update voice settings"""
        if not self.tts_engine:
            return
        
        try:
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
                self.config.voice.speech_rate = rate
            
            if volume is not None:
                self.tts_engine.setProperty('volume', volume)
                self.config.voice.speech_volume = volume
            
            self.logger.info(f"🔧 Updated voice settings: rate={rate}, volume={volume}")
            
        except Exception as e:
            self.logger.error(f"❌ Error updating voice settings: {e}")
    
    def get_available_voices(self) -> list:
        """Get list of available TTS voices"""
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            return [(voice.id, voice.name) for voice in voices] if voices else []
        except Exception:
            return []
    
    def set_voice(self, voice_id: str) -> bool:
        """Set TTS voice by ID"""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            self.logger.info(f"🎤 Changed voice to: {voice_id}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error setting voice: {e}")
            return False
    
    def is_listening(self) -> bool:
        """Check if currently listening"""
        return self.listening
    
    def is_available(self) -> bool:
        """Check if voice functionality is available"""
        return self.recognizer is not None and self.microphone is not None
    
    def shutdown(self):
        """Shutdown voice handler"""
        self.stop_listening()
        
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
        
        self.logger.info("🔇 Voice handler shutdown complete")

class SimpleVoiceHandler:
    """Simple voice handler for basic TTS functionality"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("SIMPLE_VOICE")
        self.tts_available = False
        
        try:
            import subprocess
            result = subprocess.run(['which', 'say'], capture_output=True)
            self.tts_available = result.returncode == 0
            
            if self.tts_available:
                self.logger.info("✅ macOS TTS available")
            else:
                self.logger.info("ℹ️ No TTS available")
                
        except Exception:
            self.logger.info("ℹ️ No TTS available")
    
    async def speak(self, text: str) -> bool:
        """Simple TTS using macOS say command"""
        if not self.tts_available:
            return False
        
        try:
            import subprocess
            
            await asyncio.get_event_loop().run_in_executor(
                None, subprocess.run, ['say', text]
            )
            
            self.logger.info(f"🔊 Spoke: {text[:50]}...")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Simple TTS error: {e}")
            return False
    
    def speak_sync(self, text: str) -> bool:
        """Synchronous simple TTS"""
        if not self.tts_available:
            return False
        
        try:
            import subprocess
            subprocess.run(['say', text])
            return True
        except Exception:
            return False
    
    def start_listening(self):
        """Not implemented in simple handler"""
        pass
    
    def stop_listening(self):
        """Not implemented in simple handler"""
        pass
    
    def is_listening(self) -> bool:
        """Simple handler doesn't listen"""
        return False
    
    def is_available(self) -> bool:
        """Check if simple TTS is available"""
        return self.tts_available
    
    def shutdown(self):
        """Nothing to shutdown"""
        pass
