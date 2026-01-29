"""
GUI Application for English to Kannada Translator
Built with tkinter for cross-platform compatibility
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from translator import EnglishKannadaTranslator
from tts_engine import TTSEngine
from speech_recognizer import SpeechRecognizer


class TranslatorGUI:
    """GUI Application for the translator"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("English to Kannada Translator")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.translator = EnglishKannadaTranslator()
        self.tts = TTSEngine()
        self.recognizer = SpeechRecognizer()
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Header
        header = tk.Label(
            self.root,
            text="English to Kannada Translator",
            font=("Arial", 18, "bold"),
            bg='#2196F3',
            fg='white',
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # English text section
        self.create_text_section(main_frame, "English (Source)", 0, 'english')
        
        # Button section
        self.create_button_section(main_frame)
        
        # Kannada text section
        self.create_text_section(main_frame, "Kannada (Translation)", 2, 'kannada')
    
    def create_text_section(self, parent, label, row, section_type):
        """Create a text input/output section"""
        
        # Label
        label_widget = ttk.Label(parent, text=label, font=("Arial", 12, "bold"))
        label_widget.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # Text widget
        text_widget = scrolledtext.ScrolledText(
            parent,
            height=10,
            width=40,
            font=("Arial", 11),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            borderwidth=2
        )
        text_widget.grid(row=row+1, column=0, columnspan=2, sticky=tk.NSEW, pady=5)
        
        # Store reference
        if section_type == 'english':
            self.english_text = text_widget
        else:
            self.kannada_text = text_widget
        
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row+2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        if section_type == 'english':
            # English buttons
            ttk.Button(
                button_frame,
                text="🎤 Speak",
                command=lambda: self.speak_text(self.english_text.get("1.0", tk.END), 'english')
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                button_frame,
                text="🎙️ Listen (Mic)",
                command=self.listen_from_mic
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                button_frame,
                text="🗑️ Clear",
                command=lambda: self.english_text.delete("1.0", tk.END)
            ).pack(side=tk.LEFT, padx=5)
        else:
            # Kannada buttons
            ttk.Button(
                button_frame,
                text="🎤 Speak",
                command=lambda: self.speak_text(self.kannada_text.get("1.0", tk.END), 'kannada')
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                button_frame,
                text="📋 Copy",
                command=self.copy_to_clipboard
            ).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(
                button_frame,
                text="🗑️ Clear",
                command=lambda: self.kannada_text.delete("1.0", tk.END)
            ).pack(side=tk.LEFT, padx=5)
    
    def create_button_section(self, parent):
        """Create the translation button section"""
        
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        
        # Translate button
        translate_btn = ttk.Button(
            button_frame,
            text="⬇️ TRANSLATE ⬇️",
            command=self.translate,
            width=30
        )
        translate_btn.pack()
        
        # Status label
        self.status_label = ttk.Label(
            button_frame,
            text="Ready",
            foreground="green"
        )
        self.status_label.pack(pady=5)
    
    def translate(self):
        """Translate English text to Kannada"""
        english_text = self.english_text.get("1.0", tk.END).strip()
        
        if not english_text:
            messagebox.showwarning("Input Error", "Please enter English text to translate.")
            return
        
        # Update status
        self.status_label.config(text="Translating...", foreground="blue")
        self.root.update()
        
        # Run translation in a separate thread to avoid freezing GUI
        thread = threading.Thread(target=self._translate_thread, args=(english_text,))
        thread.daemon = True
        thread.start()
    
    def _translate_thread(self, text):
        """Run translation in background thread"""
        try:
            translated = self.translator.translate(text)
            
            if translated:
                self.kannada_text.delete("1.0", tk.END)
                self.kannada_text.insert("1.0", translated)
                self.status_label.config(text="Translation complete!", foreground="green")
            else:
                self.status_label.config(text="Translation failed!", foreground="red")
                messagebox.showerror("Error", "Translation failed. Please try again.")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def speak_text(self, text, language):
        """Speak the given text"""
        text = text.strip()
        if not text:
            messagebox.showwarning("Input Error", f"Please enter {language} text to speak.")
            return
        
        # Run TTS in a separate thread
        thread = threading.Thread(target=self.tts.speak, args=(text, language))
        thread.daemon = True
        thread.start()
    
    def listen_from_mic(self):
        """Listen from microphone and fill English text"""
        self.status_label.config(text="Listening...", foreground="blue")
        self.root.update()
        
        thread = threading.Thread(target=self._listen_thread)
        thread.daemon = True
        thread.start()
    
    def _listen_thread(self):
        """Listen in background thread"""
        try:
            recognized_text = self.recognizer.recognize_from_microphone()
            
            if recognized_text:
                self.english_text.delete("1.0", tk.END)
                self.english_text.insert("1.0", recognized_text)
                self.status_label.config(text="Recognized successfully!", foreground="green")
            else:
                self.status_label.config(text="Recognition failed!", foreground="red")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
    
    def copy_to_clipboard(self):
        """Copy Kannada text to clipboard"""
        text = self.kannada_text.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showwarning("Empty", "No text to copy!")


def main():
    """Main function"""
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
