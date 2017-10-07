import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
matplotlib.use("TkAgg")

LARGE_FONT = ("Verdana", 12)


class LabelApp(tk.Tk):
    """Backbone of the app"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self,  "Sea of BTC Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Graph,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Graph)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    """Creates a page that might be used for config in the future"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(padx=50, pady=50)

        button = ttk.Button(self, text="Graph", 
                            command=lambda: controller.show_frame(Graph))
        button.pack()

        
class Graph(tk.Frame):
    """Creates a page that holds the actual graph and will eventually do all the good stuff"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Up arrow for 0 (good), down arrow for 1 (bad)", font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        
        fig = Figure(figsize=(10,3), dpi=100)
        a = fig.add_subplot(111)
        
        self.X = np.linspace(-np.pi, np.pi, 1000)
        self.Y = 2 + np.sin(self.X) + 0.1*np.random.randn(1000)
        a.scatter(self.X, self.Y, s=1)
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        def up(event=None):
            a.clear()
            self.Y = self.Y**2
            a.scatter(self.X, self.Y, s=1)
            canvas.show()
            
        def down(event=None):
            a.clear()
            self.Y = self.Y**(1/2)
            a.scatter(self.X, self.Y, s=1)
            canvas.show()
        
        controller.bind("<Up>", up)
        controller.bind("<Down>", down)
        
if __name__ == '__main__':
    app = LabelApp()
    app.mainloop()