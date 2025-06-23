from tkinter import *
import random

BG_MAIN_PATH = "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/backgr.png"
BG_START_PATH = "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/фон.png"
FONT = ("BOWLER", 30)
BUTTON_BG = "black"
BUTTON_FG = "white"

window = Tk()
window.resizable(False, False)
window.title("Игра Жизнь")
window.state('zoomed')
window.iconbitmap()

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
    game.start() 

def pattern():
    pattern_window = Toplevel(window)
    pattern_window.resizable(False, False)
    pattern_window.title("Шаблоны")
    center_window(pattern_window, 1000, 500)

    image_paths = [
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/шаблон.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/улей.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/пруд.png",
        "C:/Users/userOK/OneDrive/Документах/Колледж/2 курс/УП/Для игры/каравай.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/двойной каравай.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/пекарня.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/ящик.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/баржа.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/длинная баржа.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/лодка.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/длинная лодка.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/лодочный бант.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/корабль.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/длинный корабль.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/корабельный бант.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/змея.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/знак интеграла.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/каноэ.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/длинная баржа.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/авианосец.png",
        "C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/манго.png",
    ]

    images = []
    for path in image_paths:
        try:
            img = PhotoImage(file=path)
            images.append(img)
        except Exception as e:
            print(f"Ошибка загрузки изображения {path}: {e}")

    if not images:
        print("Нет доступных изображений!")
        return

    current_image_index = 0

    canvas = Canvas(pattern_window, width=1000, height=500)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=images[current_image_index], anchor="nw")

    slide_label = Label(pattern_window, text=f"Слайд {current_image_index + 1} из {len(images)}", font=("BOWLER", 12), background='black', foreground='white')
    slide_label.pack()

    slide_entry = Entry(pattern_window, font=("BOWLER", 12), width=5)
    slide_entry.pack(pady=10) 

    def update_background(step):
        nonlocal current_image_index
        current_image_index = (current_image_index + step) % len(images)  
        canvas.delete("all") 
        canvas.create_image(0, 0, image=images[current_image_index], anchor="nw")

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
            else:
                print("Неверный номер слайда!")
        except ValueError:
            print("Введите корректное число!")

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

def open_tutorial():
    tutorial_window = Toplevel(window)
    tutorial_window.resizable(False, False)
    tutorial_window.title("Обучение")
    center_window(tutorial_window, 1000, 500)
    tutorial_window.bg2 = PhotoImage(file="C:/Users/userOK/OneDrive/Документы/Колледж/2 курс/УП/Для игры/backgr.png")
    canvas1 = Canvas(tutorial_window, width=1000, height=500)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=tutorial_window.bg2, anchor="nw")
    button_exit_tut = create_button(tutorial_window, "Закрыть", tutorial_window.destroy)
    canvas1.create_window(820, 430, anchor="nw", window=button_exit_tut)
    tutorial_text = """
    Добро пожаловать в обучение по игре Жизнь!

    Цель игры:
    Это исследование динамики популяции клеток на двумерной решетке. 
    Игра была разработана математиком Джоном Конвеем в 1970 году и не является игрой 
    в традиционном смысле, а скорее симуляцией. 

    Правила:
    1. Клетки: Каждая клетка на решетке может быть "живой" или "мертвой".
    2. Соседство: Каждая клетка имеет восемь соседей (горизонтально, вертикально и по диагонали).
    3. Правила эволюции:
   • Если живая клетка имеет 2 или 3 живых соседа, она остается живой; иначе она умирает (от перенаселения или одиночества).
   • Если мертвая клетка имеет ровно 3 живых соседа, она становится живой (в результате размножения).

    Нажмите 'Закрыть', чтобы вернуться в игру.
    """
    label = Label(tutorial_window, text=tutorial_text, justify="center", padx=10, pady=10, font=('BOWLER', 11), fg="white", bg="black")
    canvas1.create_window(500, 200, anchor="center", window=label)

