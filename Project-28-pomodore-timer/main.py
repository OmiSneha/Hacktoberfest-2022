from tkinter import *
import math
import winsound  # optional, only for Windows

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
is_paused = False
remaining_time = 0

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    label_mark.config(text="")
    reps = 0

# ---------------------------- TIMER START ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        label.config(text="Work", fg=GREEN)

# ---------------------------- PAUSE/RESUME ------------------------------- #
def pause_resume_timer():
    global is_paused, remaining_time
    if not is_paused:
        window.after_cancel(timer)
        btn_pause.config(text="Resume")
        is_paused = True
    else:
        btn_pause.config(text="Pause")
        is_paused = False
        count_down(remaining_time)

# ---------------------------- COUNTDOWN ------------------------------- #
def count_down(count):
    global remaining_time
    remaining_time = count
    minutes = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"{minutes:02}:{seconds}")

    if count > 0 and not is_paused:
        global timer
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        play_sound()
        start_timer()
        marks = "✓" * math.floor(reps / 2)
        label_mark.config(text=marks)

# ---------------------------- SOUND ------------------------------- #
def play_sound():
    try:
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    except:
        pass

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer ⏳")
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Labels
label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 35, "bold"))
label.grid(column=1, row=0)

label_mark = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 25, "bold"))
label_mark.grid(column=1, row=3)

# Buttons
btn_start = Button(text="Start", command=start_timer, highlightthickness=0)
btn_start.grid(column=0, row=2)

btn_pause = Button(text="Pause", command=pause_resume_timer, highlightthickness=0)
btn_pause.grid(column=1, row=2)

btn_reset = Button(text="Reset", command=reset_timer, highlightthickness=0)
btn_reset.grid(column=2, row=2)

window.mainloop()
