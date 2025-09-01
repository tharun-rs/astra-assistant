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

        # Porcupine expects 16kHz mono int16
        self.input_rate = 44100
        self.frames_per_buffer = int(
            self.porcupine.frame_length * self.input_rate / self.porcupine.sample_rate
        )

        # Keep mic open for the lifetime of detector
        self.stream_ctx = self.audio.open_mic_stream(
            rate=self.input_rate,
            frames_per_buffer=self.frames_per_buffer
        )
        self.stream = self.stream_ctx.__enter__()

    def detect(self):
        data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)
        pcm = np.frombuffer(data, dtype=np.int16)

        # Resample 44100 → 16000
        pcm = np.interp(
            np.linspace(0, len(pcm), self.porcupine.frame_length, endpoint=False),
            np.arange(len(pcm)),
            pcm
        ).astype(np.int16)

        return self.porcupine.process(pcm) >= 0

    def terminate(self):
        # Close mic stream properly
        self.stream_ctx.__exit__(None, None, None)
        self.porcupine.delete()
