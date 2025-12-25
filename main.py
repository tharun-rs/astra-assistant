# main.py
from wake_word import WakeWordDetector
from recorder import record
from transcriber import transcribe
from spotify_player import play_song
from keep_speaker_alive import LowNoisePlayer
from pulseaudio_manager import PulseAudioManager
from config import MIC_NAME, SPEAKER_NAME, TRANSCRIBER_MODEL

def extract_song_name(text):
    if "play" in text.lower():
        return text.lower().split("play", 1)[1].strip()
    return ""

def main():

    # Initialize audio manager based on the selected backend
    audio = PulseAudioManager(mic_name=MIC_NAME, speaker_name=SPEAKER_NAME)
    detector = WakeWordDetector(audio_manager=audio)
    keep_alive_noise = LowNoisePlayer(audio_manager=audio)

    try:
        while True:
            keep_alive_noise.start()
            if detector.detect():
                print("Wake word detected.")
                record()
                transcript = transcribe(model=TRANSCRIBER_MODEL) # small-q5_1 for multilingual support
                print(f"You said: {transcript}")
                song = extract_song_name(transcript)
                if song:
                    play_song(song)
    finally:
        detector.terminate()

if __name__ == "__main__":
    main()

