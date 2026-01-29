"""
English to Kannada Translator Module
Handles text translation using Google Cloud Translation API
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Try to use Google Cloud, fallback to simple API
try:
    from google.cloud import translate_v2
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    import requests

load_dotenv()


class EnglishKannadaTranslator:
    """Translator class for English to Kannada translation"""
    
    def __init__(self):
        """Initialize the translator"""
        self.source_lang = "en"
        self.target_lang = "kn"
        self.client = None
        
        if GOOGLE_CLOUD_AVAILABLE:
            try:
                credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
                if credentials_path:
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
                self.client = translate_v2.Client()
            except Exception as e:
                print(f"Warning: Google Cloud not initialized. Using fallback. Error: {e}")
                self.client = None
    
    def translate(self, text: str) -> Optional[str]:
        """
        Translate English text to Kannada
        
        Args:
            text: English text to translate
            
        Returns:
            Translated Kannada text or None if translation fails
        """
        if not text or not text.strip():
            return ""
        
        try:
            if self.client and GOOGLE_CLOUD_AVAILABLE:
                result = self.client.translate_text(
                    text,
                    source_language=self.source_lang,
                    target_language=self.target_lang
                )
                return result['translatedText']
            else:
                # Fallback: Use MyMemory API (free, no authentication needed)
                return self._translate_with_mymemory(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def _translate_with_mymemory(self, text: str) -> Optional[str]:
        """
        Fallback translation using MyMemory API
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text or None
        """
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': f'{self.source_lang}|{self.target_lang}'
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data['responseStatus'] == 200:
                return data['responseData']['translatedText']
            else:
                print(f"MyMemory API error: {data.get('responseDetails', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"MyMemory translation error: {e}")
            return None
    
    def translate_batch(self, texts: list) -> list:
        """
        Translate multiple texts
        
        Args:
            texts: List of English texts
            
        Returns:
            List of translated texts
        """
        return [self.translate(text) for text in texts]


if __name__ == "__main__":
    # Test the translator
    translator = EnglishKannadaTranslator()
    
    test_texts = [
        "Hello, how are you?",
        "Welcome to Python",
        "Machine translation is amazing!"
    ]
    
    print("English to Kannada Translation Test")
    print("=" * 50)
    for text in test_texts:
        translated = translator.translate(text)
        print(f"EN: {text}")
        print(f"KN: {translated}")
        print("-" * 50)
