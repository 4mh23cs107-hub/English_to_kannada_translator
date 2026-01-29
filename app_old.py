"""
Flask Web Application for English to Kannada Translator
Full-stack web application with REST API
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from translator import EnglishKannadaTranslator
from tts_engine import TTSEngine

try:
    from speech_recognizer import SpeechRecognizer
    SPEECH_RECOGNIZER_AVAILABLE = True
except Exception as e:
    print(f"Warning: Speech recognizer not available: {e}")
    SpeechRecognizer = None
    SPEECH_RECOGNIZER_AVAILABLE = False

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
try:
    translator = EnglishKannadaTranslator()
except Exception as e:
    print(f"Warning: Translator initialization failed: {e}")
    translator = None

try:
    tts = TTSEngine()
except Exception as e:
    print(f"Warning: TTS Engine initialization failed: {e}")
    tts = None

# Configure TTS to not use GUI (if available)
if tts and tts.engine:
    tts.engine.setProperty('rate', 150)
    tts.engine.setProperty('volume', 0.9)


@app.route('/')
def landing():
    """Render the landing page"""
    return render_template('landing.html')


@app.route('/translator')
def index():
    """Render the translator page"""
    return render_template('index.html')


@app.route('/api/translate', methods=['POST'])
def api_translate():
    """
    API endpoint for text translation
    Expected JSON: {"text": "English text to translate"}
    """
    try:
        data = request.get_json()
        english_text = data.get('text', '').strip()
        
        if not english_text:
            return jsonify({'error': 'No text provided'}), 400
        
        if not translator:
            return jsonify({'error': 'Translator not initialized'}), 500
        
        # Translate the text
        kannada_text = translator.translate(english_text)
        
        if kannada_text:
            return jsonify({
                'success': True,
                'english': english_text,
                'kannada': kannada_text,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Translation failed'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/translate-batch', methods=['POST'])
def api_translate_batch():
    """
    API endpoint for batch translation
    Expected JSON: {"texts": ["text1", "text2", ...]}
    """
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts or not isinstance(texts, list):
            return jsonify({'error': 'No texts provided or invalid format'}), 400
        
        if not translator:
            return jsonify({'error': 'Translator not initialized'}), 500
        
        # Translate all texts
        results = translator.translate_batch(texts)
        
        return jsonify({
            'success': True,
            'translations': [
                {'english': eng, 'kannada': kan}
                for eng, kan in zip(texts, results)
            ],
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/speak', methods=['POST'])
def api_speak():
    """
    API endpoint for text-to-speech
    Expected JSON: {"text": "text to speak", "language": "english" or "kannada"}
    """
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        language = data.get('language', 'english').lower()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if language not in ['english', 'kannada']:
            return jsonify({'error': 'Language must be "english" or "kannada"'}), 400
        
        if not tts:
            return jsonify({
                'success': True,
                'message': 'Text-to-speech not available on this server',
                'text': text,
                'language': language
            })
        
        # Generate speech (in background, would save to file for web)
        # For now, we'll just confirm receipt
        try:
            # Try to speak (may not work in headless environment)
            tts.speak(text, language)
        except:
            pass  # Silently fail for headless environments
        
        return jsonify({
            'success': True,
            'message': 'Text-to-speech initiated',
            'text': text,
            'language': language
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'English to Kannada Translator API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/info', methods=['GET'])
def api_info():
    """Get API information"""
    return jsonify({
        'name': 'English to Kannada Translator',
        'version': '1.0.0',
        'description': 'Full-stack translator with text and speech capabilities',
        'endpoints': {
            'translate': {
                'method': 'POST',
                'path': '/api/translate',
                'params': {'text': 'English text to translate'}
            },
            'translate_batch': {
                'method': 'POST',
                'path': '/api/translate-batch',
                'params': {'texts': 'Array of English texts'}
            },
            'speak': {
                'method': 'POST',
                'path': '/api/speak',
                'params': {'text': 'Text to speak', 'language': 'english or kannada'}
            },
            'health': {
                'method': 'GET',
                'path': '/api/health'
            }
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting English to Kannada Translator Web Server...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
