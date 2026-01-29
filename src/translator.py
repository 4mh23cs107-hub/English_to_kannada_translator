"""
English to Kannada Translator Module
Handles text translation using multiple translation engines
"""

import os
from typing import Optional
from dotenv import load_dotenv
import requests
import json

# Try to use Google Cloud, fallback to deep-translator
try:
    from google.cloud import translate_v2
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False

try:
    from deep_translator import GoogleTranslator
    DEEP_TRANSLATOR_AVAILABLE = True
except ImportError:
    DEEP_TRANSLATOR_AVAILABLE = False

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
            # Try Google Translate web API first
            result = self._translate_with_google_api(text)
            if result and result != text:
                return result
            
            # Try Google Cloud API
            if self.client and GOOGLE_CLOUD_AVAILABLE:
                result = self.client.translate_text(
                    text,
                    source_language=self.source_lang,
                    target_language=self.target_lang
                )
                translated = result.get('translatedText', '')
                if translated and translated != text:
                    return translated
            
            # Try deep-translator (Google Translate backend)
            if DEEP_TRANSLATOR_AVAILABLE:
                result = self._translate_with_deep_translator(text)
                if result and result != text:
                    return result
            
            return None
        except Exception as e:
            print(f"Translation error: {e}")
            # Try Google API as fallback
            try:
                return self._translate_with_google_api(text)
            except:
                pass
            return None
    
    def _translate_with_google_api(self, text: str) -> Optional[str]:
        """
        Translate using Google Translate API via requests
        Uses the unofficial Google Translate API endpoint
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text or None
        """
        try:
            # Google Translate API endpoint
            url = "https://translate.googleapis.com/translate_a/single"
            
            params = {
                'client': 'gtx',
                'sl': 'en',  # source language
                'tl': 'kn',  # target language (Kannada)
                'dt': 't',   # data type
                'q': text
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            # Response format: [[[translation_text, original_text, ...], ...], ...]
            result = response.json()
            
            if result and isinstance(result, list) and len(result) > 0:
                # Get the translations list
                if result[0] and isinstance(result[0], list) and len(result[0]) > 0:
                    translations_list = result[0][0]
                    
                    if translations_list and isinstance(translations_list, list) and len(translations_list) > 0:
                        translated_text = translations_list[0]
                        
                        if translated_text and isinstance(translated_text, str) and translated_text != text:
                            return translated_text
            
            return None
            
        except Exception as e:
            print(f"Google Translate API error: {e}")
            return None
    
    def _translate_with_deep_translator(self, text: str) -> Optional[str]:
        """
        Translate using deep-translator (Google Translate backend)
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text or None
        """
        try:
            translator = GoogleTranslator(source_language='en', target_language='kn')
            result = translator.translate(text)
            if result and result != text:
                return result
            return None
        except Exception as e:
            print(f"Deep translator error: {e}")
            return None
    
    def _fallback_simple_translate(self, text: str) -> Optional[str]:
        """
        Ultra-simple fallback when all else fails
        
        Args:
            text: Text to translate
            
        Returns:
            Placeholder translation
        """
        if text:
            return f"[Kannada translation: {text}]"
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
