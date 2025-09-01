# keep_speaker_alive.py
# Keeps the speaker alive by playing low noise if configured to do so
import pyaudio
import numpy as np
import threading
import time
from config import PLAY_NOISE, SPEAKER_INDEX, NOISE_LEVEL

class LowNoisePlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.running = False
        self.thread = None
        self.device_index = SPEAKER_INDEX
        self.noise_level = NOISE_LEVEL

    def _play_noise(self):
        print("Starting low noise playback to keep speaker alive...")
        stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=44100,
            output=True,
            output_device_index=self.device_index,
            frames_per_buffer=1024,
        )

        while self.running:
            # constant tiny signal
            noise = (np.ones(1024) * self.noise_level).astype(np.float32)
            stream.write(noise.tobytes())
            time.sleep(0.05)


        stream.stop_stream()
        stream.close()

    def start(self):
        if PLAY_NOISE == "ON" and not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._play_noise, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.p.terminate()

