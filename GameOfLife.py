from tkinter import *
from pathlib import Path
import random
import ctypes

font_path = Path("Font/Bowler.ttf").resolve()
ctypes.windll.gdi32.AddFontResourceW(str(font_path))

FONT = ("BOWLER", 30)
BUTTON_BG = "black"
BUTTON_FG = "white"
tutorial_window = None
pattern_window=None

window = Tk()
window.resizable(False, False)
window.title("Игра Жизнь")
window.state('zoomed')

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

def on_enter(event):
    if not hasattr(event.widget, "original_font"):
        event.widget.original_font = event.widget.cget("font")

    current_font = event.widget.cget("font")
    font_family, font_size = parse_font(current_font)

    new_font_size = int(font_size) + 1
    event.widget.config(font=(font_family, new_font_size))

def parse_font(font_string):
    parts = font_string.split()
    font_family = parts[0].strip("{}")
    font_size = parts[1].strip("{}")
    return font_family, font_size

def on_leave(event):
    if hasattr(event.widget, "original_font"):
        event.widget.config(font=event.widget.original_font)

def create_button(parent, text, command=None, font=None):
    button_font = font if font else FONT
    button = Label(parent, text=text, fg=BUTTON_FG, font=button_font, cursor="hand2", relief="flat", bg=BUTTON_BG)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    if command:
        button.bind("<Button-1>", lambda event: command())
    return button

def show_menu():
    game_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)
    game.stop()

def start_game():
    menu_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

def pattern():
    global pattern_window

    if pattern_window is not None and pattern_window.winfo_exists():
        pattern_window.lift()
        return

    pattern_window = Toplevel(window)
    pattern_window.resizable(False, False)
    pattern_window.title("Шаблоны")
    center_window(pattern_window, 1000, 500)

    image_paths = [
        "Images/шаблон.png",
        "Images/улей.png",
        "Images/пруд.png",
        "Images/каравай.png",
        "Images/двойной каравай.png",
        "Images/пекарня.png",
        "Images/ящик.png",
        "Images/баржа.png",
        "Images/длинная баржа.png",
        "Images/лодка.png",
        "Images/длинная лодка.png",
        "Images/лодочный бант.png",
        "Images/корабль.png",
        "Images/длинный корабль.png",
        "Images/корабельный бант.png",
        "Images/змея.png",
        "Images/знак интеграла.png",
        "Images/каноэ.png",
        "Images/рыболовный крючок.png",
        "Images/авианосец.png",
        "Images/манго.png",
    ]

    images = []
    for path in image_paths:
        try:
            img = PhotoImage(file=path)
            images.append(img)
        except Exception:
            pass

    if not images:
        return

    current_image_index = 0

    canvas = Canvas(pattern_window, width=1000, height=500)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=images[current_image_index], anchor="nw")

    slide_label = Label(pattern_window,
                        text=f"Слайд {current_image_index + 1} из {len(images)}",
                        font=("BOWLER", 12),
                        background='black',
                        foreground='white')
    slide_label.pack()

    two_signs = pattern_window.register(lambda text: text == "" or (text.isdigit() and len(text) <= 2)), "%P"
    slide_entry = Entry(pattern_window, font=("BOWLER", 12), width=5, validate="key",
                        validatecommand=two_signs)
    slide_entry.pack(pady=10)

    def update_background(step):
        nonlocal current_image_index
        current_image_index = (current_image_index + step) % len(images)
        canvas.delete("all")
        canvas.create_image(0, 0, image=images[current_image_index], anchor="nw")

        slide_label.config(text=f"Слайд {current_image_index + 1} из {len(images)}")

        canvas.create_window(50, 460, anchor="nw", window=back_button)
        canvas.create_window(855, 460, anchor="nw", window=next_button)
        canvas.create_window(450, 460, anchor="nw", window=close_button)
        canvas.create_window(450, 420, anchor="nw", window=go_button)
        canvas.create_window(830, 10, anchor="nw", window=slide_label)
        canvas.create_window(420, 420, anchor="nw", window=slide_entry)

    def go_to_slide():
        nonlocal current_image_index
        try:
            slide_number = int(slide_entry.get())
            if 1 <= slide_number <= len(images):
                current_image_index = slide_number - 1
                update_background(0)
                slide_entry.delete(0, END)
                slide_label.config(text=f"Слайд {current_image_index + 1} из {len(images)}")
            else:
                return
        except ValueError:
            return

    back_button = create_button(pattern_window, "  Назад", lambda: update_background(-1), font=("BOWLER", 12))
    next_button = create_button(pattern_window, "  Далее", lambda: update_background(1), font=("BOWLER", 12))
    close_button = create_button(pattern_window, "  Выход", pattern_window.destroy, font=("BOWLER", 12))
    go_button = create_button(pattern_window, "Перейти", go_to_slide, font=("BOWLER", 12))

    canvas.create_window(50, 460, anchor="nw", window=back_button)
    canvas.create_window(855, 460, anchor="nw", window=next_button)
    canvas.create_window(450, 460, anchor="nw", window=close_button)
    canvas.create_window(450, 420, anchor="nw", window=go_button)
    canvas.create_window(830, 10, anchor="nw", window=slide_label)
    canvas.create_window(420, 420, anchor="nw", window=slide_entry)

