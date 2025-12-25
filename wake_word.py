# wake_word.py
import pvporcupine
import numpy as np
from config import PICOVOICE_ACCESS_KEY

class WakeWordDetector:
    def __init__(self, audio_manager, keyword="jarvis"):
        self.audio = audio_manager

        self.porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=[keyword]
        )

        # Porcupine requirements
        self.sample_rate = self.porcupine.sample_rate        # 16000
        self.frame_length = self.porcupine.frame_length      # e.g. 512

        # Open mic stream ONCE at correct rate
        self.stream_ctx = self.audio.open_mic_stream(
            rate=self.sample_rate,
            frames_per_buffer=self.frame_length
        )
        self.stream = self.stream_ctx.__enter__()

    def detect(self):
        # sounddevice API
        data, overflowed = self.stream.read(self.frame_length)

        if overflowed:
            return False

        pcm = np.frombuffer(data, dtype=np.int16)

        # Porcupine expects exactly frame_length samples
        if len(pcm) != self.frame_length:
            return False

        return self.porcupine.process(pcm) >= 0

    def terminate(self):
        self.stream_ctx.__exit__(None, None, None)
        self.porcupine.delete()
