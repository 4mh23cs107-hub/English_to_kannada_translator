"""
Text-to-Speech Engine for English and Kannada
Handles audio synthesis for both languages
"""

import os
import pyttsx3
from typing import Optional


class TTSEngine:
    """Text-to-Speech Engine"""
    
    def __init__(self):
        """Initialize the TTS engine"""
        self.engine = None
        self.voices = []
        self.is_headless = os.environ.get('HEADLESS', False) or not self._has_audio_hardware()
        
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume
            
            # List available voices
            self.voices = self.engine.getProperty('voices')
            self.set_voice_language('english')
        except Exception as e:
            print(f"Warning: TTS Engine initialization failed: {e}")
            self.is_headless = True
    
    def _has_audio_hardware(self):
        """Check if audio hardware is available"""
        try:
            import sounddevice
            return True
        except:
            return False
    
    def set_voice_language(self, language: str = 'english'):
        """
        Set the voice language
        
        Args:
            language: 'english' or 'kannada'
        """
        if not self.engine or not self.voices:
            return
            
        if language.lower() == 'english':
            # Try to find English voice
            for voice in self.voices:
                if 'english' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            # Default to first voice
            self.engine.setProperty('voice', self.voices[0].id)
        elif language.lower() == 'kannada':
            # Try to find Indian language voice
            for voice in self.voices:
                if 'indian' in voice.name.lower() or 'hindi' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            # Fallback to any available voice
            self.engine.setProperty('voice', self.voices[0].id)
    
    def speak(self, text: str, language: str = 'english'):
        """
        Speak the text
        
        Args:
            text: Text to speak
            language: Language of the text
        """
        if not text or not text.strip():
            return
        
        # Skip TTS on headless environments
        if self.is_headless:
            return
        
        try:
            if not self.engine:
                return
                
            self.set_voice_language(language)
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")
    
    def save_to_file(self, text: str, filename: str, language: str = 'english'):
        """
        Save speech to an audio file
        
        Args:
            text: Text to convert to speech
            filename: Output filename (should be .mp3 or .wav)
            language: Language of the text
        """
        if not text or not text.strip():
            return False
        
        try:
            self.set_voice_language(language)
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            print(f"Audio saved to: {filename}")
            return True
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False
    
    def set_speech_rate(self, rate: int):
        """
        Set the speech rate
        
        Args:
            rate: Speech rate (50-300, default 150)
        """
        rate = max(50, min(300, rate))
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """
        Set the volume
        
        Args:
            volume: Volume (0.0-1.0)
        """
        volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', volume)
    
    def list_voices(self):
        """List all available voices"""
        for i, voice in enumerate(self.voices):
            print(f"{i}: {voice.name}")


if __name__ == "__main__":
    # Test TTS
    tts = TTSEngine()
    
    print("Available voices:")
    tts.list_voices()
    
    print("\nSpeaking English text...")
    tts.speak("Hello, welcome to the English to Kannada translator!", language='english')
