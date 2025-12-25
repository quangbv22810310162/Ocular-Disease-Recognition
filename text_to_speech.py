import os
import uuid

from gtts import gTTS


class TextToSpeech:
    def __init__(self, audio_folder=None):
        self.audio_folder = audio_folder or os.getenv('AUDIO_FOLDER', 'static/audio')
        os.makedirs(self.audio_folder, exist_ok=True)

    def convert_to_speech(self, text):
        # Tạo file audio với tên ngẫu nhiên
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(self.audio_folder, filename)
        
        # Chuyển text thành speech
        tts = gTTS(text=text, lang='vi')
        tts.save(filepath)
        
        return filename 