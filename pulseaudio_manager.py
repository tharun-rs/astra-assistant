# pulseaudio_manager.py
import sounddevice as sd
import threading
from contextlib import contextmanager
import pulsectl
import time

class PulseAudioManager:
    def __init__(self, mic_name=None, speaker_name=None):
        """
        mic_name: optional, used to resume USB mic if suspended
        speaker_name: optional, not needed; playback goes via default sink
        """
        self.mic_lock = threading.Lock()
        self.speaker_lock = threading.Lock()
        self.pulse = pulsectl.Pulse('audio-manager')

        # Resume mic if name provided
        if mic_name:
            try:
                source = self.pulse.get_source_by_name(mic_name)
                self.pulse.source_suspend(source.index, False)
                time.sleep(0.2)  # give PulseAudio time to activate
            except pulsectl.PulseOperationFailed:
                print(f"Warning: mic '{mic_name}' not found or cannot be resumed")

        # Use default devices; PulseAudio will route USB mic & speaker automatically
        self.mic_index = None
        self.speaker_index = None

    @contextmanager
    def open_mic_stream(self, rate, frames_per_buffer):
        self.mic_lock.acquire()
        stream = sd.InputStream(
            device='default',  # use PulseAudio default source
            samplerate=rate,
            channels=1,
            dtype='int16',
            blocksize=frames_per_buffer
        )
        stream.start()
        try:
            yield stream
        finally:
            stream.stop()
            stream.close()
            self.mic_lock.release()

    def release_mic(self, stream):
        stream.stop()
        stream.close()
        self.mic_lock.release()

    @contextmanager
    def open_speaker_stream(self, rate):
        self.speaker_lock.acquire()
        stream = sd.OutputStream(
            device='default',  # use PulseAudio default sink
            samplerate=rate,
            channels=1,
            dtype='float32'
        )
        stream.start()
        try:
            yield stream
        finally:
            stream.stop()
            stream.close()
            self.speaker_lock.release()

    def release_speaker(self, stream):
        stream.stop()
        stream.close()
        self.speaker_lock.release()

    def terminate(self):
        if self.mic_lock.locked() or self.speaker_lock.locked():
            print("Warning: terminating while streams are active")
        self.pulse.close()
