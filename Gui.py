from tkinter import *
import tkinter as tk 
import tkinter.ttk as ttk
import main_def
import math

stream_count = int
STREAM_MAX = 4
MAX_VOLUME = 512

port_padx = 10
sound_padx = 17
sound_button_padx = 15
main_sound_button_padx = 16

dec_col = 1
main_col = 2
inc_col = 3
sound_col = 4
str_name_col = 5
port_col = 6


def inc_dec_sound(p, i):
    if p == "P1":
        Sv = int(sound_level_1.get())
        sl = sound_level_1
        port = port_player_1.get()
    elif p == "P2":
        Sv = int(sound_level_2.get())
        sl = sound_level_2
        port = port_player_2.get()
    elif p == "P3":
        Sv = int(sound_level_3.get())
        sl = sound_level_3
        port = port_player_3.get()
    elif p == "P4":
        Sv = int(sound_level_4.get())
        sl = sound_level_4
        port = port_player_4.get()
    else:
        return "Error knowing which inc sound button was pressed"

    if Sv >= 200 and i == "inc":
        return
    else:
        volume = main_def.get_stream_info({p: port}, pw_entry.get())
        if volume[p] <= 10:
            return
        else:
            if i == "inc":
                main_def.increment_sound(port, pw_entry.get())
            elif i == "dec":
                main_def.decrement_sound(port, pw_entry.get())

            volume = main_def.get_stream_info({p: port}, pw_entry.get())
            percent = sound_return_percentage(volume)
            sl.delete(0, END)
            sl.insert(0, percent)

def refresh_stream(p):
    if p == "P1":
        port = port_player_1.get()
        name = player1.get()
    elif p == "P2":
        port = port_player_2.get()
        name = player2.get()
    elif p == "P3":
        port = port_player_3.get()
        name = player3.get()
    elif p == "P4":
        port = port_player_4.get()
        name = player4.get()
    else:
        return "Error getting players stream to refresh."
    
    playlist_id = main_def.get_vlc_playlist_info(port, name, pw_entry.get())
    main_def.setup_refresh_commands(port, playlist_id, pw_entry.get())
    

def main_sound(button):
    port = get_ports(button)
    sound_level = get_sound_percent(button)
    sound_decimal = sound_percent_decimal(sound_level)
    
    if port == "Port get error":
        None
    else:
        volumes = main_def.get_stream_info(port, pw_entry.get())
        main_def.change_main_sound(volumes, port, sound_decimal, pw_entry.get())

def get_ports(p):
    ports = {}
    if p == "P1":
        ports.update({"Main": port_player_1.get()})
    elif p == "P2":
        ports.update({"Main": port_player_2.get()})
    elif p == "P3":
        ports.update({"Main": port_player_3.get()})
    elif p == "P4":
        ports.update({"Main": port_player_4.get()})
    else:
        return "Port get error"
    

    if port_player_1.get() != "" and p != 'P1':
        ports.update({"P1": port_player_1.get()})
    if port_player_2.get() != "" and p != 'P2':
        ports.update({"P2": port_player_2.get()})
    if port_player_3.get() != "" and p != 'P3':
        ports.update({"P3": port_player_3.get()})
    if port_player_4.get() != "" and p != 'P4':
        ports.update({"P4": port_player_4.get()})

    return ports

def get_sound_percent(p):
    if p == "P1":
        return sound_level_1.get()
    elif p == "P2":
        return sound_level_2.get()
    elif p == "P3":
        return sound_level_3.get()
    elif p == "P4":
        return sound_level_4.get()
    else:
        return "Sound Percent get error"


def sound_percent_decimal(s):
    num = int(s)
    dec_value = 256 * (num / 100.0)
    if dec_value >= MAX_VOLUME:
        None
    else:    
        return math.ceil(dec_value)
    
def sound_return_percentage(s):
    for key, value in s.items():
        num = int(value)
        per_value = (num / 256) * 100
    if per_value > 201:
        return 200
    else:
        return round(per_value)



root = Tk()
root.title("Pyre\'s VLC Restream Helper")
root.config(bg="light gray")
root.geometry("600x425+50+50")
root.rowconfigure(9, minsize=300, weight=1)
root.columnconfigure(6, minsize=200, weight=1)

