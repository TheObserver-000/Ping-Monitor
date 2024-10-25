#import tkinter as tk
#from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import os
import subprocess
import re
import time
import threading
import playsound
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def printtxt(txt):
    textbox.configure(state= "normal")
    textbox.insert(ctk.END, txt)
    textbox.configure(state= "disabled")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def load_ip_addresses(file_path):
    with open(file_path, 'r') as file:
        ip_addresses = [line.strip() for line in file.readlines()]
        ip_addresses.append('(Custom)')
    return ip_addresses

def ping(ip):
    command = ["ping", "-n", "1", ip] if os.name == 'nt' else ["ping", "-c", "1", ip]
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    return result.stdout.decode()

def get_ping_time(ping_output):
    time_ms = re.search(r'time[=<]\s*(\d+)ms', ping_output)
    if time_ms:
        return int(time_ms.group(1))
    return None

def print_timeout(condition):
    if condition == 1:
        printtxt("Request timed out.")
    elif condition == 2:
        printtxt("Destination host unreachable.")
    elif condition == 3:
        printtxt("Destination net unreachable.")
    elif condition == 4:
        printtxt("General failure.")
    elif condition == 5:
        printtxt("Unknown host.")

def is_timeout(ping_output):
    if "Request timed out" in ping_output:
        return 1
    elif "Destination host unreachable" in ping_output:
        return 2
    elif "Destination net unreachable" in ping_output:
        return 3
    elif "General failure" in ping_output:
        return 4
    elif "Unknown host" in ping_output:
        return 5
    return 0

def sound_call(sound_mode, condition):
    if sound_mode == "Silent":
        pass
    elif sound_mode == "Normal":
        if condition == 1:
            playsound.playsound(os.path.join(base_dir, "Sounds", "normal_alert.mp3"))
        elif condition == 2:
            playsound.playsound(os.path.join(base_dir, "Sounds", "normal_warning.mp3"))
        elif condition == 3:
            playsound.playsound(os.path.join(base_dir, "Sounds", "normal_error.mp3"))
        elif condition == 4:
            playsound.playsound(os.path.join(base_dir, "Sounds", "normal_router.mp3"))
        elif condition == 5:
            playsound.playsound(os.path.join(base_dir, "Sounds", "normal_unknown.mp3"))
    elif sound_mode == "Loud":
        if condition == 1:
            playsound.playsound(os.path.join(base_dir, "Sounds", "loud_alert.mp3"))
        elif condition == 2:
            playsound.playsound(os.path.join(base_dir, "Sounds", "loud_warning.mp3"))
        elif condition == 3:
            playsound.playsound(os.path.join(base_dir, "Sounds", "loud_error.mp3"))
        elif condition == 4:
            playsound.playsound(os.path.join(base_dir, "Sounds", "loud_router.mp3"))
        elif condition == 5:
            playsound.playsound(os.path.join(base_dir, "Sounds", "loud_unknown.mp3"))

def warning_highlight(warning_mode, condition):
    if warning_mode == 0:
        printtxt("\n")
    elif warning_mode == 1:
        if condition == 1:
            printtxt("   >>>   Alert: Network latency.\n")
        elif condition == 2:
            printtxt("   >>>   Warning: Critical network latency.\n")
        elif condition == 3:
            printtxt("   >>>   Error: Network failure.\n")
        elif condition == 4:
            printtxt("   >>>   Error: Router unreachable.\n")

def get_time():
    time_string = time.strftime("%H:%M:%S")
    printtxt(f"(Time: {time_string})\t")

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

def ping_process(ip, first_threshold, second_threshold, sound_mode, time_mode, warning_mode, router_mode):

    ping_output = ping(ip)

    if time_mode == 1:
        get_time()
        
    if is_timeout(ping_output) != 0:
        if router_mode == 1:
            router_output = ping("192.168.1.1")
            if is_timeout(router_output) != 0:
                print_timeout(is_timeout(ping_output))
                warning_highlight(warning_mode, 4)
                sound_call(sound_mode, 4)
            else:
                print_timeout(is_timeout(ping_output))
                warning_highlight(warning_mode, 3)
                sound_call(sound_mode, 3)
        elif router_mode == 0:
            print_timeout(is_timeout(ping_output))
            warning_highlight(warning_mode, 3)
            sound_call(sound_mode, 3)

    else:
        ping_time = get_ping_time(ping_output)

        if ping_time is not None:
            printtxt(f"Ping time: {ping_time} ms")

            if ping_time > first_threshold and first_threshold != 0:
                if ping_time > second_threshold != 0 and second_threshold != 0:
                    warning_highlight(warning_mode, 2)
                    sound_call(sound_mode, 2)
                else:
                    warning_highlight(warning_mode, 1)
                    sound_call(sound_mode, 1)
            else:
                printtxt("\n")
        else:
            printtxt(f"Unknown Error. Failed to get ping time. More information:\n{ping_output}\n")
            sound_call(sound_mode, 5)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
