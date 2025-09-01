# keep_speaker_alive.py
# Keeps the speaker alive by playing low noise if configured to do so
import numpy as np
import threading
import time
from config import PLAY_NOISE, NOISE_LEVEL


class LowNoisePlayer:
    def __init__(self, audio_manager):
        self.audio = audio_manager
        self.running = False
        self.thread = None
        self.noise_level = NOISE_LEVEL

    def _play_noise(self):
        print("Starting low noise playback to keep speaker alive...")
        with self.audio.open_speaker_stream(rate=44100) as stream:
            while self.running:
                # constant tiny signal
                noise = (np.ones(1024) * self.noise_level).astype(np.float32)
                stream.write(noise.tobytes())
                time.sleep(0.05)

    def start(self):
        if PLAY_NOISE == "ON" and not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._play_noise, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
