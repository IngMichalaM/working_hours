import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import timedelta, date

""" Track your working time. Start by pressing 'Start', stop/pause by pressing 'Stop'.
    'Save' button saves the current day / start time / stip time / elapsed time / comment 
    to the curretn diretory to the file 'working_hours.txt'.
    Works also when the computer is asleep. """

# ToDo: Sound alert after 8 h.

root = tk.Tk()
root.title("Working hours")
root.option_add("*tearOff", False)

# define vars to hold time values
start_time = 0
stop_time = 0
elapsed_time = 0
time_to_display = '00:00:00'

# define variables to hold "display" values
# time_to_display = "00:00:00"
display_seconds = tk.StringVar()
display_seconds.set('00')

display_minutes = tk.StringVar()
display_minutes.set("00")

display_hours = tk.StringVar()
display_hours.set('00')

# variable to hold stopwatch status
status = "stopped"


def reset_watch():
    global status, elapsed_time
    """ cannot reset while 'started' """

    if status == 'stopped':
        elapsed_time = 0
        label_elapsed_time.configure(text="0:00:00")


def start_watch():
    global status, start_time

    # elapsed_time - default 0, otherwise the time for the previous start-stop lap
    if status == 'stopped':
        status = 'started'
        # if started - nothing

        start_time = time.time()

        start_button.configure(text="Runnning ... ")
        display_time()


def stop_watch():
    global status, start_time, elapsed_time, stop_time

    if status == 'started':
        status = "stopped"

        stop_time = time.time()
        elapsed_time = elapsed_time + stop_time - start_time

        start_button.configure(text="Start")
        display_time()


def display_time():
    global status, start_time, time_to_display, elapsed_time

    while status == 'started':
        try:
            time_to_display_s = time.time() - start_time + elapsed_time
            time_to_display = str(timedelta(seconds=time_to_display_s))
            time_to_display_now = time_to_display.split('.')[0]
            # print(f'The time to display is {time_to_display_now}')
            label_elapsed_time.configure(text=time_to_display_now)
            root.update()
            time.sleep(1)
        except tk.TclError:
            break

    if status == 'stopped':
        time_to_display = str(timedelta(seconds=elapsed_time))
        time_to_display_now = time_to_display.split('.')[0]
        label_elapsed_time.configure(text=time_to_display_now)
        root.update()


def save_time_to_file():
    global status, start_time, elapsed_time, stop_time

    current_directory = os.getcwd()
    file_name = 'working_hours.txt'
    filename = os.path.join(current_directory, file_name)

    today = date.today()

    # today date - start time - stop time - elapsed time - working status

    time_to_display = str(timedelta(seconds=elapsed_time))
    time_to_display_now = time_to_display.split('.')[0]

    work_time_target = 8 * 60 * 60
    if elapsed_time >= work_time_target:  # 8 working hours
        working_status = "OK. You've worked well."
    elif elapsed_time == 0:
        messagebox.showinfo("Missing end time", "Have you pressed the Stop button? If not, do it now please.")
        return
    else:
        delta_work_time = work_time_target - elapsed_time
        working_status = f"Not that great today. You should have worked more (missing {time.strftime('%H:%M:%S', time.gmtime(delta_work_time))})."

    with open(filename, "a+") as file:  # a+ create teh file if it does not exist
        file.write(';'.join([str(today), time.strftime('%H:%M:%S', time.localtime(start_time)), time.strftime('%H:%M:%S', time.localtime(stop_time)), time_to_display_now, working_status]))
        file.write('\n')

    messagebox.showinfo("Saved", "Your data are saved now. You can go on or quit/close the window.")


def confirm_quit():

    confirm = messagebox.askyesno(
        message="Are you sure you want to quit?",
        title="Confirm Quit"
    )

    if confirm:
        root.destroy()
    else:
        return


# ------------------------------------------------------

buttons_width = 10
buttons_height = 2

f = tk.Frame(root)
f.pack(fill="both", expand=True, padx=1, pady=(4, 0))

start_button = tk.Button(f, bg="green", text='Start', width=buttons_width, height=buttons_height,
                         command=lambda: start_watch())
start_button.pack(side='left', fill='x', expand=False)

stop_button = tk.Button(f, bg="red", text='Stop', width=buttons_width, height=buttons_height,
                        command=lambda: stop_watch())
stop_button.pack(side='left', fill='x', expand=False)

reset_button = tk.Button(f, bg="plum2", text='Reset', width=buttons_width, height=buttons_height,
                         command=lambda: reset_watch())
reset_button.pack(side='left', fill='x', expand=False)

quit_button = tk.Button(f, fg='white', bg="black", text='Quit', width=buttons_width, height=buttons_height,
                        command=lambda : confirm_quit())
quit_button.pack(side='left', fill='x', expand=False)

save_button = tk.Button(f, fg='black', bg="yellow", text='Save', width=buttons_width, height=buttons_height,
                        command=lambda: save_time_to_file())
save_button.pack(side='left', fill='x', expand=False)

label = tk.Label(root, text='Elapsed time', font="Verdana 20 bold")
label.pack(side='top', fill="both")

label_elapsed_time = tk.Label(root, text=time_to_display, font="Verdana 20 bold")
label_elapsed_time.pack(side='top', fill="both")

today_time_label = tk.Label(root, text=time.strftime("%d/%m/%Y"), font="Verdana 10 bold")
today_time_label.pack(side='bottom', fill="both")

root.mainloop()
