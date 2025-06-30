# recorder.py
import pyaudio
import wave

def record(filename="command.wav", seconds=5):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    for _ in range(0, int(44100 / 1024 * seconds)):
        frames.append(stream.read(1024))

    stream.stop_stream()
    stream.close()
    pa.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
