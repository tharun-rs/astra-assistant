# spotify_player.py
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, LIBRE_SPOT_DEVICE

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

def play_song(song_name):
    devices = sp.devices()["devices"]
    print("Available devices:", [d["name"] for d in devices])

    device = next(
        (d for d in devices if d["name"] == LIBRE_SPOT_DEVICE),
        None
    )

    if not device:
        print(f"{LIBRE_SPOT_DEVICE} device not found")
        return

    device_id = device["id"]

    results = sp.search(q=song_name, type="track", limit=1)
    if not results["tracks"]["items"]:
        print("Song not found")
        return

    uri = results["tracks"]["items"][0]["uri"]

    # Step 1: Transfer playback
    sp.transfer_playback(
        device_id=device_id,
        force_play=False
    )

    # Step 2: Wait until device is active
    import time
    for _ in range(10):
        state = sp.current_playback()
        if state and state.get("device", {}).get("id") == device_id:
            break
        time.sleep(0.5)
    else:
        print("Device never became active")
        return

    # Step 3: Start playback (NO device_id here)
    sp.start_playback(
        uris=[uri]
    )

    print(f"Playing on {LIBRE_SPOT_DEVICE}: {song_name}")

    devices = sp.devices()["devices"]
    print("Available devices:", [d["name"] for d in devices])

    device = next(
        (d for d in devices if d["name"] == LIBRE_SPOT_DEVICE),
        None
    )

    if not device:
        print(f"{LIBRE_SPOT_DEVICE} device not found")
        return

    device_id = device["id"]

    results = sp.search(q=song_name, type="track", limit=1)
    if not results["tracks"]["items"]:
        print("Song not found")
        return

    uri = results["tracks"]["items"][0]["uri"]

    # activate the device
    sp.transfer_playback(
        device_id=device_id,
        force_play=True
    )

    # Small delay helps librespot wake up
    import time
    time.sleep(0.5)

    sp.start_playback(
        device_id=device_id,
        uris=[uri]
    )

    print(f"Playing on {LIBRE_SPOT_DEVICE}: {song_name}")