def on_pattern_window_close():
    global pattern_window

    if pattern_window is not None:
        pattern_window.destroy()
    pattern_window = None

def open_tutorial():
    global tutorial_window

    if tutorial_window is not None and tutorial_window.winfo_exists():
        tutorial_window.lift()
        return

    tutorial_window = Toplevel(window)
    tutorial_window.resizable(False, False)
    tutorial_window.title("Обучение")
    center_window(tutorial_window, 1000, 500)
    tutorial_window.bg2 = PhotoImage(file="Images/backgr_info.png")
    canvas1 = Canvas(tutorial_window, width=1000, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=tutorial_window.bg2, anchor="nw")
    button_exit_tut = create_button(tutorial_window, "Выход", tutorial_window.destroy, font=("BOWLER", 19))
    canvas1.create_window(870, 450, anchor="nw", window=button_exit_tut)

def close_tutorial():
    global tutorial_window
    if tutorial_window is not None:
        tutorial_window.destroy()
        tutorial_window = None

class GameOfLife:
    def __init__(self, root, width=68, height=39, cell_size=18):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.canvas = Canvas(root, width=width * cell_size, height=height * cell_size)
        self.canvas.place(x=0, rely=1.0, anchor='sw')
        self.line = Canvas(root, bg="white", width=302, height=0.1)
        self.line.place(x=1228, y=135)

        self.speed = 100
        self.running = False

        self.prev_alive=0
        self.total_born = 0
        self.total_died = 0
        self.total_alive = 0
        self.generation_count = 0

        self.gradient = BooleanVar(value=False)
        self.birth_threshold = IntVar(value=3)
        self.loneliness_threshold = IntVar(value=2)
        self.overpopulation_threshold = IntVar(value=3)
        self.death_aging_slider = IntVar(value=10)

        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.rules_window = None
        self.pattern_window = None

        self.age_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.aging_enabled = BooleanVar(value=False)

        self.create_buttons()
        self.draw_grid()

    def create_buttons(self):
        self.name = Label(self.root, text="Жизнь", font=("BOWLER", 30), bg="black", fg="#00ff00")
        self.name.place(x=1325,y=45)

        self.control = Label(self.root, text="Управление", font=("BOWLER", 18), bg="black", fg="white")
        self.control.place(x=20,y=25)

        self.speed_lab = Label(self.root, text="Скорость", font=("BOWLER", 18), bg="black", fg="white")
        self.speed_lab.place(x=390,y=25)

        self.color = Label(self.root, text="Цвет", font=("BOWLER", 18), bg="black", fg="white")
        self.color.place(x=700,y=25)

        self.gradient_checkbox = Checkbutton(self.root,
                                             text="Оттенки зеленого",
                                             font=("BOWLER", 12),
                                             bg="black",
                                             fg="white",
                                             variable=self.gradient,
                                             command=self.draw_grid,
                                             selectcolor="black",
                                             activebackground="black",
                                             activeforeground="white",
                                             onvalue=True,
                                             offvalue=False)

        self.gradient_checkbox.place(x=700, y=70)

        self.status = Label(self.root, text="Статус", font=("BOWLER", 19), bg="black", fg="white")
        self.status.place(x=1320,y=150)

        self.alive = Label(self.root, text="Живые", font=("BOWLER", 14), bg="black", fg="white")
        self.alive.place(x=1235,y=200)

        self.dead = Label(self.root, text="Умерло", font=("BOWLER", 14), bg="black", fg="white")
        self.dead.place(x=1235,y=235)

        self.born = Label(self.root, text="Рождено", font=("BOWLER", 14), bg="black", fg="white")
        self.born.place(x=1235,y=270)

        self.generation = Label(self.root, text="Поколение", font=("BOWLER", 14), bg="black", fg="white")
        self.generation.place(x=1235,y=305)

        self.rules = Label(self.root, text="Правила", font=("BOWLER", 19), bg="black", fg="white")
        self.rules.place(x=1310,y=360)

        self.neighbors_born = Label(self.root, text="Соседей для рождения", font=("BOWLER", 13), bg="black", fg="white")
        self.neighbors_born.place(x=1250,y=400)

        self.born_slider = Scale(
            self.root,
            from_=2, to=7,
            orient=HORIZONTAL,
            bg="black",
            fg="white",
            variable=self.birth_threshold,
            length=250,
            command=self.validate_rules
        )
        self.born_slider.set(3)
        self.born_slider.place(x=1250, y=425)

        self.neighbors_deathalone = Label(self.root, text="Соседей для смерти", font=("BOWLER", 13), bg="black", fg="white")
        self.neighbors_deathalone.place(x=1270,y=490)

        self.alone = Label(self.root, text="(от одиночества)", font=("BOWLER", 10), bg="black", fg="white")
        self.alone.place(x=1310,y=515)

        self.death_alone_slider = Scale(
            self.root,
            from_=1, to=6,
            orient=HORIZONTAL,
            bg="black",
            fg="white",
            length=250,
            variable=self.loneliness_threshold,
            command=self.validate_rules
        )
        self.death_alone_slider.set(2)
        self.death_alone_slider.place(x=1250, y=540)

        self.death = Label(self.root, text="Соседей для смерти", font=("BOWLER", 13), bg="black", fg="white")
        self.death.place(x=1270,y=605)

        self.overpopulation = Label(self.root, text="(от перенаселения)", font=("BOWLER", 10), bg="black", fg="white")
        self.overpopulation.place(x=1310,y=630)

        self.death_over_slider = Scale(
            self.root,
            from_=3, to=8,
            orient=HORIZONTAL,
            bg="black",
            fg="white",
            length=250,
            variable=self.overpopulation_threshold,
            command=self.validate_rules
        )
        self.death_over_slider.set(3)
        self.death_over_slider.place(x=1250, y=655)

        self.aging = Label(self.root, text="Старение", font=("BOWLER", 13), bg="black", fg="white")
        self.aging.place(x=1330,y=715)

        self.aging_checkbox = Checkbutton(self.root,
                                          font=("BOWLER", 12),
                                          bg="black",
                                          fg="white",
                                          variable=self.aging_enabled,
                                          command=self.draw_grid,
                                          selectcolor="black",
                                          activebackground="black",
                                          activeforeground="white",
                                          onvalue=True,
                                          offvalue=False
                                          )
        self.aging_checkbox.place(x=1445, y=712)

        self.death_aging_slider = Scale(
            self.root,
            from_=10, to=20,
            orient=HORIZONTAL,
            bg="black",
            fg="white",
            length=250,
        )
        self.death_aging_slider.set(10)
        self.death_aging_slider.place(x=1250, y=740)

        self.reset_rules_button = create_button(self.root, "Сброс правил", command=self.reset_rules, font=("BOWLER", 15))
        self.reset_rules_button.place(x=1289, y=800)

        self.start_button = create_button(self.root, "Старт", command=self.start, font=("BOWLER", 14))
        self.start_button.place(x=20, y=80)

        self.pattern_button = create_button(self.root, "Шаблоны", command=self.open_pattern, font=("BOWLER", 18))
        self.pattern_button.place(x=950, y=25)

        self.rules_button = create_button(self.root, "🛈", command=self.open_rules, font=("BOWLER", 30))
        self.rules_button.place(x=950, y=65)

        self.stop_button = create_button(self.root, "Стоп", command=self.stop, font=("BOWLER", 14))
        self.stop_button.place(x=105, y=80)

        self.reset_button = create_button(self.root, "Сброс", command=self.reset, font=("BOWLER", 14))
        self.reset_button.place(x=180, y=80)

        self.randomize_button = create_button(self.root, "Рандом", command=self.randomize, font=("BOWLER", 14))
        self.randomize_button.place(x=265, y=80)

        self.speed_label = Label(self.root, text=f"Скорость: {self.speed} мс", font=("BOWLER", 12), bg="black",
                                 fg="white")
        self.speed_label.place(x=390, y=60)

        self.live_label = Label(self.root, text="0", font=("BOWLER", 14), bg="black",
                                 fg="white")
        self.live_label.place(x=1530, y=190, anchor="ne")

        self.dead_label = Label(self.root, text="0", font=("BOWLER", 14), bg="black",
                                 fg="white")
        self.dead_label.place(x=1530, y=225, anchor="ne")

        self.born_label = Label(self.root, text="0", font=("BOWLER", 14), bg="black",
                                 fg="white")
        self.born_label.place(x=1530, y=260, anchor="ne")

        self.generation_label = Label(self.root, text="0", font=("BOWLER", 14), bg="black",
                                 fg="white")
        self.generation_label.place(x=1530, y=295, anchor="ne")

        self.speed_slider = Scale(
            self.root,
            from_=1000, to=10,
            orient=HORIZONTAL,
            bg="black",
            fg="white",
            length=250,
            command=self.update_speed
        )
        self.speed_slider.set(self.speed)
        self.speed_slider.place(x=390, y=80)

    def draw_grid(self):
        self.canvas.delete("all")
        aging_enabled = self.aging_enabled.get()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x]:
                    if aging_enabled:
                        age = self.age_grid[y][x]
                        self.gradient.set(False)
                        brightness = max(0, 255 - age * 10)
                        brightness = max(brightness, 55)
                        color = f'#00{brightness:02x}00'
                    elif self.gradient.get():
                        green_value = random.randint(130, 255)
                        color = f'#00{green_value:02x}00'
                    else:
                        color = "#00ff00"

                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill=color, outline="gray"
                    )
                else:
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="black", outline="gray"
                    )

    def open_pattern(self):
        if self.pattern_window is not None and self.pattern_window.winfo_exists():
            self.pattern_window.lift()
            return

        self.was_running = self.running

        if self.running:
            self.stop()

        self.pattern_window = Toplevel(self.root)
        self.pattern_window.resizable(False, False)
        self.pattern_window.title("Шаблоны")
        center_window(self.pattern_window, 1000, 500)

        image_paths = [
            "Images/шаблон.png",
            "Images/улей.png",
            "Images/пруд.png",
            "Images/каравай.png",
            "Images/двойной каравай.png",
            "Images/пекарня.png",
            "Images/ящик.png",
            "Images/баржа.png",
            "Images/длинная баржа.png",
            "Images/лодка.png",
            "Images/длинная лодка.png",
            "Images/лодочный бант.png",
            "Images/корабль.png",
            "Images/длинный корабль.png",
            "Images/корабельный бант.png",
            "Images/змея.png",
            "Images/знак интеграла.png",
            "Images/каноэ.png",
            "Images/авианосец.png",
            "Images/манго.png",
            "Images/рыболовный крючок.png",
    ]

        self.images = []

        for path in image_paths:
            try:
                img = PhotoImage(file=path)
                self.images.append(img)
            except Exception:
                pass

        if not self.images:
            return

        self.current_image_index = 0

        self.pattern_canvas = Canvas(self.pattern_window, width=1000, height=500)
        self.pattern_canvas.pack(fill="both", expand=True)

        self.pattern_canvas.create_image(0, 0, image=self.images[self.current_image_index], anchor="nw")

        self.slide_label = Label(
            self.pattern_window,
            text=f"Слайд {self.current_image_index + 1} из {len(self.images)}",
            font=("BOWLER", 12),
            background='black',
            foreground='white')
        self.slide_label.pack()

        two_signs = (self.pattern_window.register(lambda text: text == "" or (text.isdigit() and len(text) <= 2)), "%P")

        self.slide_entry = Entry(self.pattern_window, font=("BOWLER", 12), width=5, validate="key", validatecommand=two_signs)
        self.slide_entry.pack(pady=10)

        self.back_button = create_button(self.pattern_window, "  Назад", lambda: self.update_pattern_background(-1), font=("BOWLER", 12))
        self.next_button = create_button(self.pattern_window, "  Далее", lambda: self.update_pattern_background(1), font=("BOWLER", 12))
        self.close_button = create_button(self.pattern_window, "  Выход", self.on_pattern_window_close, font=("BOWLER", 12))
        self.go_button = create_button(self.pattern_window, "Перейти", self.go_to_pattern_slide, font=("BOWLER", 12))

        self.pattern_canvas.create_window(50, 460, anchor="nw", window=self.back_button)
        self.pattern_canvas.create_window(855, 460, anchor="nw", window=self.next_button)
        self.pattern_canvas.create_window(450, 460, anchor="nw", window=self.close_button)
        self.pattern_canvas.create_window(450, 420, anchor="nw", window=self.go_button)
        self.pattern_canvas.create_window(830, 10, anchor="nw", window=self.slide_label)
        self.pattern_canvas.create_window(420, 420, anchor="nw", window=self.slide_entry)

        self.pattern_window.protocol("WM_DELETE_WINDOW", self.on_pattern_window_close)

    def update_pattern_background(self, step):
        self.current_image_index = (self.current_image_index + step) % len(self.images)
        self.pattern_canvas.delete("all")
        self.pattern_canvas.create_image(0, 0, image=self.images[self.current_image_index], anchor="nw")
        self.slide_label.config(text=f"Слайд {self.current_image_index + 1} из {len(self.images)}")
        self.pattern_canvas.create_window(50, 460, anchor="nw", window=self.back_button)
        self.pattern_canvas.create_window(855, 460, anchor="nw", window=self.next_button)
        self.pattern_canvas.create_window(450, 460, anchor="nw", window=self.close_button)
        self.pattern_canvas.create_window(450, 420, anchor="nw", window=self.go_button)
        self.pattern_canvas.create_window(830, 10, anchor="nw", window=self.slide_label)
        self.pattern_canvas.create_window(420, 420, anchor="nw", window=self.slide_entry)

    def go_to_pattern_slide(self):
        try:
            slide_number = int(self.slide_entry.get())
            if 1 <= slide_number <= len(self.images):
                self.current_image_index = slide_number - 1
                self.update_pattern_background(0)
                self.slide_entry.delete(0, END)
        except ValueError:
            return

    def on_pattern_window_close(self):
        if self.pattern_window is not None:
            self.pattern_window.destroy()
            self.pattern_window = None

            if hasattr(self, 'was_running') and self.was_running:
                self.start()

    def open_rules(self):
        if self.rules_window is not None and self.rules_window.winfo_exists():
            self.rules_window.lift()
            return

        self.was_running = self.running

        if self.running:
            self.stop()

        self.rules_window = Toplevel(self.root)
        self.rules_window.resizable(False, False)
        self.rules_window.title("Обучение")
        center_window(self.rules_window, 1000, 500)

        self.rules_window.bg2 = PhotoImage(
            file="Images/backgr_rules.png")

        canvas1 = Canvas(self.rules_window, width=1000, height=500)
        canvas1.pack(fill="both", expand=True)
        canvas1.create_image(0, 0, image=self.rules_window.bg2, anchor="nw")

        button_exit_tut = create_button(
            self.rules_window,
            "Выход",
            command=self.on_rules_window_close,
            font=("BOWLER", 14)
        )
        canvas1.create_window(899, 470, anchor="nw", window=button_exit_tut)

        self.rules_window.protocol("WM_DELETE_WINDOW", self.on_rules_window_close)

    def on_rules_window_close(self):
        if self.rules_window is not None:
            self.rules_window.destroy()
            self.rules_window = None

            if hasattr(self, 'was_running') and self.was_running:
                self.start()

    def update_speed(self, value):
        self.speed = int(value)
        self.speed_label.config(text=f"Скорость: {self.speed} мс")

    def count_alive_cells(self):
        return sum(cell for row in self.grid for cell in row)

    def start(self):
        if not self.running:
            self.running = True
            self.run_generation()

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.running = False
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.total_born = 0
        self.total_died = 0
        self.prev_alive = 0
        self.generation_count = 0
        self.draw_grid()
        self.live_label.config(text="0")
        self.dead_label.config(text="0")
        self.born_label.config(text="0")
        self.generation_label.config(text="0")
        self.speed = 100
        self.speed_slider.set(self.speed)


    def randomize(self):
        self.grid = [[random.choice([0, 1]) for _ in range(self.width)] for _ in range(self.height)]
        self.draw_grid()

    def reset_rules(self):
            self.birth_threshold.set(3)
            self.born_slider.set(3)

            self.loneliness_threshold.set(2)
            self.death_alone_slider.set(2)

            self.overpopulation_threshold.set(3)
            self.death_over_slider.set(3)

            self.aging_enabled.set(False)
            self.death_aging_slider.set(10)

    def validate_rules(self, *_):
        alone = self.death_alone_slider.get()
        over = self.death_over_slider.get()
        born = self.born_slider.get()

        if alone >= over:
            self.death_alone_slider.set(over - 1)

        if born > over:
            self.born_slider.set(over)

        if born <= alone:
            self.born_slider.set(alone + 1)

        if born > over:
            self.death_over_slider.set(born)

        if born <= alone:
            self.death_alone_slider.set(born-1)

    def update_gradient_availability(self):
        if self.aging_enabled.get():
            self.gradient_checkbox.config(state="disabled")
        else:
            self.gradient_checkbox.config(state="normal")

    def run_generation(self):
        if not self.running:
            return

        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)

                if self.grid[y][x]:
                    if (neighbors < self.loneliness_threshold.get() or
                            neighbors > self.overpopulation_threshold.get()):
                        new_grid[y][x] = 0
                        self.age_grid[y][x] = 0
                    else:
                        new_grid[y][x] = 1
                        self.age_grid[y][x] += 1
                        if self.aging_enabled.get() and self.age_grid[y][x] >= self.death_aging_slider.get():
                            new_grid[y][x] = 0
                            self.age_grid[y][x] = 0
                else:
                    if neighbors == self.birth_threshold.get():
                        new_grid[y][x] = 1
                        self.age_grid[y][x] = 0

        self.grid = new_grid
        self.draw_grid()

        alive = self.count_alive_cells()
        delta = alive - self.prev_alive

        if delta > 0:
            self.total_born += delta
        elif delta < 0:
            self.total_died += abs(delta)

        self.generation_count += 1
        self.prev_alive = alive

        self.live_label.config(text=alive)
        self.dead_label.config(text=self.total_died)
        self.born_label.config(text=self.total_born)
        self.generation_label.config(text=self.generation_count)

        self.root.after(self.speed, self.run_generation)

    def count_neighbors(self, x, y):
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors += self.grid[ny][nx]
        return neighbors

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1 - self.grid[y][x]
            self.draw_grid()

