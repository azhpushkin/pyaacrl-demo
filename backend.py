import random
import time

import sounddevice as sd

sd.default.samplerate = 44_100


class Backend:
    def __init__(self):
        # TODO: init pyaacrl over here
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

    def record(self, duration: int = 5):
        self.current_recording = sd.rec((duration * sd.default.samplerate), channels=1, blocking=True)
    
    def play_recording(self):
        sd.play(self.current_recording, blocking=True)

    def match_recording(self):
        time.sleep(5)
        return [
            (random.randint(0, 100), song)
            for song in self.get_all_library_songs()
        ]
    