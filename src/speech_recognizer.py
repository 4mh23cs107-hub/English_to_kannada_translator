"""
Speech Recognition Module
Handles conversion of speech to text
"""

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

from typing import Optional


class SpeechRecognizer:
    """Speech recognition class for converting audio to text"""
    
    def __init__(self):
        """Initialize the speech recognizer"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = None
            self.microphone = None
            return
            
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Warning: Speech recognizer initialization failed: {e}")
            self.recognizer = None
            self.microphone = None
    
    def recognize_from_microphone(self) -> Optional[str]:
        """
        Recognize speech from microphone
        
        Returns:
            Recognized text or None if recognition fails
        """
        if not SPEECH_RECOGNITION_AVAILABLE or not self.recognizer:
            return None
            
        try:
            with self.microphone as source:
                print("Listening... Please speak now.")
                audio = self.recognizer.listen(source, timeout=10)
            
            print("Processing audio...")
            text = self.recognizer.recognize_google(audio, language='en-US')
            print(f"Recognized: {text}")
            return text
        
        except sr.UnknownValueError:
            print("Could not understand the audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def recognize_from_file(self, audio_file: str) -> Optional[str]:
        """
        Recognize speech from an audio file
        
        Args:
            audio_file: Path to audio file (.wav, .mp3, etc.)
            
        Returns:
            Recognized text or None
        """
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text
        
        except sr.UnknownValueError:
            print("Could not understand the audio file.")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return None


if __name__ == "__main__":
    # Test speech recognition
    recognizer = SpeechRecognizer()
    text = recognizer.recognize_from_microphone()
    if text:
        print(f"You said: {text}")
