import numpy as np


def top_track_audio_features_average(audio_features):
    danceabilities = []
    energy = []
    loudness = []
    acousticness = []
    liveness = []
    for feature in audio_features:
        danceabilities.append(int(f"{feature['danceability'] * 100:.0f}"))
        energy.append(int(f"{feature['energy'] * 100:.0f}"))
        loudness.append(int(f"{abs(feature['loudness'] / 60) * 100:.0f}"))
        acousticness.append(int(f"{feature['acousticness'] * 100:.0f}"))
        liveness.append(int(f"{feature['liveness'] * 100:.0f}"))
    print(np.mean(liveness))
    return {
        "danceability": np.mean(danceabilities),
        "energy": np.mean(energy),
        "loudness": np.mean(loudness),
        "acousticness": np.mean(acousticness),
        "liveness": np.mean(liveness)
    }
