import random, string
import tkinter as tk
from tkinter import filedialog as tk_fd
from tkinter.font import nametofont
import tkinter.ttk as ttk
from PIL import Image, ImageTk



class App:
    def __init__(self, root):
        self.root = root

        # self.root.minsize(600, 500)
        # self.root.maxsize(600, 500)
        self.root.resizable(False, False)

        tk.Button(root, text='Open a library', command=self.pick_library, width=10)\
            .grid(row=0, column=0, pady=10, padx=10)
        
        self.lib_name = tk.StringVar()
        self.lib_name.set('No library picked')
        tk.Label(textvariable=self.lib_name).\
            grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=10)

        i = Image.open('circle-solid.png')
        self.rec = ImageTk.PhotoImage(i.resize((16, 16)))

        i2 = Image.open('play-solid.png')
        self.play = ImageTk.PhotoImage(i2.resize((16, 16)))

        



        tk.Button(root, text='Record', command=self.record, image=self.rec, compound=tk.LEFT)\
            .grid(row=1, column=0, padx=10, pady=10)
        tk.Button(root, text='Replay', command=self.record, image=self.play, compound=tk.LEFT)\
            .grid(row=1, column=1, padx=10)
        tk.Button(root, text='List', command=self.record, width=8)\
            .grid(row=1, column=2, padx=10)
        tk.Button(root, text='Add', command=self.record, width=8)\
            .grid(row=1, column=3, padx=10)

        
        self.f = tk.Frame()
        self.f.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW, padx=10, pady=10)



        columns = ('#1', '#2', )
        self.results = ttk.Treeview(self.f, show='headings', columns=columns)

        self.results.heading('#1', text='Match')
        self.results.column('#1', minwidth=50, width=100, stretch=0, anchor=tk.CENTER)
        self.results.heading('#2', text='Name')

        rand_text = lambda: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(10, 30)))

        for _ in range(50):
            self.results.insert("", tk.END, values=('50%', rand_text()))

        self.results.grid(row=0, column=0, sticky='nsew')
        self.f.columnconfigure(0, weight=1)

        sb = ttk.Scrollbar(self.f, orient=tk.VERTICAL, command=self.results.yview)
        sb.grid(row=0, column=1, sticky='ns')

        self.results.configure(yscrollcommand=sb.set)
        sb.config(command=self.results.yview)


        

    
    
    def record(self):
        pass
    
    def pick_library(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = tk_fd.askopenfilename(
            title='Open a file',
            initialdir='~',
            filetypes=filetypes
        )
        print('Picked', filename)

        self.lib_name.set('Loaded: ' + filename)




if __name__ == '__main__':
    root = tk.Tk()
    def_font = nametofont("TkDefaultFont")
    def_font.configure(size=12)
    app = App(root)
    root.mainloop()

