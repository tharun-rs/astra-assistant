# wake_word.py
import pvporcupine
import pyaudio
import struct

class WakeWordDetector:
    def __init__(self, keyword="hey google"):
        self.porcupine = pvporcupine.create(keywords=[keyword])
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def detect(self):
        pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
        return self.porcupine.process(pcm) >= 0

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        self.porcupine.delete()
