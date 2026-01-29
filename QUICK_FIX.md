# Quick Fix Reference

## The Errors (What Was Happening)

### Error 1: TTS Engine Failed
```
AttributeError: 'NoneType' object has no attribute 'setProperty'
```
**Why:** Linux doesn't have audio library. Code tried to configure None object.

### Error 2: Port Not Detected
```
No open ports detected, continuing to scan...
```
**Why:** App hardcoded to port 5000, but platforms set PORT environment variable.

---

## The Fixes (What Changed)

### Fix 1: Check If TTS Engine Exists
```python
# BEFORE - Crashes if tts.engine is None
tts.engine.setProperty('rate', 150)

# AFTER - Checks first
if tts and tts.engine:
    tts.engine.setProperty('rate', 150)
```

### Fix 2: Read PORT From Environment
```python
# BEFORE - Hardcoded to 5000
app.run(debug=True, host='0.0.0.0', port=5000)

# AFTER - Reads from environment
port = int(os.environ.get('PORT', 5000))
app.run(debug=False, host='0.0.0.0', port=port)
```

---

## How to Test

### Local (Windows)
```powershell
.\env\Scripts\Activate.ps1
python app.py
# Opens on http://localhost:5000
```

### Production (Render/Heroku)
Platform automatically:
1. Sets PORT environment variable
2. App reads it
3. Listens on correct port

---

## What's Fixed

| Issue | Before | After |
|-------|--------|-------|
| TTS on servers | CRASH | Gracefully skip TTS |
| Port detection | FAIL | Auto-detected |
| Debug mode | Enabled | Disabled (production) |
| Deployment | Broken | Working |

---

## Files Changed
- `app.py` - 2 key fixes added

## Status
✓ Working locally
✓ Ready for Render/Heroku
✓ No breaking changes
✓ All features preserved

---

**Deploy anytime now!**
