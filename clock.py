
try:
    import tkinter as tk               
    from tkinter import font as tkfont  
except ImportError:
    import Tkinter as tk    

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Clock, Stopwatch, Timer):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Clock")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Clock(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Clock", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="stopwatch", command=lambda: controller.show_frame("Stopwatch"))
        button2 = tk.Button(self, text="timer", command=lambda: controller.show_frame("Timer"))
        button1.pack()
        button2.pack()

        from tkinter import Label
        from time import strftime

        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(self, font=('calibri', 40, 'bold'), background='#F0F0F0', foreground='black')
        lbl.pack(side="top", pady=50)
        time()

class Stopwatch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        from tkinter import Button, Label
        import time

        class Stopwatch:
            def __init__(self, master):
                self.master = master
                self.label = Label(self.master, text="0.0", font=('calibri', 40, 'bold'))
                self.label.pack()

                self.running = False
                self.start_time = None
                self.update_clock()

                self.start_button = Button(self.master, text="Start", command=self.start_stop)
                self.start_button.pack(side="left")

                self.reset_button = Button(self.master, text="Reset", command=self.reset)
                self.reset_button.pack(side="right")

            def update_clock(self):
                if self.running:
                    elapsed_time = time.time() - self.start_time
                    self.label.config(text=str(round(elapsed_time, 1)))
                self.label.after(100, self.update_clock)

            def start_stop(self):
                if self.running:
                    self.running = False
                    self.start_button.config(text="Start")
                else:
                    if self.start_time is None:
                        self.start_time = time.time()
                    else:
                        self.start_time = time.time() - (float(self.label.cget("text")))
                    self.running = True
                    self.start_button.config(text="Stop")

            def reset(self):
                self.running = False
                self.start_time = None
                self.label.config(text="0.0")

        stopwatch = Stopwatch(self)

        label = tk.Label(self, text="Stopwatch", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Clock", command=lambda: controller.show_frame("Clock"))
        button.pack()


class Timer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Clock",
                           command=lambda: controller.show_frame("Clock"))
        button.pack()


        


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()