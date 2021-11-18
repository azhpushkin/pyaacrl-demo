import sys
import threading

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog
from PySide2 import QtCore, QtGui

from backend import Backend


UI_FILE_PATH = "pyaacrl-gui-main.ui"


class Window:
    backend: Backend

    def __init__(self):
        file = QtCore.QFile(UI_FILE_PATH)
        file.open(QtCore.QFile.ReadOnly)

        self.window = QUiLoader().load(file)


        file.close()

        self.connect_signals()

        self.backend = Backend()
        self.recording = False

    def connect_signals(self):
        self.window.button_pick_library.clicked.connect(self.pick_library)
        self.window.button_record.clicked.connect(self.start_stop_recording)
        self.window.button_from_file.clicked.connect(self.open_clip_from_file)
        self.window.button_play.clicked.connect(self.play)
        self.window.button_recognize.clicked.connect(self.recognize)

        self.window.list_songs.itemClicked.connect(self.on_item_click)

    def on_item_click(self, item):
        self.window.button_rename.setEnabled(True)
        self.window.button_delete_song.setEnabled(True)

    def recognize(self):
        def on_done(result_str):
            self.window.label_matches_result.setText(result_str)

        threading.Thread(
            target=self.backend.match_recording,
            args=(on_done, )
        ).start()
        

    def play(self):
        self.backend.play_recording()
    
    def pick_library(self):
        path_to_file, _ = QFileDialog.getOpenFileName(
            self.window,
            filter="Music files (*.mp3 *.wav)"
        )
        
        a = self.window.label_library_path
        a.setText(f'<b>Loaded:</b> {path_to_file}')
        a.setEnabled(True)

        self.backend.open_songs_library(path_to_file)
        self.window.button_add_songs.setEnabled(True)


        # TODO
        self.window.list_songs.clear()
        songs = ['asdasdasd', '123', 'idh1u910d']
        for song in songs:
            self.window.list_songs.addItem(song)

        self.window.button_rename.setEnabled(False)
        self.window.button_delete_song.setEnabled(False)
    
    def start_stop_recording(self):
        if not self.recording:
            self.window.button_record.setText('Stop')
            self.window.button_record.setIcon(
                QtGui.QIcon(QtGui.QPixmap("stop.png"))
            )
            self.recording = True

            self.backend.start_recording()

            self.window.button_record.setStyleSheet("border: 1px solid green");


        else:
            self.window.button_record.setText('Record')
            self.window.button_record.setIcon(
                QtGui.QIcon(QtGui.QPixmap("record.png"))
            )
            self.window.button_record.setStyleSheet("");
            self.recording = False
            self.backend.stop_recording()

            self.clip_loaded()

    def open_clip_from_file(self):
        path_to_file, _ = QFileDialog.getOpenFileName(
            self.window,
            filter="Music files (*.mp3 *.wav)"
        )

        self.backend.open_file(path_to_file)
        self.clip_loaded()

    
    def clip_loaded(self):
        self.window.label_clip_status.setText(f'Clip loaded')

        self.window.button_play.setEnabled(True)
        self.window.button_recognize.setEnabled(True)



if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    
    app = QApplication()

    w = Window()
    w.window.show()
    sys.exit(app.exec_())