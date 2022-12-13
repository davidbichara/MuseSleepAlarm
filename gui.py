import tkinter as tk
from tkinter import *
from GIFLoader import ImageLabel;
import pandas as pd
import time
from threading import Thread
import os
import traceback

########################################################################################################################################
#GenerateUI(): Launches and fully manages UI
#Parms: None
#Returns: None
########################################################################################################################################

def GenerateUI():
      # create root window
    root = tk.Tk()
    print("UI Starting...")
    '''
    root.title("Mind Alarm")  # title of the GUI window
    root.maxsize(900, 600)  # specify the max size the window can expand to
    root.config(bg="white")  # specify background color
    '''
    root.title("MUSE interface")  # title of the GUI window
    #root.maxsize(1200, 2000)  # specify the max size the window can expand to
    root.config(bg="white")  # specify background color
    FontBtn=('Times', 40, 'normal') #font and size for button 
    FontCon=('Times', 30, 'normal') #font for the connection status 

    #Window Size  
    window_width = 800
    window_height = 500

    #Centers the window on the screen 
    screen_width = root.winfo_screenwidth() # get the screen dimension
    screen_height = root.winfo_screenheight() # get the screen dimension
    center_x = int(screen_width/2 - window_width / 2)  # find the center point
    center_y = int(screen_height/2 - window_height / 2)+15# find the center point
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # set the position of the window to the center of the screen

    #makes row 1 bigger 
    root.rowconfigure(1, weight=3)
    root.rowconfigure(0, weight=1)
    ############################
    response = Label(root, text ="Connection status: ", font=FontCon, fg="black", bg= 'white')
    response.grid(row=0,column=0, sticky=tk.NS, padx=2, pady=0)
    connectionStatus = tk.StringVar()
    connectionStatus.set("Not Connected")
    connectionColor = tk.StringVar()
    connectionColor.set("red")
    connectionLabel = Label(root, textvariable =connectionStatus, font=FontCon, fg="red", bg= 'white')
    connectionLabel.grid(row=0,column=1, sticky=tk.W, padx=2, pady=2)
    ######################################
    gif = ImageLabel(root)
    gif.grid(row=3,column=0)

    gif.load('waveloading.gif')
    prev = "Not Connected"

    def clicked():
        stopAlarmCSV = pd.DataFrame(['Stop'])
        print(stopAlarmCSV.head())
        stopAlarmCSV.to_csv('/home/pi/Desktop/Method2/alarmStop.csv')
        print('Button Pressed')


    response = Label(root, text ="", fg="black", bg= 'white')
    response.grid(row=4,column=1, padx=5, pady=5)
    btn = Button(root, wraplength=140, height=7, width=12, text="Stop\nAlarm", font=FontBtn, bg='red', fg='white', command=clicked)
    #btn.grid(row=1, column=1, padx=0, pady=0)
    btn.grid(row=3, column=1, padx=0, pady=0)
    

   # def showConnection():
    #    contectionText = Label(root, text ="Connected!", fg="green", bg= 'white').grid(row=1,column=0, padx=5, pady=1)
    def updateConnection(connectionStatus, connectionLabel, gif, prevStatus):
        #print("calling updateConnection")
        if os.path.exists('/home/pi/Desktop/Method2/connected.txt'): # arr
            connection = "Connected"
        else:
            connection = "Not Connected"
        connectionStatus.set(connection)
        color = "green" if connection == "Connected" else "red"
        connectionLabel.config(fg=color)
        if connection == "Connected" and prevStatus == "Not Connected":
            gif.unload()
            gif.load('waveloading.gif')
        elif connection =="Not Connected":
            gif.unload()
            gif.load('checklist.png')
        prev = connection
        return prev

   
    while True:
        #time.sleep(5)
        prev = updateConnection(connectionStatus, connectionLabel, gif, prev)
        root.update_idletasks()
        root.update()
