import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog as tk_fd
from tkinter.font import nametofont

from PIL import Image, ImageTk

from backend import Backend


APP_GRID = {
    0: {
        0: ('open_lib_button', {}),
        1: ('lib_name_label', dict(columnspan=3, sticky=tk.W)), 
    },
    1: {
        0: ('record_button', {}),
        1: ('replay_button', {}),
        2: ('list_songs_button', {}),
        3: ('add_song_button', {}),
    },
    2: {
        0: ('results_heading', dict(columnspan=4, sticky=tk.NSEW)),
    },
    3: {
        0: ('results_frame', dict(columnspan=4, sticky=tk.NSEW))
    },
}

class GUI:
    def __init__(self, backend: Backend):
        self.backend = backend

        self.root = tk.Tk()
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=12)

        self.root.resizable(False, False)

        # store images to self to avoid garbage collection, which makes images unload from memory
        self._record_image = Image.open('record.png').resize((16, 16))
        self._record_image_tk = ImageTk.PhotoImage(self._record_image)
        self._replay_image = Image.open('play.png').resize((16, 16)) 
        self._replay_image_tk = ImageTk.PhotoImage(self._replay_image)
  
        self.open_lib_button = tk.Button(
            self.root, text='Open a library',
            command=self.open_lib_action, width=10
        )
        self.record_button = tk.Button(
            self.root, text='Record',
            image=self._record_image_tk , compound=tk.LEFT,
            command=self.record_action
        )
        self.replay_button = tk.Button(
            self.root, text='Replay',
            image=self._replay_image_tk, compound=tk.LEFT,
            command=self.replay_action
        )
        self.list_songs_button = tk.Button(
            self.root, text='List songs',
            command=self.list_songs_action, width=10
        )
        self.add_song_button = tk.Button(
            self.root, text='Add song',
            command=self.add_song_action, width=10
        )

        self.library_path_var = tk.StringVar()
        self.library_path_var.set('No library picked')
        self.lib_name_label = tk.Label(textvariable=self.library_path_var)

        self.results_heading_var = tk.StringVar()
        self.results_heading_var.set('Pick a library to use for recognition')
        self.results_heading = tk.Label(textvariable=self.results_heading_var)

        self.results_frame = tk.Frame(self.root)
        self.results: ttk.Treeview
        self._init_results_frame_()
        
        for x, cols in APP_GRID.items():
            for y, (element_id, extra_params) in cols.items():
                getattr(self, element_id).grid(row=x, column=y, padx=10, pady=10, **extra_params)
    
    def _init_results_frame_(self):
        columns = ('#1', '#2', )
        self.results = ttk.Treeview(self.results_frame, show='headings', columns=columns)

        self.results.heading('#1', text='Match')
        self.results.column('#1', minwidth=50, width=100, stretch=0, anchor=tk.CENTER)
        self.results.heading('#2', text='Name')

        self.results.grid(row=0, column=0, sticky=tk.NSEW)
        self.results_frame.columnconfigure(0, weight=1)

        scroll = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results.yview)
        scroll.grid(row=0, column=1, sticky=tk.NS)

        self.results.configure(yscrollcommand=scroll.set)
        scroll.config(command=self.results.yview)

    def start(self):
        self.root.mainloop()

    def list_songs_action(self):
        self.results_heading_var.set('List of songs, that are fingerprinted')
        self.results.column('#1', minwidth=0, width=0, stretch=0, anchor=tk.CENTER)
        songs_list = self.backend.get_all_library_songs()

        self.results.delete(*self.results.get_children())
        for song_name in songs_list:
            self.results.insert("", tk.END, values=('0%', song_name))

    def add_song_action(self):
        filename = tk_fd.askopenfilename(
            title='Open a file',
            initialdir='~',
            filetypes=[('All files', '*.*'), ]
        )
        self.backend.add_song_to_library(filename)
    
    def record_action(self):
        self.results.column('#1', minwidth=50, width=100, stretch=0, anchor=tk.CENTER)
        self.results.delete(*self.results.get_children())
        self.results_heading_var.set('Recording 7-seconds to use for recognition...')

        self.record_button.config(relief=tk.SUNKEN)
        self.root.update_idletasks()  # required to ensure that label is updated
        self.backend.record(duration=7)

        self.record_button.config(relief=tk.RAISED)
        self.results_heading_var.set('Performing recognition...')

        threading.Thread(target=self.match_and_show_results).start()

    def match_and_show_results(self):
        matched_songs = self.backend.match_recording()
        matched_songs.sort(reverse=True)
        self.results_heading_var.set('Matched songs:')

        for probability, song_name in matched_songs:
            self.results.insert("", tk.END, values=(f'{probability}%', song_name))
    
    def replay_action(self):
        self.replay_button.config(relief=tk.SUNKEN)
        self.backend.play_recording()

        self.replay_button.config(relief=tk.RAISED)
    
    def open_lib_action(self):
        filename = tk_fd.askopenfilename(
            title='Open a file',
            initialdir='~',
            filetypes=[('All files', '*.*'), ]
        )

        self.backend.open_songs_library(filename)
        self.library_path_var.set('Loaded: ' + filename)
        self.results_heading_var.set('Press "Record" to recognize track via mic')
        


if __name__ == '__main__':
    app_backend = Backend()
    gui = GUI(app_backend)
    gui.start()
