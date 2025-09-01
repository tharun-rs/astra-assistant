# audio_manager.py
import pyaudio
import threading
from contextlib import contextmanager

class AudioManager:
    def __init__(self, mic_index, speaker_index):
        self.p = pyaudio.PyAudio()
        self.mic_index = mic_index
        self.speaker_index = speaker_index
        self.mic_lock = threading.Lock()
        self.speaker_lock = threading.Lock()

    @contextmanager
    def open_mic_stream(self, rate, frames_per_buffer):
        self.mic_lock.acquire()
        stream = None
        try:
            stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=True,
                input_device_index=self.mic_index,
                frames_per_buffer=frames_per_buffer
            )
            yield stream
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            self.mic_lock.release()

    def release_mic(self, stream):
        stream.stop_stream()
        stream.close()
        self.mic_lock.release()

    @contextmanager
    def open_speaker_stream(self, rate):
        self.speaker_lock.acquire()
        stream = None
        try:
            stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=rate,
                output=True,
                output_device_index=self.speaker_index
            )
            yield stream
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            self.speaker_lock.release()

    def release_speaker(self, stream):
        """Close speaker stream and release lock"""
        stream.stop_stream()
        stream.close()
        self.speaker_lock.release()

    def terminate(self):
        if self.mic_lock.locked() or self.speaker_lock.locked():
            print("Warning: terminating while streams are active")
        self.p.terminate()