style = ttk.Style()
style.theme_use('alt')
style.configure('Tbutton', background="grey")
style.configure("TLabel", background='light grey')
style.map('Tbutton', background=[('active', 'grey')])
style.configure("TFrame", background="green")

refresh_frame = ttk.Frame(root)
refresh_frame.rowconfigure(3, weight=2)
refresh_frame.columnconfigure(2, weight=2)


refresh = tk.IntVar()

def refresh_init():
    if refresh.get() == 0:
        refresh_frame.grid_forget()
    else:
        refresh_frame.grid(column=1, columnspan=4, row=8, rowspan=10, sticky=NW)


pw = tk.StringVar()

player1 = tk.StringVar()
player2 = tk.StringVar()
player3 = tk.StringVar()
player4 = tk.StringVar()

port_player_1 = tk.StringVar()
port_player_2 = tk.StringVar()
port_player_3 = tk.StringVar()
port_player_4 = tk.StringVar()

sound_player1 = tk.StringVar()
sound_player2 = tk.StringVar()
sound_player3 = tk.StringVar()
sound_player4 = tk.StringVar()

pw_entry = ttk.Entry(root, textvariable=pw, show="*", width=10)
pw_entry.grid(column=1, row=1, padx=10, pady=10, sticky=W)

pw_label = ttk.Label(root, text="<~~ Password")
pw_label.grid(column=2, row=1, padx=10, pady=10, sticky=W)

stream_metadata_label = ttk.Label(root, text="Stream Name Metadata")
stream_metadata_label.grid(column=str_name_col, row=2, padx=10, pady=10, sticky=(N, W))

port_label = ttk.Label(root, text="Port")
port_label.grid(column=port_col, row=2, padx=16, pady=5, sticky=W)

sound_level_label = ttk.Label(root, text="Sound %")
sound_level_label.grid(column=sound_col, row=2, padx=10, pady=4, sticky=W)

dec_sound_label = ttk.Label(root, text="Dec Sound")
dec_sound_label.grid(column=dec_col, row=2, padx=10, pady=5, sticky=W)

main_sound_label = ttk.Label(root, text="Set Main Sound")
main_sound_label.grid(column=main_col, row=2, padx=10, pady=5, sticky=W)

inc_sound_label = ttk.Label(root, text="Inc Sound")
inc_sound_label.grid(column=inc_col, row=2, padx=14, pady=5, sticky=W)

stream_metadata_entry_1 = ttk.Entry(root, textvariable=player1)
stream_metadata_entry_1.grid(column=str_name_col, row=3, padx=10, pady=10)

stream_metadata_entry_2 = ttk.Entry(root, textvariable=player2)
stream_metadata_entry_2.grid(column=str_name_col, row=4, padx=10, pady=10)

stream_metadata_entry_3 = ttk.Entry(root, textvariable=player3)
stream_metadata_entry_3.grid(column=str_name_col, row=5, padx=10, pady=10)

stream_metadata_entry_4 = ttk.Entry(root, textvariable=player4)
stream_metadata_entry_4.grid(column=str_name_col, row=6, padx=10, pady=10)

port_1 = ttk.Entry(root, textvariable=port_player_1, width=5)
port_1.grid(column=port_col, row=3, padx=port_padx, pady=10, sticky=W)

port_2 = ttk.Entry(root, textvariable=port_player_2, width=5)
port_2.grid(column=port_col, row=4, padx=port_padx, pady=10, sticky=W)

port_3 = ttk.Entry(root, textvariable=port_player_3, width=5)
port_3.grid(column=port_col, row=5, padx=port_padx, pady=10, sticky=W)

port_4 = ttk.Entry(root, textvariable=port_player_4, width=5)
port_4.grid(column=port_col, row=6, padx=port_padx, pady=10, sticky=W)

sound_level_1 = ttk.Entry(root, textvariable=sound_player1, width=5)
sound_level_1.grid(column=sound_col, row=3, padx=sound_padx, pady=10, sticky=W)

sound_level_2 = ttk.Entry(root, textvariable=sound_player2, width=5)
sound_level_2.grid(column=sound_col, row=4, padx=sound_padx, pady=10, sticky=W)

sound_level_3 = ttk.Entry(root, textvariable=sound_player3, width=5)
sound_level_3.grid(column=sound_col, row=5, padx=sound_padx, pady=10, sticky=W)

sound_level_4 = ttk.Entry(root, textvariable=sound_player4, width=5)
sound_level_4.grid(column=sound_col, row=6, padx=sound_padx, pady=10, sticky=W)

