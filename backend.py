import random
import time
import numpy as np

import sounddevice as sd
import soundfile as sf

sd.default.samplerate = 44_100


class Backend:
    def __init__(self):
        self.library = None
        self.extra_songs = []
        self.current_recording = None

    def open_songs_library(self, path):
        self.library = path

    def add_song_to_library(self, path):
        self.extra_songs.append(path)

    def get_all_library_songs(self):
        songs = ['Lorem', 'Ipsum', 'hahaha', 'Some another song', 'Что-то на русском', *self.extra_songs]
        random.shuffle(songs)
        return songs
    
    def _save_frames(self, indata, frames, time, status):
        self.frames.append(np.copy(indata))
    
    def start_recording(self):
        self.frames = []
        self.out = sd.InputStream(latency=None, channels=1, callback=self._save_frames)
        self.out.start()

    def stop_recording(self):
        self.out.stop()
        sf.write('recording.wav', np.concatenate(self.frames), sd.default.samplerate)
        self.out.close()
    
    def play_recording(self):
        fs, x = sf.read('recording.wav', 'rb')
        sd.play(x, fs)

    def match_recording(self) -> str:
        time.sleep(5)
        return "Cool song, written by cool author"
