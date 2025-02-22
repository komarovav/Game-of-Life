from tkinter import *
from tkinter import Toplevel, PhotoImage, Canvas
from playsound import playsound

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')


def on_enter(event):
    event.widget.config(font=("Comic Sans MS", 32, "bold"))


def on_leave(event):
    event.widget.config(font=("Comic Sans MS", 30))


def start():
    print("иу")


def pattern():
    pattern_window = Toplevel(window)
    pattern_window.title("Шаблоны")
    center_window(pattern_window, 400, 300)
    pattern_window.bg3 = PhotoImage(file="C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/backgr.png")
    canvas1 = Canvas(pattern_window, width=400, height=300)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=pattern_window.bg3, anchor="nw")
    close_button = Label(pattern_window, text="  Выход", fg="white", font=("Comic Sans MS", 30), cursor="hand2",
                         relief="flat", bg="#4fc8f3")
    close_button.pack(pady=10)
    close_button.bind("<Button-1>", lambda event: pattern_window.destroy())
    close_button_canvas = canvas1.create_window(230, 230, anchor="nw", window=close_button)


def exit():
    window.destroy()


def open_tutorial():
    tutorial_window = Toplevel(window)
    tutorial_window.title("Обучение")
    center_window(tutorial_window, 1000, 500)
    tutorial_window.bg2 = PhotoImage(file="C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/backgr.png")
    canvas1 = Canvas(tutorial_window, width=1000, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=tutorial_window.bg2, anchor="nw")

    close_button = Label(tutorial_window, text="  Выход", fg="white", font=("Comic Sans MS", 30), cursor="hand2",
                         relief="flat", bg="#4fc8f3")
    close_button.pack(pady=10)
    close_button.bind("<Button-1>", lambda event: tutorial_window.destroy())
    close_button_canvas = canvas1.create_window(830, 430, anchor="nw", window=close_button)

window = Tk()
window.title("Игра Жизнь")

bg = PhotoImage(file="C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/backgr.png")
canvas1 = Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")
canvas1.create_text(770, 150, text="Жизнь", font=("Comic Sans MS", 60, "bold"), fill="white")

button_exit = Label(window, text="  Выход", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat",
                bg="#4fc8f3")
button_start = Label(window, text="  Начать", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat",
                bg="#4fc8f3")
button_pattern = Label(window, text="Шаблоны", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat",
                bg="#4fc8f3")
button_music = Label(window, text="♫", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat", bg="#4fc8f3")
button_info = Label(window, text="🛈", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat", bg="#4fc8f3")

button_exit.bind("<Enter>", on_enter)
button_exit.bind("<Leave>", on_leave)
button_exit.bind("<Button-1>", lambda event: exit())

button_start.bind("<Enter>", on_enter)
button_start.bind("<Leave>", on_leave)
button_start.bind("<Button-1>", lambda event: start())

button_pattern.bind("<Enter>", on_enter)
button_pattern.bind("<Leave>", on_leave)
button_pattern.bind("<Button-1>", lambda event: pattern())

button_music.bind("<Enter>", on_enter)
button_music.bind("<Leave>", on_leave)

button_info.bind("<Enter>", on_enter)
button_info.bind("<Leave>", on_leave)
button_info.bind("<Button-1>", lambda event: open_tutorial())

button_exit_canvas = canvas1.create_window(678, 370, anchor="nw", window=button_exit)
button_start_canvas = canvas1.create_window(670, 230, anchor="nw", window=button_start)
button_pattern_canvas = canvas1.create_window(670, 300, anchor="nw", window=button_pattern)
button_music_canvas = canvas1.create_window(12, 2, anchor="nw", window=button_music)
button_info_canvas = canvas1.create_window(1485, 2, anchor="nw", window=button_info)

window.mainloop()