player1_dec_sound = ttk.Button(root, text="Dec P1", width=7, command=lambda p="P1", i="dec" : inc_dec_sound(p, i))
player1_dec_sound.grid(column=dec_col, row=3, padx=main_sound_button_padx, pady=10, sticky=W)

player2_dec_sound = ttk.Button(root, text="Dec P2", width=7, command=lambda p="P2", i="dec" : inc_dec_sound(p, i))
player2_dec_sound.grid(column=dec_col, row=4, padx=sound_button_padx, pady=10, sticky=W)

player3_dec_sound = ttk.Button(root, text="Dec P3", width=7, command=lambda p="P3", i="dec" : inc_dec_sound(p, i))
player3_dec_sound.grid(column=dec_col, row=5, padx=sound_button_padx, pady=10, sticky=W)

player4_dec_sound = ttk.Button(root, text="Dec P4", width=7, command=lambda p="P4", i="dec" : inc_dec_sound(p, i))
player4_dec_sound.grid(column=dec_col, row=6, padx=sound_button_padx, pady=10, sticky=W)

player1_main_sound = ttk.Button(root, text="Main P1", command= lambda p="P1" : main_sound(p))
player1_main_sound.grid(column=main_col, row=3, padx=main_sound_button_padx, pady=10, sticky=W)

player2_main_sound = ttk.Button(root, text="Main P2", command=lambda p="P2" : main_sound(p))
player2_main_sound.grid(column=main_col, row=4, padx=main_sound_button_padx, pady=10, sticky=W)

player3_main_sound = ttk.Button(root, text="Main P3", command=lambda p="P3" : main_sound(p))
player3_main_sound.grid(column=main_col, row=5, padx=main_sound_button_padx, pady=10, sticky=W)

player4_main_sound = ttk.Button(root, text="Main P4", command=lambda p="P4" : main_sound(p))
player4_main_sound.grid(column=main_col, row=6, padx=main_sound_button_padx, pady=10, sticky=W)

player1_inc_sound = ttk.Button(root, text="Inc P1", width=7, command=lambda p="P1", i="inc" : inc_dec_sound(p, i))
player1_inc_sound.grid(column=inc_col, row=3, padx=main_sound_button_padx, pady=10, sticky=W)

player2_inc_sound = ttk.Button(root, text="Inc P2", width=7, command=lambda p="P2", i="inc" : inc_dec_sound(p, i))
player2_inc_sound.grid(column=inc_col, row=4, padx=sound_button_padx, pady=10, sticky=W)

player3_inc_sound = ttk.Button(root, text="Inc P3", width=7, command=lambda p="P3", i="inc" : inc_dec_sound(p, i))
player3_inc_sound.grid(column=inc_col, row=5, padx=sound_button_padx, pady=10, sticky=W)

player4_inc_sound = ttk.Button(root, text="Inc P4", width=7, command=lambda p="P4", i="inc" : inc_dec_sound(p, i))
player4_inc_sound.grid(column=inc_col, row=6, padx=sound_button_padx, pady=10, sticky=W)

refresh_stream_cb = ttk.Checkbutton(root, text="Refresh Stream", onvalue=1, offvalue=0, variable=refresh, command=refresh_init)
refresh_stream_cb.grid(column=1, row=7, padx=10, pady=10, columnspan=2, sticky=W)

player1_refresh = ttk.Button(refresh_frame, text="P1 Stream", command= lambda p="P1" : refresh_stream(p))
player1_refresh.grid(column=1, row=1, padx=main_sound_button_padx, pady=10, sticky=W)

player2_refresh = ttk.Button(refresh_frame, text="P2 Stream", command=lambda p="P2" : refresh_stream(p))
player2_refresh.grid(column=2, row=1, padx=main_sound_button_padx, pady=10, sticky=W)

player3_refresh = ttk.Button(refresh_frame, text="P3 Stream", command=lambda p="P3" : refresh_stream(p))
player3_refresh.grid(column=1, row=2, padx=main_sound_button_padx, pady=10, sticky=W)

player4_refresh = ttk.Button(refresh_frame, text="P4 Stream", command=lambda p="P4" : refresh_stream(p))
player4_refresh.grid(column=2, row=2, padx=main_sound_button_padx, pady=10, sticky=W)


root.mainloop()
