from tkinter import *
import math
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

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    """Resets the timer back to 00:00, with the original title. Resets the number of reps
    and check marks. The timer returns to initial state."""

    # stops timer from counting down
    window.after_cancel(timer)

    # timer_text 00:00
    canvas.itemconfig(timer_text, text="00:00")
    # title_label "Timer
    timer_label.config(text="Timer", fg=GREEN)
    # reset check_marks
    global reps
    reps = 0
    check_marks.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    """Starts timer. Depending on number of reps, the work, break, or long break timer starts."""

    global reps

    # convert to seconds
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # for each even number of reps, starting at 0, start work timer
    if reps % 2 == 0:
        count_down(work_sec)
        timer_label.config(text="Work", fg=GREEN, font=(FONT_NAME, 50, "bold"), bg=YELLOW)
    # for each odd number of reps, start break timer
    # for each 7th rep, start longer break timer
    elif reps % 7 == 0:
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=GREEN, font=(FONT_NAME, 50, "bold"), bg=YELLOW)
    else:
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=PINK, font=(FONT_NAME, 50, "bold"), bg=YELLOW)

    reps += 1


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """Starts count down and changes timer accordingly."""

    count_min = math.floor(count / 60)
    count_sec = count % 60

    # maintains 0:00 format
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # changes timer accordingly
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # if there is remaining time, continue count; if not, start timer again
    if count > 0:
        global timer
        # after 1 second, count_down; then, decrement count
        timer = window.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)

        # add check mark for every work time accomplished
        for i in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=2, column=2)

timer_label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50, "bold"), bg=YELLOW)
timer_label.grid(row=1, column=2)

start_button = Button(text="Start", borderwidth=0, font=(FONT_NAME, 10, "normal"),command=start_timer)
start_button.grid(row=3, column=1)

reset_button = Button(text="Reset", borderwidth=0, font=(FONT_NAME, 10, "normal"), command=reset_timer)
reset_button.grid(row=3, column=3)

check_marks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
check_marks.grid(row=4, column=2)


window.mainloop()