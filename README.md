# English to Kannada Translator

A comprehensive Python application that translates English text and speech to Kannada with text-to-speech capabilities. Now available as both **Desktop GUI** and **Full-Stack Web Application**.

## 🎯 Available Versions

### 1. **Desktop Application (GUI)**
- Cross-platform tkinter interface
- [Launch with: `python main.py`]

### 2. **Web Application (Full-Stack)** ✨ NEW
- Modern responsive web interface
- REST API backend
- Browser-based text and speech processing
- [Launch with: `python app.py` or `run_web.bat`]

## ✨ Features

✅ **Text Translation**: Convert English text to Kannada  
✅ **Text-to-Speech**: Hear translations spoken aloud in Kannada  
✅ **Speech Recognition**: Capture English speech from microphone  
✅ **GUI Interface**: User-friendly tkinter interface (desktop version)  
✅ **Web Interface**: Beautiful responsive web UI (web version)  
✅ **REST API**: Multiple endpoints for programmatic access  
✅ **Batch Translation**: Translate multiple texts  
✅ **Translation History**: Track previous translations  
✅ **Multiple APIs**: Google Cloud Translation with MyMemory API fallback  

## 📂 Project Structure

```
English_to_kannada_translator/
├── app.py                          # Flask web application ⭐
├── main.py                         # Desktop GUI entry point
├── run_web.bat                     # Windows startup script
├── run_web.sh                      # Linux/macOS startup script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration
├── src/
│   ├── translator.py              # Core translation logic
│   ├── tts_engine.py              # Text-to-speech engine
│   ├── speech_recognizer.py       # Speech recognition
│   └── gui_app.py                 # Desktop GUI
├── templates/
│   └── index.html                 # Web interface
├── static/
│   ├── css/
│   │   └── style.css              # Modern styling
│   ├── js/
│   │   ├── api.js                 # API client
│   │   └── app.js                 # Frontend logic
│   └── audio/                     # Audio files
├── README.md                      # This file
├── WEB_GUIDE.md                   # Detailed web documentation
└── .git/                          # Version control
```

## 🚀 Quick Start

### Option 1: Web Version (Recommended)

**Windows**:
```bash
run_web.bat
```

**Linux/macOS**:
```bash
chmod +x run_web.sh
./run_web.sh
```

**Manual**:
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open your browser to `http://localhost:5000`

### Option 2: Desktop Version

```bash
python main.py
```

## 📦 Installation

### 1. Clone/Setup the Repository
```bash
cd English_to_kannada_translator
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Setup Google Cloud Translation

For better translation quality:

1. Create a Google Cloud project
2. Enable Cloud Translation API
3. Create service account credentials
4. Copy `.env.example` to `.env`
5. Add credentials path to `.env`

## 🌐 Web Application Usage

### Features
- Dual-panel layout (English ↔ Kannada)
- Real-time character counting
- Translation history with localStorage
- One-click copy to clipboard
- Text-to-speech for both languages
- Responsive mobile design
- Beautiful modern UI with animations

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/translate` | POST | Translate single text |
| `/api/translate-batch` | POST | Batch translate |
| `/api/speak` | POST | Text-to-speech |
| `/api/health` | GET | Health check |
| `/api/info` | GET | API information |

### Example API Usage

```bash
# Translate text
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'

# Response
{
  "success": true,
  "english": "Hello, how are you?",
  "kannada": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
  "timestamp": "2026-01-28T10:30:00.000Z"
}
```

## 💻 Desktop Application Usage

### Using the GUI Interface

1. **Text Translation**:
   - Enter English text in the left panel
   - Click "TRANSLATE" button
   - See Kannada translation in the right panel

2. **Text-to-Speech**:
   - Click "🎤 Speak" button to hear text spoken aloud

3. **Speech Recognition**:
   - Click "🎙️ Listen (Mic)" button to record English speech
   - Recognized text will appear in English panel