ip_file_path = os.path.join(base_dir, "Settings", "ip_addresses.txt")
ip_addresses = load_ip_addresses(ip_file_path)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
window = ctk.CTk()
window.title("Ping Monitor")
window.configure(background = "#483D8B")
window.geometry("1300x650")
window.minsize(950,541) 
window.iconbitmap(os.path.join(base_dir, "Assets", "pingmonitor_logo.png")) 
window.columnconfigure((3,4,5), weight= 1)
window.rowconfigure(2, weight= 1)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
ipentersave = ""
def custom_ip_check(*args):
    global ip_address
    global ipentersave

    ip_manuall = re.search(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', ipenter.get())    #checks for correct IP format
    if ip_manuall:
        ip_manuall = ip_manuall.group(0)
        if comboboxip.get() == (len(ipl)-1):
            ip_address = ip_manuall 
        ipentersave = ip_manuall 
    elif ipenter.get() == "":
        ipenter.delete(0, ctk.END)
        ipentersave = ""
    else:
        ipenter.delete(0, ctk.END)
        ipenter.insert(0, ipentersave)
    
    if ipentersave == ip_address:
        lblshowip.configure(text= ip_address, text_color = col6)
    else:
        lblshowip.configure(text= ip_address, text_color = col7)

def choose_ip(*args):
    global ip_address
    global ipentersave

    if comboboxip.get() == ipl[-1]:  
        ip_manuall = re.search(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', ipenter.get())    #checks for correct IP format
        if ip_manuall:
            ip_manuall = ip_manuall.group(0)
            ip_address = ip_manuall 
    else:
        ip_address = comboboxip.get()

    if ipentersave == ip_address:
        lblshowip.configure(text= ip_address, text_color = col6)
    else:
        lblshowip.configure(text= ip_address, text_color = col7)
    router_mode_check()

def choose_sound_mode(*args):
    global sound_mode
    sound_mode = comboboxsound.get()
    router_mode_check()

def choose_threshold1(*args):
    global first_threshold
    global second_threshold

    if first_t.get().isdigit() == True:
        if int(first_t.get()) > 9999:
            first_threshold = int(9999)
            first_t.delete(0, ctk.END)
            first_t.insert(0, first_threshold)
        else: 
            first_threshold = int(first_t.get())
            first_t.delete(0, ctk.END)
            first_t.insert(0, first_threshold)
    else:
        first_threshold = int(0)
        first_t.delete(0, ctk.END)
        first_t.insert(0, first_threshold)
    lblshowt1.configure(text= first_threshold)
    choose_threshold2()

def choose_threshold2(*args):
    global first_threshold
    global second_threshold
    
    if second_t.get().isdigit() == True:
        if int(second_t.get()) > 9999:
            second_threshold = int(9999)
            second_t.delete(0, ctk.END)
            second_t.insert(0, second_threshold)
        elif first_threshold == 0 or int(second_t.get()) <= first_threshold:
            second_threshold = 0
            second_t.delete(0, ctk.END)
            second_t.insert(0, second_threshold)
        else:
            second_threshold = int(second_t.get())
            second_t.delete(0, ctk.END)
            second_t.insert(0, second_threshold)
    else:
        second_threshold = int(0)
        second_t.delete(0, ctk.END)
        second_t.insert(0, second_threshold)
    lblshowt2.configure(text= second_threshold)

def choose_time_mode(*args):
    global time_mode
    time_mode = ts.get()

def choose_warning_mode(*args):
    global warning_mode
    warning_mode = hs.get()
    router_mode_check()

def choose_router_mode(*args):
    global router_mode
    router_mode = rs.get()

def router_mode_check():
    global warning_mode
    global sound_mode
    try:
        if ip_address == "192.168.1.1":
            rs.set(1)
        if warning_mode == 0 and sound_mode == "Silent":
            rs.set(0)
        choose_router_mode()
    except Exception as error:
        #print(error)
        pass
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def clearterminal():
    textbox.configure(state= "normal")
    textbox.delete(1.0, ctk.END)
    textbox.configure(state= "disabled")

def on_destroy(event):
    global close
    if event.widget != window:
        return
    close = 1

def scrollfix():
    global scrollpo
    if scrollpo==1:
        scrollpo=0
    elif scrollpo==0:
        scrollpo=1

def startstop():
    global start_indicator
    if start_indicator == 1:
        start_indicator = 0
        startbutton.configure(image= startpic)
    elif start_indicator ==0:
        startbutton.configure(image= stoppic)
        start_indicator = 1

def main_loop():
    global start_indicator
    global scrollpo
    global close
    global ip_address
    global first_threshold
    global second_threshold
    global sound_mode
    global time_mode
    global warning_mode
    global router_mode
    try:
        while close == 0:
            time.sleep(0.05)
            if start_indicator ==1:
                choose_ip()
                custom_ip_check()
                choose_threshold1()
                choose_threshold2()
                while start_indicator ==1:
                    ping_process(ip_address, first_threshold, second_threshold, sound_mode, time_mode, warning_mode, router_mode)
                    if scrollpo ==1:
                        textbox.yview_moveto(1.0)
                    time.sleep(1)

    except Exception as error:
        #print(error)
        return
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
start_indicator = 0
scrollpo = 1
close = 0
#-------------------------------------------------------------------------------------------------------------------------------------------------------
ip_address = None
sound_mode = None
first_threshold = 0 
second_threshold = 0 
time_mode = 0
warning_mode = 0
router_mode = 0
#-------------------------------------------------------------------------------------------------------------------------------------------------------
pad1  = 0
pad2  = 3
col1  = "#E0FFFF"
col2  = "#EFEFEF"
col3  = "#151515"
col4  = "#2E2E2E"
col5  = "#2A3439"
col6  = "#32CD32"
col7  = "#009500"
col8  = "#1E90FF"
col9  = "#005FC5"
col10 = "#483D8B"

font1_1 = ("calibri", 9)
font1_2 = ("calibri", 10)
font1_3 = ("calibri", 12)
font2   = ("Consolas", 12)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
frame1_r0t2_c0  = ctk.CTkFrame(window, width= 35, height= 300, bg_color= col5, corner_radius=0)
frame1_r0t2_c0.grid(row = 0, column = 0, padx= pad1, pady= pad1, rowspan= 4, sticky= "nsew")

frame2_r0_c1t2  = ctk.CTkFrame(window, width= 200, height= 35, bg_color= col5, corner_radius=0)
frame2_r0_c1t2.grid(row = 0, column = 1, padx= pad1, pady= pad1, columnspan= 2, sticky= "nsew")

frame3_r1_c1t2  = ctk.CTkFrame(window, width= 200, height= 400, bg_color= col4, corner_radius=0)
frame3_r1_c1t2.grid(row = 1, column = 1, padx= pad1, pady= pad1, sticky= "nsew")
#frame4 is gone
frame5_r2_c1t2  = ctk.CTkFrame(window, width= 200, bg_color= col5, corner_radius=0)
frame5_r2_c1t2.grid(row = 2, column = 1, padx= pad1, pady= pad1, columnspan= 2, sticky= "nsew")

frame6_r3_c1t2  = ctk.CTkFrame(window, width= 200, height= 100, bg_color= col5, corner_radius=0)
frame6_r3_c1t2.grid(row = 3, column = 1, padx= pad1, pady= pad1, columnspan= 2, sticky= "nsew")
frame6_r3_c1t2.columnconfigure((0,1,2), weight=1)
frame6_r3_c1t2.rowconfigure((0,1,2), weight=1)

frame7_r0_c3t5  = ctk.CTkFrame(window, width= 300, height= 35, bg_color= col5, corner_radius=0)
frame7_r0_c3t5.grid(row = 0, column = 3, padx= pad1, pady= pad1, columnspan= 3, sticky= "nsew")

frame8_r2_c3t5  = ctk.CTkFrame(window, width= 500, height= 300, bg_color= col3)
frame8_r2_c3t5.grid(row = 1, column = 3, padx= pad2, pady= pad2, columnspan= 3 ,rowspan= 2, sticky= "nsew")
frame8_r2_c3t5.columnconfigure(0, weight=3)
frame8_r2_c3t5.rowconfigure(0, weight= 3)

frame9_r3_c3    = ctk.CTkFrame(window, width= 100, height= 100, bg_color= col5, corner_radius=0)
frame9_r3_c3.grid(row = 3, column = 3, padx= pad1, pady= pad1, sticky= "nsew")
frame9_r3_c3.columnconfigure((0,1,2), weight=1)
frame9_r3_c3.rowconfigure((0,1,2), weight=1)

frame10_r3_c4   = ctk.CTkFrame(window, width= 100, height= 100, bg_color= col5, corner_radius=0)
frame10_r3_c4.grid(row = 3, column = 4, padx= pad1, pady= pad1, sticky= "nsew")
frame10_r3_c4.columnconfigure((0,1,2), weight=1)
frame10_r3_c4.rowconfigure((0,1,2), weight=1)

frame11_r3_c5   = ctk.CTkFrame(window, width= 100, height= 100, bg_color= col5, corner_radius=0)
frame11_r3_c5.grid(row = 3, column = 5, padx= pad1, pady= pad1, sticky= "nsew")
frame11_r3_c5.columnconfigure((0,1,2), weight=1)
frame11_r3_c5.rowconfigure((0,1,2), weight=1)

frame12_r0t2_c6 = ctk.CTkFrame(window, width= 35, height= 300, bg_color= col5, corner_radius=0)
frame12_r0t2_c6.grid(row = 0, column = 6, padx= pad1, pady= pad1, rowspan= 4, sticky= "nsew")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lbl1 = ctk.CTkLabel(frame3_r1_c1t2, text = "IP addresses:", fg_color = col4, text_color= col1, font = font1_1, corner_radius = 0).grid(row = 0, column = 0, columnspan = 2, sticky= "w")
lbl2 = ctk.CTkLabel(frame3_r1_c1t2, text = "Sound options:", fg_color = col4, text_color= col1, font = font1_1, corner_radius = 0).grid(row = 0, column = 2, columnspan = 2, sticky= "w")

ipl = ip_addresses
comboboxip= ctk.CTkOptionMenu(frame3_r1_c1t2, command = choose_ip, values = ipl, font= font1_2, corner_radius=3, anchor="center")
comboboxip.set(ipl[0])
comboboxip.grid(row=1, column=0, columnspan = 2, padx = 3, pady = 3, sticky= "w")

sdl = ["Silent","Normal","Loud"]
comboboxsound= ctk.CTkOptionMenu(frame3_r1_c1t2, command = choose_sound_mode, values = sdl, font= font1_2, corner_radius=3, anchor="center")
comboboxsound.set(sdl[1])
comboboxsound.grid(row=1, column=2, columnspan = 2, padx = 3, pady = 3, sticky= "w")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace1 = ctk.CTkLabel(frame3_r1_c1t2, fg_color = col4, corner_radius = 0, text="").grid(row = 2, column = 0, columnspan = 4)

lbl3 = ctk.CTkLabel(frame3_r1_c1t2, text = "Custom IP address:", fg_color = col4, text_color= col1, font = font1_1).grid(row = 3, column = 0, columnspan = 2, sticky= "w")
lbl4 = ctk.CTkLabel(frame3_r1_c1t2, text = "Current IP address:", fg_color = col4, text_color= col1, font = font1_1).grid(row = 3, column = 2, columnspan = 2, sticky= "w")

ipenter = ctk.CTkEntry(frame3_r1_c1t2, width=100, font = font1_2, corner_radius=3)
ipenter.grid(row=4, column=0, columnspan = 2, padx = 3, pady = 3, sticky= "nsw")
ipenter.bind("<Return>", custom_ip_check)

lblshowip = ctk.CTkLabel(frame3_r1_c1t2, fg_color= col4, text_color= col6, anchor="w", font = font1_2, text= "")
lblshowip.grid(row = 4, column = 2, columnspan = 2, sticky= "w")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace2 = ctk.CTkLabel(frame3_r1_c1t2, fg_color = col4, corner_radius = 0, text="").grid(row = 5, column = 0, columnspan = 4)

lbl5 = ctk.CTkLabel(frame3_r1_c1t2, text = "First threshold:", fg_color= col4, text_color= col1, font = font1_1, corner_radius = 0).grid(row = 6, column = 0, columnspan = 2, sticky= "w")
lbl6 = ctk.CTkLabel(frame3_r1_c1t2, text = "Second threshold:", fg_color= col4, text_color= col1, font = font1_1, corner_radius = 0).grid(row = 6, column = 2, columnspan = 2, sticky= "w")

first_t = ctk.CTkEntry(frame3_r1_c1t2, width= 40, font = font1_2, corner_radius=3)
first_t.grid(row=7, column=0, padx = 3, pady = 3, sticky= "nsw")
first_t.bind("<Return>", choose_threshold1)

second_t = ctk.CTkEntry(frame3_r1_c1t2, width= 40, font = font1_2, corner_radius=3)
second_t.grid(row=7, column=2, padx = 3, pady = 3, sticky= "nsw")
second_t.bind("<Return>", choose_threshold1)

lblshowt1 = ctk.CTkLabel(frame3_r1_c1t2 , fg_color= col4, text_color= col6, anchor="w", font = font1_2, text= "")
lblshowt1.grid(row = 7, column = 1, sticky= "e")
lblshowt2 = ctk.CTkLabel(frame3_r1_c1t2 , fg_color= col4, text_color= col6, anchor="w", font = font1_2, text= "")
lblshowt2.grid(row = 7, column = 3, sticky= "e")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace3 = ctk.CTkLabel(frame3_r1_c1t2, fg_color = col4, corner_radius = 0, text="").grid(row = 8, column = 0, columnspan = 4)

time_mode = 0

ts = ctk.IntVar(value= time_mode)
tswitch = ctk.CTkSwitch(frame3_r1_c1t2, command= choose_time_mode, variable= ts, onvalue= 1, offvalue= 0, text= "Time")
tswitch.grid(row = 9, column = 0, columnspan = 4, padx = 3, pady = 3, sticky= "w")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace4 = ctk.CTkLabel(frame3_r1_c1t2, fg_color = col4, corner_radius = 0, text="").grid(row = 10, column = 0, columnspan = 4)

warning_mode = 0

hs =  ctk.IntVar(value = warning_mode)
hswitch = ctk.CTkSwitch(frame3_r1_c1t2, command= choose_warning_mode, variable= hs, onvalue= 1, offvalue= 0, text= "Warning highlight")
hswitch.grid(row = 11, column = 0, columnspan = 4, padx = 3, pady = 3, sticky= "w")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace5 = ctk.CTkLabel(frame3_r1_c1t2, fg_color = col4, corner_radius = 0, text="").grid(row = 12, column = 0, columnspan = 4)

router_mode = 0

rs =  ctk.IntVar(value = router_mode)
rswitch = ctk.CTkSwitch(frame3_r1_c1t2, command= choose_router_mode, variable= rs, onvalue= 1, offvalue= 0, text= "Router check")
rswitch.grid(row = 13, column = 0, columnspan = 4, padx = 3, pady = 3, sticky= "w")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
textbox = ctk.CTkTextbox(frame8_r2_c3t5, corner_radius=0)
textbox.grid(row=0, column=0, sticky = "nswe")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
logolblpic = ctk.CTkImage(Image.open(os.path.join(base_dir, "Assets", "pingmonitor.png")))
startpic = ctk.CTkImage(Image.open(os.path.join(base_dir, "Assets", "start.png")))
stoppic  = ctk.CTkImage(Image.open(os.path.join(base_dir, "Assets", "stop.png")))

logolbl = ctk.CTkLabel(frame6_r3_c1t2, bg_color = col5, padx = 10, pady = 1, image = logolblpic, text="")
logolbl.grid(row= 1, column= 1, sticky="nsw")

clearbutton = ctk.CTkButton(frame9_r3_c3, command= clearterminal, text= "Clear text box", font = font1_3)
clearbutton.grid(row= 1, column= 1)

startbutton = ctk.CTkButton(frame10_r3_c4, command = startstop, image= startpic, text="")
startbutton.grid(row= 1, column= 1)

Yfixbutton = ctk.CTkButton(frame11_r3_c5, command = scrollfix, text= "Scroll fix", font = font1_3)
Yfixbutton.grid(row= 1, column= 1)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
choose_ip()
choose_sound_mode()
choose_threshold1()
choose_time_mode()
choose_warning_mode()
choose_router_mode()
router_mode_check()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
mloop = threading.Thread(target = main_loop)
mloop.start()

window.bind("<Destroy>", on_destroy)

window.mainloop()

#how to update exe file (for me):
#open cmd
#cd /d D:\code\ping (the directory of file)
#pyinstaller --noconsole --icon=app_icon.ico --add-data "Data;Data" --add-data "Resource;Resource" ping_monitor.py
#add --onefile after pyinstaller to bundle the entire code and its dependencies
#add --noconsole after pyinstaller to remove console