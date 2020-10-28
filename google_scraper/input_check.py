from tkinter import messagebox


def gui_input(website, rep_time, rep_limit, result_num, key_word):
    if website != "Google":
        messagebox.showerror("Error", "The website allowed is only Google")
        return 0

    return -1