4. **Copy & Clear**:
   - Use "📋 Copy" to copy text to clipboard
   - Use "🗑️ Clear" to clear text fields

### Command Line Testing

```bash
# Test translator
python src/translator.py

# Test text-to-speech
python src/tts_engine.py

# Test speech recognition
python src/speech_recognizer.py
```

## 📚 Modules

### translator.py
Handles English to Kannada translation:
- `EnglishKannadaTranslator.translate(text)` - Single text
- `EnglishKannadaTranslator.translate_batch(texts)` - Multiple texts
- Google Cloud API with MyMemory fallback

### tts_engine.py
Text-to-speech functionality:
- `TTSEngine.speak(text, language)` - Speak aloud
- `TTSEngine.save_to_file(text, filename, language)` - Save to file
- Supports English and Kannada

### speech_recognizer.py
Speech recognition:
- `SpeechRecognizer.recognize_from_microphone()` - Mic input
- `SpeechRecognizer.recognize_from_file(audio_file)` - File input
- Uses Google Speech Recognition API

### gui_app.py
Desktop GUI built with tkinter:
- Dual-panel interface
- Integrated translation and speech
- Status feedback and error handling

## 🛠️ Requirements

- Python 3.8+
- Flask 2.3.3+
- Microphone (for speech features)
- Internet connection (for translation & speech)
- Modern web browser (for web version)
- Windows/Mac/Linux OS

## 📱 Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Translation | ✅ | ✅ | ✅ | ✅ |
| TTS/Speech | ✅ | ✅ | ✅ | ✅ |
| History | ✅ | ✅ | ✅ | ✅ |
| All Features | ✅ | ✅ | ✅ | ✅ |

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
SOURCE_LANGUAGE=en
TARGET_LANGUAGE=kn
FLASK_ENV=development
FLASK_DEBUG=True
```

### Server Configuration
Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🚨 Troubleshooting

### PyAudio Installation Issues

**Windows**:
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Linux**:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Server Won't Start
```bash
# Check if port 5000 is in use
# Windows: netstat -ano | findstr :5000
# Linux/Mac: lsof -i :5000

# Use different port in app.py
```

### Translation Not Working
- Verify internet connection
- Check API credentials (if using Google Cloud)
- MyMemory fallback should work without setup
- Check browser console for errors

### Speech Features Not Working
- Allow microphone access in browser settings
- Ensure microphone is connected
- Check system audio settings
- Try different browser (Chrome recommended)

## 📖 Detailed Documentation

For comprehensive guides:
- [Web Application Guide](WEB_GUIDE.md) - Full web documentation
- [API Documentation](WEB_GUIDE.md#-api-endpoints) - REST API details
- [Deployment Guide](WEB_GUIDE.md#-deployment) - Production deployment
- [Troubleshooting](WEB_GUIDE.md#-troubleshooting) - Common issues

## 🚀 Future Enhancements

- [ ] Support for more Indian languages
- [ ] Real-time translation as you type
- [ ] File upload for batch translation
- [ ] Advanced pronunciation guide
- [ ] User accounts and cloud sync
- [ ] Offline translation capability
- [ ] Mobile app (React Native)
- [ ] Database for persistent history
- [ ] Voice-to-voice translation
- [ ] Translation quality ratings

## 📊 Performance

- Translation: < 2 seconds
- TTS: Real-time with system voice
- API Response: < 1 second
- UI Responsiveness: 60 FPS

## 🔐 Security

- Input validation (frontend & backend)
- XSS prevention with HTML escaping
- CORS configuration for API
- Error handling without info leakage
- No sensitive data in logs

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit pull requests
4. Report issues

## 📞 Support

For questions or issues:
1. Check troubleshooting section
2. Review browser console
3. Check Flask logs
4. Open GitHub issue
5. Contact: [support info]

---

**Choose your interface:**
- 🖥️ **Desktop**: `python main.py` - Standalone app
- 🌐 **Web**: `python app.py` - Full-featured web version

**Happy translating! 🇬🇧 ➜ 🇮🇳**