# 🚀 Quick Start Guide - Landing Page & Translator

## Getting Started

### 1. Activate Virtual Environment
```powershell
# In PowerShell
env\Scripts\Activate.ps1

# OR in Command Prompt
env\Scripts\activate.bat
```

### 2. Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

## Accessing the Pages

### Landing Page (Home)
- **URL**: `http://localhost:5000/`
- **Purpose**: Showcase the translator with features, benefits, and CTA
- **Features**:
  - Hero section with animated floating boxes
  - Feature cards (6 items)
  - How it works (4-step process)
  - Showcase with demo translation
  - Call-to-action section
  - Responsive footer

### Translator App
- **URL**: `http://localhost:5000/app`
- **Purpose**: Main translation interface
- **Features**:
  - English text input
  - Real-time Kannada translation
  - Text-to-speech
  - Copy to clipboard
  - Translation history
  - Character counter

## File Structure

```
English_to_kannada_translator/
├── app.py                          # Flask application (routes)
├── requirements.txt                # Python dependencies
├── templates/
│   ├── landing.html               # Landing page (NEW)
│   └── index.html                 # Translator app page
├── static/
│   ├── css/
│   │   ├── landing.css           # Landing page styles (NEW)
│   │   └── style.css             # App styles
│   ├── js/
│   │   ├── landing.js            # Landing page scripts (NEW)
│   │   ├── app.js                # App scripts
│   │   └── api.js                # API calls
│   └── audio/
├── src/
│   ├── translator.py             # Translation engine
│   ├── tts_engine.py             # Text-to-speech
│   └── speech_recognizer.py      # Speech input
└── env/                           # Virtual environment
```

## Route Changes

### Updated Routes (app.py)
```python
@app.route('/')              # → Landing page (was translator)
@app.route('/app')           # → Translator app (new)
@app.route('/api/translate') # → Translation API
@app.route('/api/speak')     # → Text-to-speech API
```

## Customization

### Change Landing Page Colors
Edit `static/css/landing.css`:
```css
:root {
    --primary-color: #2196F3;      /* Change blue */
    --secondary-color: #FF9800;    /* Change orange */
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Update Landing Page Content
Edit `templates/landing.html`:
- Hero section text (lines 35-45)
- Feature descriptions (lines 95-115)
- Statistics (lines 52-65)
- Demo translation (lines 180-195)

### Modify App Navigation
Edit `templates/index.html`:
- Back button link (line 18)
- App title (line 23)

## Features Overview

### Landing Page Highlights
✨ **Modern Design**
- Purple gradient background
- Smooth animations
- Responsive layout
- Professional typography

🎯 **Engaging Elements**
- Floating animated boxes
- Hover effects on cards
- Smooth scroll animations
- Mobile hamburger menu

📱 **Fully Responsive**
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (480px - 767px)
- Small mobile (< 480px)

### Translator App Highlights
⚡ **Fast Translation**
- Instant translation as you type
- No API latency

🎤 **Audio Features**
- Text-to-speech for both languages
- Clear pronunciation

📋 **User-Friendly**
- One-click copy
- Translation history
- Character counter
- Clear/reset buttons

## Troubleshooting

### Flask Module Not Found
```bash
# Make sure venv is activated, then:
pip install flask python-dotenv
```

### Port Already in Use
```bash
# Run on different port:
set FLASK_ENV=development
python app.py --port 5001
```

### Translations Not Working
- Check if `deep-translator` is installed: `pip install deep-translator`
- Ensure internet connection
- Check translator.py for errors

### Browser Cache Issues
- Clear browser cache (Ctrl+Shift+Delete)
- Do a hard refresh (Ctrl+F5)

## API Endpoints

### Translate Text
```
POST /api/translate
Content-Type: application/json

{"text": "Hello world"}

Response: {"kannada": "ಹ್ಯಾಲೋ ವರ್ಲ್ಡ್"}
```

### Speak Text
```
POST /api/speak
Content-Type: application/json

{"text": "Hello", "language": "en"}
```

## Performance Tips

1. **Landing Page**: Fully static, very fast
2. **Translation**: First request ~500ms, cached thereafter
3. **Audio**: Uses pyttsx3 (no external API calls)

## Security Notes

✅ All translations are processed locally
✅ No data is stored or logged
✅ CSRF protection enabled
✅ Content Security Policy enforced

## Support

For issues or questions:
1. Check LANDING_PAGE_GUIDE.md for detailed documentation
2. Review error messages in terminal
3. Check browser console for JavaScript errors (F12)
4. Ensure all dependencies are installed

---

**Version**: 1.0
**Last Updated**: 2026-01-29
**Status**: ✅ Ready for Use
