from tkinter import *
from tkinter import PhotoImage

def on_enter(event):
    event.widget.config(font=("Comic Sans MS", 32, "bold"))

def on_leave(event):
    event.widget.config(font=("Comic Sans MS", 30))

window = Tk()
window.title("Игра Жизнь")

bg = PhotoImage(file="C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/backgr.png")
canvas1 = Canvas(window, width=1540, height=790)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")
canvas1.create_text(770, 150, text="Жизнь", font=("Comic Sans MS", 60, "bold"), fill="white")

button1 = Label(window, text="  Выход", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat", bg="#4fc8f3")
button2 = Label(window, text="  Начать", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat", bg="#4fc8f3")
button3 = Label(window, text="Загрузить", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat", bg="#4fc8f3")
button4 = Label(window, text="♫", fg="white", font=("Comic Sans MS", 30), cursor="hand2", relief="flat", bg="#4fc8f3")
button5 = Label(window, text="🛈", fg="#4fc8f3", font=("Comic Sans MS", 30), cursor="hand2", relief="flat", bg="white")

button1.bind("<Enter>", on_enter)
button1.bind("<Leave>", on_leave)
button2.bind("<Enter>", on_enter)
button2.bind("<Leave>", on_leave)
button3.bind("<Enter>", on_enter)
button3.bind("<Leave>", on_leave)
button4.bind("<Enter>", on_enter)
button4.bind("<Leave>", on_leave)
button5.bind("<Enter>", on_enter)
button5.bind("<Leave>", on_leave)

button1_canvas = canvas1.create_window(678, 370, anchor="nw", window=button1)
button2_canvas = canvas1.create_window(670, 230, anchor="nw", window=button2)
button3_canvas = canvas1.create_window(670, 300, anchor="nw", window=button3)
button4_canvas = canvas1.create_window(12, 2, anchor="nw", window=button4)
button5_canvas = canvas1.create_window(1400, 700, anchor="nw", window=button5)

window.mainloop()