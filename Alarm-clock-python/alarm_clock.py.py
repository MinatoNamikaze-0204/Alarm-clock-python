from tkinter import *
from tkinter import ttk
import datetime
import time
import winsound
from threading import Thread, Event

# Create main window
root = Tk()
root.geometry("400x300")
root.title("Alarm Clock")
root.config(bg='lightblue')

# Configure styles for widgets
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 14))
style.configure('Title.TLabel', font=('Helvetica', 20, 'bold'), foreground='red')
style.configure('Time.TLabel', font=('Helvetica', 24))
style.configure('TButton', font=('Helvetica', 12), padding=10)

# Title label
title_label = ttk.Label(root, text="Alarm Clock", style='Title.TLabel')
title_label.pack(pady=10)

# Current time display
current_time_label = ttk.Label(root, style='Time.TLabel')
current_time_label.pack()

def update_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_time_label.config(text=f"Current Time: {current_time}")
    root.after(1000, update_time)

update_time()

# Frame for time selection
frame = ttk.Frame(root)
frame.pack(pady=10)

# Initialize spinbox values with current time
now = datetime.datetime.now()
initial_hour = f"{now.hour:02d}"
initial_minute = f"{now.minute:02d}"
initial_second = f"{now.second:02d}"

# Hour spinbox
hour_label = ttk.Label(frame, text="Hour:")
hour_label.grid(row=0, column=0, padx=5)
hour_spinbox = ttk.Spinbox(frame, from_=0, to=23, width=5, format="%02.0f")
hour_spinbox.set(initial_hour)
hour_spinbox.grid(row=0, column=1, padx=5)

# Minute spinbox
minute_label = ttk.Label(frame, text="Minute:")
minute_label.grid(row=0, column=2, padx=5)
minute_spinbox = ttk.Spinbox(frame, from_=0, to=59, width=5, format="%02.0f")
minute_spinbox.set(initial_minute)
minute_spinbox.grid(row=0, column=3, padx=5)

# Second spinbox
second_label = ttk.Label(frame, text="Second:")
second_label.grid(row=0, column=4, padx=5)
second_spinbox = ttk.Spinbox(frame, from_=0, to=59, width=5, format="%02.0f")
second_spinbox.set(initial_second)
second_spinbox.grid(row=0, column=5, padx=5)

# Alarm status label
alarm_set_label = ttk.Label(root, text="No alarm set")
alarm_set_label.pack(pady=10)

# Button frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Initialize stop event
stop_event = None

# Function to set the alarm
def set_alarm():
    global stop_event
    stop_event = Event()
    set_alarm_time = f"{hour_spinbox.get()}:{minute_spinbox.get()}:{second_spinbox.get()}"
    alarm_set_label.config(text=f"Alarm set for: {set_alarm_time}")
    set_button.config(state=DISABLED)
    cancel_button.config(state=NORMAL)
    t1 = Thread(target=alarm, args=(set_alarm_time, stop_event))
    t1.start()

# Function to cancel the alarm
def cancel_alarm():
    global stop_event
    if stop_event is not None:
        stop_event.set()
        reset_ui()

# Function to check alarm time
def alarm(set_alarm_time, stop_event):
    while not stop_event.is_set():
        time.sleep(1)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == set_alarm_time:
            print("Time to Wake up!")
            try:
                winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            except:
                print("Sound file not found; alarm triggered without sound")
            root.after(0, reset_ui)
            break

# Function to reset UI after alarm or cancellation
def reset_ui():
    set_button.config(state=NORMAL)
    cancel_button.config(state=DISABLED)
    alarm_set_label.config(text="No alarm set")

# Set alarm button
set_button = ttk.Button(button_frame, text="Set Alarm", command=set_alarm)
set_button.pack(side=LEFT, padx=10)

# Cancel alarm button
cancel_button = ttk.Button(button_frame, text="Cancel Alarm", command=cancel_alarm, state=DISABLED)
cancel_button.pack(side=LEFT, padx=10)

# Start Tkinter event loop
root.mainloop()