menu_frame = Frame(window)
menu_frame.pack(fill="both", expand=True)

bg_main = PhotoImage(file="Images/backgr.png")
canvas = Canvas(menu_frame, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_main, anchor="nw")
canvas.create_text(770, 250, text="Жизнь", font=("BOWLER", 60, "bold"), fill="white")

button_start = create_button(menu_frame, "  Начать", start_game)
button_exit = create_button(menu_frame, "  Выход", window.destroy)
button_pattern = create_button(menu_frame, "Шаблоны", pattern)
button_info = create_button(menu_frame, "🛈", open_tutorial)

canvas.create_window(650, 330, anchor="nw", window=button_start)
canvas.create_window(658, 470, anchor="nw", window=button_exit)
canvas.create_window(650, 400, anchor="nw", window=button_pattern)
canvas.create_window(1485, 2, anchor="nw", window=button_info)

game_frame = Frame(window)

bg_start = PhotoImage(file="Images/backgr_game.png")
game_canvas = Canvas(game_frame, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
game_canvas.pack(fill="both", expand=True)
game_canvas.create_image(0, 0, image=bg_start, anchor="nw")

button_menu = create_button(game_frame, "Меню", show_menu, font=("BOWLER", 18))
game_canvas.create_window(1150, 25, anchor="nw", window=button_menu)

game = GameOfLife(game_canvas)

window.mainloop()