from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import pygame
import os
from mutagen.mp3 import MP3
import threading

root = Tk()
root.config(bg="white")
root.iconbitmap("assets/boombox.ico")
root.title("Music Player")
root.geometry("600x500")


pygame.mixer.init()

title = Label(root, text="Music Player", font=("TkDefaultFont", 30, "bold"), bg="white")
title.pack(pady=10)


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

btn_select_folder = ctk.CTkButton(root, text="Select Music Folder", 
                                  command=load_music,
                                  font=("TkDefaultFont", 18),
                                  text_color="black",
                                  border_color="black",
                                  border_width=1, 
                                  fg_color="white",
                                  hover_color="white"
                                 )

btn_select_folder.pack(pady = 10)

switch_value = True

def toggle(): 
  
    global switch_value 
    if switch_value == True: 
        songlist.config(bg="#534e69", fg="white")
        control_frame.config(bg="#534e69")
        play_btn.config(bg="#534e69")
        pause_btn.config(bg="#534e69")
        next_btn.config(bg="#534e69")
        prev_btn.config(bg="#534e69")
        title.config(bg="#26242f", fg="white")
        btn_select_mode.configure(fg_color="#26242f", 
                      border_color="white",
                      text_color = "white",
                      hover_color = "#26242f")
        btn_select_folder.configure(fg_color="#26242f", 
                      border_color="white",
                      text_color = "white",
                      hover_color = "#26242f") 
        
          
        # Changes the window to dark theme 
        root.config(bg="#26242f")   
        switch_value = False
  
    else: 
        songlist.config(bg="white", fg="black")
        control_frame.config(bg="white")
        play_btn.config(bg="white")
        pause_btn.config(bg="white")
        next_btn.config(bg="white")
        prev_btn.config(bg="white")
        title.config(bg="white", fg="black")
        btn_select_mode.configure( fg_color="white",  
                      border_color="black", 
                      text_color = "black",
                      hover_color = "white") 
        btn_select_folder.configure(fg_color="white",  
                      border_color="black", 
                      text_color = "black",
                      hover_color = "white")
          
        # Changes the window to light theme 
        root.config(bg="white")   
        switch_value = True
  

btn_select_mode = ctk.CTkButton(root, 
                                text="Change Theme", 
                                font=("TkDefaultFont", 18), 
                                command=toggle, 
                                text_color="black",
                                border_color="black",
                                border_width=1, 
                                fg_color="white",
                                hover_color="white")
btn_select_mode.pack(padx = 10)

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

            if current_position >= pbar["max"]:
                try:
                    next_music()
                except:
                    stop_music()
                pbar["value"] = 0

pt = threading.Thread(target=update_progress_bar)
pt.daemon = True
pt.start()

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


border = Frame(root, background="black")
songlist = Listbox(border, width=50, font=("TkDefaultFont", 16))
songlist.pack(pady=1, padx= 1)
border.pack(padx=40, pady=40)

play_btn_image = PhotoImage(file= "assets/play.png")
pause_btn_image = PhotoImage(file= "assets/pause.png")
next_btn_image = PhotoImage(file= "assets/next.png")
prev_btn_image = PhotoImage(file= "assets/previous.png")

s = ttk.Style()
s.theme_use('alt')
s.configure("blue.Horizontal.TProgressbar", troughcolor = 'white', background = '#0078d7', bordercolor = "white", darkcolor = "#0078d7", lightcolor = "white" )
pbar = Progressbar(root, length=300, mode="determinate", style="blue.Horizontal.TProgressbar")
pbar.pack(pady=10)

control_frame = Frame(root, bg="white")
control_frame.pack(pady=20)

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music, bg="white")
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music, bg="white")
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music, bg="white")
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music, bg="white")

play_btn.grid(row=0,column=1,padx=7,pady=10)
pause_btn.grid(row=0,column=2,padx=7,pady=10)
next_btn.grid(row=0,column=3,padx=7,pady=10)
prev_btn.grid(row=0,column=0,padx=7,pady=10)

root.mainloop()