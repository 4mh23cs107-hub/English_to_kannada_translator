/**
 * Main Application Logic
 */

class TranslatorApp {
    constructor() {
        this.initElements();
        this.initEventListeners();
        this.initSpeechRecognition();
        this.translationHistory = [];
    }

    /**
     * Initialize DOM elements
     */
    initElements() {
        this.elements = {
            englishText: document.getElementById('englishText'),
            kannadaText: document.getElementById('kannadaText'),
            translateBtn: document.getElementById('translateBtn'),
            translationLoader: document.getElementById('translationLoader'),
            statusMessage: document.getElementById('statusMessage'),
            speakEnglish: document.getElementById('speakEnglish'),
            speakKannada: document.getElementById('speakKannada'),
            clearEnglish: document.getElementById('clearEnglish'),
            clearKannada: document.getElementById('clearKannada'),
            copyEnglish: document.getElementById('copyEnglish'),
            copyKannada: document.getElementById('copyKannada'),
            englishCount: document.getElementById('englishCount'),
            kannadaCount: document.getElementById('kannadaCount'),
            translationHistory: document.getElementById('translationHistory')
        };
    }

    /**
     * Initialize event listeners
     */
    initEventListeners() {
        // Translation
        this.elements.translateBtn.addEventListener('click', () => this.translate());
        
        // English panel
        this.elements.speakEnglish.addEventListener('click', () => this.speak(this.elements.englishText.value, 'english'));
        this.elements.clearEnglish.addEventListener('click', () => this.clearText('english'));
        this.elements.copyEnglish.addEventListener('click', () => this.copyToClipboard(this.elements.englishText.value, 'English'));
        this.elements.englishText.addEventListener('input', () => this.updateCharCount('english'));

        // Kannada panel
        this.elements.speakKannada.addEventListener('click', () => this.speak(this.elements.kannadaText.value, 'kannada'));
        this.elements.clearKannada.addEventListener('click', () => this.clearText('kannada'));
        this.elements.copyKannada.addEventListener('click', () => this.copyToClipboard(this.elements.kannadaText.value, 'Kannada'));
        this.elements.kannadaText.addEventListener('input', () => this.updateCharCount('kannada'));

        // Enter key to translate
        this.elements.englishText.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.translate();
            }
        });

        // Load translation history on startup
        this.loadTranslationHistory();
    }

    /**
     * Initialize Web Speech API
     */
    initSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.speechRecognition = SpeechRecognition ? new SpeechRecognition() : null;

        if (this.speechRecognition) {
            this.speechRecognition.lang = 'en-US';
            this.speechRecognition.continuous = false;
            this.speechRecognition.interimResults = false;

            this.speechRecognition.onstart = () => {
                this.showStatus('Listening...', 'info');
            };

            this.speechRecognition.onend = () => {
                this.showStatus('Listening stopped', 'info');
            };

            this.speechRecognition.onerror = (event) => {
                this.showStatus(`Speech error: ${event.error}`, 'error');
            };

            this.speechRecognition.onresult = (event) => {
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        this.elements.englishText.value += transcript + ' ';
                        this.updateCharCount('english');
                    } else {
                        interimTranscript += transcript;
                    }
                }
            };
        }
    }

    /**
     * Translate English text to Kannada
     */
    async translate() {
        const text = this.elements.englishText.value.trim();

        if (!text) {
            this.showStatus('Please enter English text to translate', 'error');
            return;
        }

        try {
            this.setLoadingState(true);
            const result = await api.translate(text);

            if (result.success) {
                this.elements.kannadaText.value = result.kannada;
                this.updateCharCount('kannada');
                this.showStatus('Translation successful!', 'success');
                
                // Add to history
                this.addToHistory(result.english, result.kannada);
            } else {
                this.showStatus('Translation failed', 'error');
            }
        } catch (error) {
            this.showStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoadingState(false);
        }
    }

    /**
     * Speak text using Web Speech API
     */
    speak(text, language = 'english') {
        if (!text.trim()) {
            this.showStatus('No text to speak', 'error');
            return;
        }

        const synth = window.speechSynthesis;
        
        // Cancel any ongoing speech
        synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = language === 'english' ? 'en-US' : 'kn-IN';
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        utterance.onstart = () => {
            this.showStatus(`Speaking ${language}...`, 'info');
        };

        utterance.onend = () => {
            this.showStatus('Speech completed', 'success');
        };

        utterance.onerror = (event) => {
            this.showStatus(`Speech error: ${event.error}`, 'error');
        };

        synth.speak(utterance);

        // Also notify backend (optional)
        api.speak(text, language).catch(() => {});
    }

    /**
     * Clear text area
     */
    clearText(panel) {
        if (panel === 'english') {
            this.elements.englishText.value = '';
        } else {
            this.elements.kannadaText.value = '';
        }
        this.updateCharCount(panel);
    }

    /**
     * Copy text to clipboard
     */
    async copyToClipboard(text, label) {
        if (!text.trim()) {
            this.showStatus(`No ${label} text to copy`, 'error');
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            this.showStatus(`${label} text copied!`, 'success');
        } catch (error) {
            this.showStatus('Failed to copy text', 'error');
        }
    }

    /**
     * Update character count
     */
    updateCharCount(panel) {
        const textArea = panel === 'english' ? this.elements.englishText : this.elements.kannadaText;
        const countElement = panel === 'english' ? this.elements.englishCount : this.elements.kannadaCount;
        const count = textArea.value.length;
        countElement.textContent = `${count} character${count !== 1 ? 's' : ''}`;
    }

    /**
     * Show status message
     */
    showStatus(message, type = 'info') {
        const statusEl = this.elements.statusMessage;
        statusEl.textContent = message;
        statusEl.className = `status-message ${type}`;
        statusEl.style.display = 'block';

        // Auto-hide after 5 seconds
        setTimeout(() => {
            statusEl.style.display = 'none';
        }, 5000);
    }

    /**
     * Set loading state
     */
    setLoadingState(loading) {
        this.elements.translateBtn.disabled = loading;
        this.elements.translationLoader.style.display = loading ? 'flex' : 'none';
    }

    /**
     * Add translation to history
     */
    addToHistory(english, kannada) {
        const entry = {
            english,
            kannada,
            timestamp: new Date()
        };

        this.translationHistory.unshift(entry);
        
        // Keep only last 10 translations
        if (this.translationHistory.length > 10) {
            this.translationHistory.pop();
        }

        // Save to localStorage
        this.saveTranslationHistory();
        this.renderHistory();
    }

    /**
     * Render translation history
     */
    renderHistory() {
        const container = this.elements.translationHistory;

        if (this.translationHistory.length === 0) {
            container.innerHTML = '<p class="empty-message">No translations yet. Start typing to see history!</p>';
            return;
        }

        container.innerHTML = this.translationHistory.map((entry, index) => `
            <div class="history-item" onclick="app.restoreFromHistory(${index})">
                <div class="history-item-text">
                    <span class="history-en">${this.escapeHTML(entry.english)}</span>
                </div>
                <div class="history-item-text">
                    <span class="history-kn">→ ${this.escapeHTML(entry.kannada)}</span>
                </div>
                <div class="history-time">${entry.timestamp.toLocaleTimeString()}</div>
            </div>
        `).join('');
    }

    /**
     * Restore translation from history
     */
    restoreFromHistory(index) {
        const entry = this.translationHistory[index];
        this.elements.englishText.value = entry.english;
        this.elements.kannadaText.value = entry.kannada;
        this.updateCharCount('english');
        this.updateCharCount('kannada');
        this.showStatus('Restored from history', 'info');
    }

    /**
     * Save history to localStorage
     */
    saveTranslationHistory() {
        const data = this.translationHistory.map(entry => ({
            english: entry.english,
            kannada: entry.kannada,
            timestamp: entry.timestamp.toISOString()
        }));
        localStorage.setItem('translationHistory', JSON.stringify(data));
    }

    /**
     * Load history from localStorage
     */
    loadTranslationHistory() {
        try {
            const data = localStorage.getItem('translationHistory');
            if (data) {
                this.translationHistory = JSON.parse(data).map(entry => ({
                    ...entry,
                    timestamp: new Date(entry.timestamp)
                }));
                this.renderHistory();
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    /**
     * Escape HTML special characters
     */
    escapeHTML(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TranslatorApp();
    console.log('Translator app initialized');
});
