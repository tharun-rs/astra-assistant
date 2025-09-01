# main.py
from wake_word import WakeWordDetector
from recorder import record
from transcriber import transcribe
from spotify_player import play_song
from keep_speaker_alive import LowNoisePlayer

def extract_song_name(text):
    if "play" in text.lower():
        return text.lower().split("play", 1)[1].strip()
    return ""

def main():
    detector = WakeWordDetector()
    noise = LowNoisePlayer()
    print("Listening for wake word...")

    try:
        while True:
            noise.start()
            if detector.detect():
                print("Wake word detected.")
                record()
                transcript = transcribe()
                print(f"You said: {transcript}")
                song = extract_song_name(transcript)
                if song:
                    play_song(song)
    finally:
        detector.terminate()

if __name__ == "__main__":
    main()