class GameOfLife:
    def __init__(self, root, width=100, height=100, cell_size=20):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.dead_color = "black" 
        self.max_age = 10 

        self.grid = [[(0, 0) for _ in range(width)] for _ in range(height)]

        self.canvas = Canvas(root, width=width * cell_size, height=height * cell_size)
        self.canvas.pack()

        self.speed = 100 

        self.running = False
        self.draw_grid()
        self.create_buttons() 
        self.canvas.bind("<Button-1>", self.toggle_cell)  

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                state, age = self.grid[y][x]
                if state:
                    color = self.age_to_color(age)
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill=color
                    )
                else:
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill=self.dead_color, outline="gray"
                    )

    def age_to_color(self, age):
        max_brightness = 255  
        brightness = max_brightness - int((age / self.max_age) * max_brightness)
        return f"#{brightness:02x}{brightness:02x}00" 

    def create_buttons(self):
        self.start_button = create_button(self.root, "Старт", command=self.start, font=("BOWLER", 14))
        self.start_button.place(x=50, y=50)

        self.stop_button = create_button(self.root, "Стоп", command=self.stop, font=("BOWLER", 14))
        self.stop_button.place(x=150, y=50)

        self.reset_button = create_button(self.root, "Сброс", command=self.reset, font=("BOWLER", 14))
        self.reset_button.place(x=250, y=50)

        self.randomize_button = create_button(self.root, "Рандом", command=self.randomize, font=("BOWLER", 14))
        self.randomize_button.place(x=350, y=50)

        self.speed_label = Label(self.root, text=f"Скорость: {self.speed} мс", font=("BOWLER", 12), bg="black",
                                 fg="white")
        self.speed_label.place(x=50, y=100)

        self.speed_slider = Scale(
            self.root,
            from_=1000, to=10, 
            orient=HORIZONTAL,
            length=300,
            command=self.update_speed
        )
        self.speed_slider.set(self.speed) 
        self.speed_slider.place(x=50, y=130)

    def update_speed(self, value):
        self.speed = int(value)
        self.speed_label.config(text=f"Скорость: {self.speed} мс")

    def start(self):
        self.running = True
        self.run_generation()

    def stop(self):
        self.running = False

    def reset(self):
        self.grid = [[(0, 0) for _ in range(self.width)] for _ in range(self.height)]
        self.draw_grid()

    def randomize(self):
        self.grid = [[(random.choice([0, 1]), 0) if random.choice([0, 1]) else (0, 0) for _ in range(self.width)] for _
                     in range(self.height)]
        self.draw_grid()

    def run_generation(self):
        if not self.running:
            return

        new_grid = [[(0, 0) for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                state, age = self.grid[y][x]
                neighbors = self.count_neighbors(x, y)

                if state:
                    if neighbors < 2 or neighbors > 3 or age >= self.max_age:
                        new_grid[y][x] = (0, 0)
                    else:
                        new_grid[y][x] = (1, age + 1)
                else:
                    if neighbors == 3:
                        new_grid[y][x] = (1, 1)
                    else:
                        new_grid[y][x] = (0, 0)

        self.grid = new_grid
        self.draw_grid()
        self.root.after(self.speed, self.run_generation) 

    def count_neighbors(self, x, y):
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors += self.grid[ny][nx][0]
        return neighbors

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            state, age = self.grid[y][x]
            self.grid[y][x] = (1 - state, 1 if state == 0 else 0)
            self.draw_grid()

menu_frame = Frame(window)
menu_frame.pack(fill="both", expand=True)

bg_main = PhotoImage(file=BG_MAIN_PATH)
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

bg_start = PhotoImage(file=BG_START_PATH)
game_canvas = Canvas(game_frame, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
game_canvas.pack(fill="both", expand=True)
game_canvas.create_image(0, 0, image=bg_start, anchor="nw")

button_menu = create_button(game_frame, "Меню", show_menu)
game_canvas.create_window(12, 2, anchor="nw", window=button_menu)

game = GameOfLife(game_canvas)

window.mainloop()
