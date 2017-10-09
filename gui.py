import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

from dataset import Dataset
import settings

LARGE_FONT = ("Verdana", 12)


def write(path, content, end='\n'):
    """Appends data to the chosen file"""
    with open(path, "a") as f:
        f.write(str(content))
        f.write(end)


class LabelApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Label helper")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Config, Graph,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Graph)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Config(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Config", font=LARGE_FONT)
        label.pack(padx=50, pady=50)

        button = ttk.Button(self, text="Graph",
                            command=lambda: controller.show_frame(Graph))
        button.pack()


class Graph(tk.Frame):
    def __init__(self, parent, controller):

        # Boilerplate
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Up arrow for 0 (good), down arrow for 1 (bad)", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        fig = Figure(figsize=(10, 3), dpi=100)
        plot = fig.add_subplot(111)

        self.dataset = Dataset(settings.FILENAME, settings.CHUNK_SIZE, settings.STEP)

        data = self.dataset.next_chunk()
        self.X, self.Y = data[:, 0], data[:, 1]
        plot.scatter(self.X, self.Y, s=.01)

        # Boilerplate
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # To fix: saving the last label
        def up(event=None):
            try:
                self.Y = self.dataset.next_chunk()[:, 1]
            except:
                return
            print("ok")
            write('result.txt', 1)
            plot.clear()
            plot.scatter(self.X, self.Y, s=.01)
            canvas.show()

        def down(event=None):
            try:
                self.Y = self.dataset.next_chunk()[:, 1]
            except:
                return
            print("bad")
            write('result.txt', 0)
            plot.clear()

            plot.scatter(self.X, self.Y, s=.01)
            canvas.show()

        controller.bind("<Up>", up)
        controller.bind("<Down>", down)