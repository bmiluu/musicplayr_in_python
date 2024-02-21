from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import *
import pygame
import os
from mutagen.mp3 import MP3
import threading

root = Tk()
root.iconbitmap("assets/boombox.ico")
root.title("Music Player")
root.geometry("600x350")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

current_position = 0
songs = []
current_song = ""
paused = False

def update_progress_bar():
    global current_position, paused
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_position = pygame.mixer.music.get_pos() / 1000  
            pbar["value"] = current_position

            if current_position >= pbar["maximum"]:
                stop_music()
                pbar["value"] = 0

pt = threading.Thread(target=update_progress_bar)
pt.daemon = True
pt.start()

def load_music():
    global current_song
    root.directory = filedialog.askdirectory()
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song, paused
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
        audio = MP3(os.path.join(root.directory, current_song))
        song_duration = audio.info.length
        pbar["maximum"] = song_duration
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def stop_music():
    global paused
    pygame.mixer.music.stop()
    paused = False

def next_music():
    global current_song, paused
    try:
        songlist.select_clear(0, END)
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global current_song, paused
    try:
        songlist.select_clear(0,END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label="Select Folder", command=load_music)
menubar.add_cascade(label="Select Music", menu=organise_menu)

songlist = Listbox(root, bg="black", fg="white",width="100",height="15")
songlist.pack()

play_btn_image = PhotoImage(file= "assets/play.png")
pause_btn_image = PhotoImage(file= "assets/pause.png")
next_btn_image = PhotoImage(file= "assets/next.png")
prev_btn_image = PhotoImage(file= "assets/previous.png")

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0,column=1,padx=7,pady=10)
pause_btn.grid(row=0,column=2,padx=7,pady=10)
next_btn.grid(row=0,column=3,padx=7,pady=10)
prev_btn.grid(row=0,column=0,padx=7,pady=10)

pbar = Progressbar(root, length=300, mode="determinate")
pbar.pack(pady=10)

root.mainloop()