# Full-Stack Web Application Guide

## 🚀 Quick Start

### Windows
```bash
# Run the startup script
run_web.bat
```

### Linux/macOS
```bash
# Make the script executable
chmod +x run_web.sh

# Run the startup script
./run_web.sh
```

### Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

## 📂 Project Structure

```
English_to_kannada_translator/
├── app.py                          # Flask backend application
├── main.py                         # Desktop GUI version
├── run_web.bat                     # Windows startup script
├── run_web.sh                      # Linux/macOS startup script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration
├── src/
│   ├── translator.py              # Translation logic
│   ├── tts_engine.py              # Text-to-speech
│   ├── speech_recognizer.py       # Speech recognition
│   └── gui_app.py                 # Desktop GUI
├── templates/
│   └── index.html                 # Web interface
├── static/
│   ├── css/
│   │   └── style.css              # Styling
│   ├── js/
│   │   ├── api.js                 # API client
│   │   └── app.js                 # Frontend logic
│   └── audio/                     # Audio files (if needed)
└── README.md                      # Documentation
```

## 🌐 Web Features

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Translation**: Instant feedback while typing
- **Speech Synthesis**: Browser-based text-to-speech
- **History Tracking**: Recent translations stored in browser
- **Clipboard Integration**: Easy copy functionality

### Backend (Flask)
- **REST API**: Multiple endpoints for different operations
- **CORS Support**: Cross-origin requests enabled
- **Error Handling**: Comprehensive error management
- **Health Checks**: API status monitoring

## 📡 API Endpoints

### 1. Translate Text
```
POST /api/translate
Content-Type: application/json

{
  "text": "Hello, how are you?"
}

Response:
{
  "success": true,
  "english": "Hello, how are you?",
  "kannada": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
  "timestamp": "2026-01-28T10:30:00.000Z"
}
```

### 2. Batch Translation
```
POST /api/translate-batch
Content-Type: application/json

{
  "texts": ["Hello", "Good morning", "Thank you"]
}

Response:
{
  "success": true,
  "translations": [
    {"english": "Hello", "kannada": "ಹಲೋ"},
    {"english": "Good morning", "kannada": "ಸುಪ್ರಭಾತ"},
    {"english": "Thank you", "kannada": "ಧನ್ಯವಾದ"}
  ],
  "timestamp": "2026-01-28T10:30:00.000Z"
}
```

### 3. Text-to-Speech
```
POST /api/speak
Content-Type: application/json

{
  "text": "Hello world",
  "language": "english"
}

Response:
{
  "success": true,
  "message": "Text-to-speech initiated",
  "text": "Hello world",
  "language": "english"
}
```

### 4. Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "service": "English to Kannada Translator API",
  "version": "1.0.0",
  "timestamp": "2026-01-28T10:30:00.000Z"
}
```

### 5. API Info
```
GET /api/info

Response:
{
  "name": "English to Kannada Translator",
  "version": "1.0.0",
  "description": "Full-stack translator with text and speech capabilities",
  "endpoints": { ... }
}
```

## 🎯 Features Explained

### Translation
- Real-time translation from English to Kannada
- Uses Google Cloud Translation API (with MyMemory fallback)
- Fast and accurate translations
- Batch processing support

### Text-to-Speech
- Browser-based speech synthesis using Web Speech API
- Support for English and Kannada
- Adjustable speech rate and volume
- Automatic language detection

### Speech Recognition
- Browser-based speech recognition using Web Speech API
- Real-time transcription
- Support for English input
- Microphone access required

### Translation History
- Automatic saving of recent translations
- Stored in browser's localStorage
- Quick access to previous translations
- Click to restore previous translations

## 🔧 Configuration

### Environment Setup
Create a `.env` file:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
SOURCE_LANGUAGE=en
TARGET_LANGUAGE=kn
FLASK_ENV=development
FLASK_DEBUG=True
```

### Server Configuration
To run on a different host/port:
```python
# Edit app.py
app.run(debug=True, host='0.0.0.0', port=8000)
```

## 🌐 Accessing the Application

Once the server is running:

1. **Web Interface**: Open browser and navigate to `http://localhost:5000`
2. **API Docs**: Check available endpoints at `http://localhost:5000/api/info`
3. **Health Check**: Monitor API at `http://localhost:5000/api/health`

## 💻 Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Web Speech API | ✅ | ✅ | ✅ | ✅ |
| Translation | ✅ | ✅ | ✅ | ✅ |
| TTS | ✅ | ✅ | ✅ | ✅ |
| History | ✅ | ✅ | ✅ | ✅ |

## 📱 Responsive Breakpoints

- **Desktop**: 1200px+
- **Tablet**: 768px - 1024px
- **Mobile**: Below 768px

## 🔐 Security

- Input validation on both frontend and backend
- XSS prevention through HTML escaping
- CORS configuration for API access
- Error handling without exposing sensitive info

## 📊 Performance Tips

1. **Caching**: Browser caches static assets
2. **Lazy Loading**: History items load on demand
3. **Compression**: Enable gzip on production server
4. **CDN**: Consider using CDN for static files
5. **API Rate Limiting**: Implement on production

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port 5000 is in use
# Windows: netstat -ano | findstr :5000
# Linux/Mac: lsof -i :5000

# Use different port
python -c "app.run(port=8000)"
```

### Translation Not Working
- Check internet connection
- Verify API credentials (if using Google Cloud)
- Check browser console for errors
- Restart the server

### Speech Recognition Not Working
- Allow microphone access in browser
- Check browser permissions
- Ensure microphone is connected
- Try a different browser

### UI Not Loading
- Clear browser cache (Ctrl+Shift+Delete)
- Check if static files are in correct location
- Verify Flask is serving static files
- Check browser console for 404 errors

## 🚀 Deployment

### Heroku
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### AWS/GCP/Azure
Follow respective cloud platform guides for Flask deployment.

## 📝 Future Enhancements

- [ ] User authentication and accounts
- [ ] Translation history database
- [ ] Multiple language support
- [ ] Document upload for translation
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)
- [ ] Voice-to-voice translation
- [ ] Offline support (service workers)
- [ ] Advanced pronunciation guide
- [ ] Translation quality ratings

## 📞 Support

For issues or feature requests:
1. Check the troubleshooting section
2. Review Flask and browser console logs
3. Open an issue in the repository
4. Contact support

## 📄 License

This project is open source and available for educational purposes.

---

**Happy translating! 🇬🇧 ➜ 🇮🇳**
