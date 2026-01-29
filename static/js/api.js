/**
 * API Module - Handles all API calls to the backend
 */

class TranslatorAPI {
    constructor(baseURL = '') {
        this.baseURL = baseURL || window.location.origin;
        this.timeout = 15000; // 15 second timeout
    }

    /**
     * Make a fetch request with timeout
     */
    async request(endpoint, options = {}) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        try {
            const url = `${this.baseURL}${endpoint}`;
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            throw error;
        } finally {
            clearTimeout(timeoutId);
        }
    }

    /**
     * Translate text from English to Kannada
     */
    async translate(text) {
        return this.request('/api/translate', {
            method: 'POST',
            body: JSON.stringify({ text })
        });
    }

    /**
     * Translate multiple texts (batch)
     */
    async translateBatch(texts) {
        return this.request('/api/translate-batch', {
            method: 'POST',
            body: JSON.stringify({ texts })
        });
    }

    /**
     * Text-to-speech
     */
    async speak(text, language = 'english') {
        return this.request('/api/speak', {
            method: 'POST',
            body: JSON.stringify({ text, language })
        });
    }

    /**
     * Health check
     */
    async healthCheck() {
        return this.request('/api/health');
    }

    /**
     * Get API info
     */
    async getInfo() {
        return this.request('/api/info');
    }
}

// Create global API instance
const api = new TranslatorAPI();
