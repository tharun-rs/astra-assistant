# wake_word.py
import pvporcupine
import pyaudio
import struct
import numpy as np
from config import PICOVOICE_ACCESS_KEY, MICROPHONE_INDEX

class WakeWordDetector:
    def __init__(self, keyword="jarvis"):
        self.porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keywords=[keyword]
        )

        self.pa = pyaudio.PyAudio()

        # Use the first USB mic at 44100 Hz
        self.device_index = None
        self.input_rate = 44100

        # Find device matching MICROPHONE_INDEX
        self.device_index = None
        for i in range(self.pa.get_device_count()):
            dev = self.pa.get_device_info_by_index(i)
            if f"card {MICROPHONE_INDEX}" in dev["name"].lower() or "usb pnp sound device" in dev["name"].lower():
                if dev["maxInputChannels"] > 0:
                    self.device_index = i
                    break

        if self.device_index is None:
            raise RuntimeError(f"Audio card {MICROPHONE_INDEX} not found")

        self.frames_per_buffer = int(
            self.porcupine.frame_length * self.input_rate / self.porcupine.sample_rate
        )

        self.stream = self.pa.open(
            rate=self.input_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.frames_per_buffer
        )

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
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        self.porcupine.delete()
