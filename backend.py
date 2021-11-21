import random
import time
import numpy as np

import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment

import pyaacrl

sd.default.samplerate = 44_100


class Backend:
    def __init__(self):
        self.library = None
        self.extra_songs = []

    def open_songs_library(self, path):
        self.library = pyaacrl.Storage(path)

    def add_song_to_library(self, path):
        self.extra_songs.append(path)

    def get_all_library_songs(self):
        return [s.name for s in self.library.list_songs()]
    
    def _save_frames(self, indata, frames, time, status):
        self.frames.append(np.copy(indata))
    
    def start_recording(self):
        self.frames = []
        self.out = sd.InputStream(latency=None, channels=1, callback=self._save_frames)
        self.out.start()

    def stop_recording(self):
        self.out.stop()

        # TODO: check pydub.export
        sf.write('recording.wav', np.concatenate(self.frames), sd.default.samplerate)
        self.out.close()

        self.open_file('recording.wav')

    def open_file(self, filename):
        if filename.endswith('mp3'):
            self.file = AudioSegment.from_mp3(filename)
        else:
            self.file = AudioSegment.from_wav(filename)

        self.file__path = filename
        
    def play_recording(self):
        a = self.file.split_to_mono()

        x = [np.array(i.get_array_of_samples()) for i in a]
        q = np.column_stack(x)
        sd.play(q)

    def match_recording(self, callback) -> str:
        matches = self.library.get_matches(pyaacrl.Fingerprint.from_wav(self.file__path))
        top_match, conf = matches[0]
        callback(top_match.name + '\n' + f'Confidence: {conf}')

