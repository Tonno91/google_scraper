import tkinter as tk
from tkinter import ttk, END
import tkinter.font as font


class Button_box(tk.Frame):
    def __init__(self, text, colour="green"):
        super().__init__()
        self.status_click = False
        self.box = tk.Button(self, text=text, fg=colour, command=(lambda: self.click_on(text)))
        self.box['font'] = myFont["button"]
        self.box.pack()

    def click_on(self, text):
        print("Button \"{}\" action: click - ".format(text), end='')
        if not self.status_click:
            self.status_click = True
        print("Button \"{}\" status: {}".format(text, self.status_click))


class Combo_box(tk.Frame):
    def __init__(self, text, values, colour="black"):
        super().__init__()
        self.title = tk.Label(self, text=text, fg=colour)
        self.title['font'] = myFont["label"]
        self.title.pack(side="left", padx=10, pady=10)
        self.box = ttk.Combobox(self, values=values, width=30, height=1)
        self.box.set("")
        self.box['font'] = myFont["label"]
        self.box.pack(side="left", ipadx=20, ipady=3, padx=10, pady=10)


class Spin_box(tk.Frame):
    def __init__(self, text, min, max):
        super().__init__()
        self.title = tk.Label(self, text=text)
        self.title['font'] = myFont["label"]
        self.title.pack(side="left", padx=10, pady=10)
        self.box = tk.Spinbox(self, from_=min, to=max)
        self.box.delete(first=0)
        self.box['font'] = myFont["label"]
        self.box.pack(side="left", padx=10, pady=10)

    def get_value(self):
        return int(self.box.get().replace('\n', ''))


class Text_box(tk.Frame):
    def __init__(self, text, colour="black"):
        super().__init__()
        self.title = tk.Label(self, text=text, fg=colour)
        self.title['font'] = myFont["label"]
        self.title.pack(side="left", padx=10, pady=10)
        self.box = tk.Text(self, width=30, height=1)
        self.box['font'] = myFont["label"]
        self.box.pack(side="left", padx=10, pady=10)

    def get_value(self):
        return self.box.get(1.0, END).replace('\n', '')


class Progress_bar(tk.Frame):
    def __init__(self):
        super().__init__()
        self.bar = ttk.Progressbar(self, orient='horizontal', length=400,
                                     mode='determinate')
        self.bar.pack(side="left", padx=10, pady=10, expand="YES")

    def bar_step(self, percentage):
        self.bar['value'] = percentage


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MainApplication, self).__init__()
        self.title("        GOOGLE SCRAPER      ")
        self.configure(background='pale green')

        global myFont
        myFont = {"button": font.Font(family='Helvetica', size=16, weight='bold'),
                  "label": font.Font(family='Helvetica', size=14)}

        self.website = Combo_box("Website", ["Google", "Bing"])
        self.rep_time = Spin_box("Repeat Time (sec)", 1, 20)
        self.rep_limit = Spin_box("Repeat Limit", 1, 100)
        self.key_words = Text_box("Key words")
        self.result_num = Spin_box("Result number", 1, 100)
        self.start = Button_box("Start Analysis")
        self.start_bar = Progress_bar()
        self.stop = Button_box("Stop Analysis", "red")

        for row, element in enumerate([self.start, self.start_bar, self.stop, self.result_num,
                                       self.rep_time, self.rep_limit, self.key_words, self.website]):
            element.grid(row=row, column=0)
