from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
PURPLE = "#c8a1e0"
BLUE = "#478ccf"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
timer = None
cycles = 0
play_program = 1
play_timer = True
count_min = 0
count_sec = 0



# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    global cycles
    cycles = 0
    start_button.config(state="normal")

# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global cycles
    cycles += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if cycles == 1 or cycles == 3 or cycles == 5 or cycles == 7:
        count_down(work_sec)
        title_label.config(text="WORK", fg=GREEN)
        focus_window("off")
    elif cycles == 8:
        count_down(long_break_sec)
        title_label.config(text="BREAK", fg=RED)
        focus_window("on")
    elif cycles == 2 or cycles == 4 or cycles == 6:
        count_down(short_break_sec)
        title_label.config(text="BREAK", fg=PINK)
        focus_window("on")
    else:
        pass
    start_button.config(state="disabled")
    pause_button.config(state="active")
    reset_button.config(state="active")

# ---------------------------- PAUSE / RESUME ------------------------------- #

def pause():
    global current_status_label
    global current_status_label_color

    current_status_label = title_label.cget("text")
    current_status_label_color = title_label.cget("fg")
    window.after_cancel(timer)
    pause_button.config(text="▶️Resume", command=resume)
    title_label.config(text="PAUSED ", fg=BLUE, font=(FONT_NAME, 36, "bold"))


def resume():
    pause_button.config(text="⏸️Pause", command=pause)
    saved_data = count_min * 60 + int(count_sec)
    count_down(saved_data)
    title_label.config(text=current_status_label, fg=current_status_label_color, font=(FONT_NAME, 36, "bold"))





# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global cycles
    global count_min
    global count_sec
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)


    if count == 0:
        window.bell()
        start_timer()
    if cycles == 2:
        checkmark = "✔️"
        check_marks.config(text=checkmark)
    if cycles == 4:
        checkmark = "✔️✔️"
        check_marks.config(text=checkmark)
    if cycles == 6:
        checkmark = "✔️✔️✔️"
        check_marks.config(text=checkmark)
    if cycles == 8:
        checkmark = "✔️✔️✔️✔️"
        check_marks.config(text=checkmark)
    if cycles > 8:
        window.after_cancel(timer)
        title_label.config(text="Great Work :)", fg=PURPLE)
        canvas.itemconfig(timer_text, text="00:00")
        start_button.config(state=DISABLED)
        pause_button.config(state=DISABLED)


# ---------------------------- UI SETUP ------------------------------- #

def focus_window(option):
    if option == "on":
        window.deiconify()
        window.focus_force()
        window.attributes('-topmost', 1)
    elif option == "off":
        window.attributes('-topmost', 0)

window = Tk()
window.title("Pomodoro")
window.minsize(width=400, height=445)
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(height=224, width=210, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=image)
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 36, "bold"))
canvas.grid(column=1, row=1)


title_label = Label()
title_label.config(text="Timer", fg=GREEN, font=(FONT_NAME, 36, "bold"), bg=YELLOW)
title_label.grid(column=1, row=0)

start_button = Button()
start_button.config(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

pause_button = Button()
pause_button.config(text="⏸️Pause", command=pause, state=DISABLED)
pause_button.grid(column=1, row=4)
pause_button.lift()

reset_button = Button()
reset_button.config(text="Reset", command=reset_timer, state=DISABLED)
reset_button.grid(column=2, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)

# Check if the program is paused or not.

if play_timer:
    start_button.config(command=start_timer)
    reset_button.config(command=reset_timer)
else:
    pass


window.mainloop()
