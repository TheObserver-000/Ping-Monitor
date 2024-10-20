import tkinter as tk
from tkinter import ttk
#import ttkbootstrap as ttkb
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
    textbox.config(state= "normal")
    textbox.insert(tk.END, txt)
    textbox.config(state= "disabled")
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
    if sound_mode == 0:
        pass
    elif sound_mode == 1:
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
    elif sound_mode == 2:
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
window = tk.Tk()
window.title("Ping Monitor")
window.config(background = "#483D8B")
window.geometry("1300x650")
#window.resizable(0,0)
window.minsize(950,541)
pic = tk.PhotoImage(file = os.path.join(base_dir, "Assets", "pingmonitor_logo.png"))
window.iconphoto(True, pic) 
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
def custom_ip_check(event = None):
    global ip_address
    global ipentersave

    ip_manuall = re.search(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', ipenter.get())    #checks for correct IP format
    if ip_manuall:
        ip_manuall = ip_manuall.group(0)
        if comboboxip.current() == (len(ipl)-1):
            ip_address = ip_manuall 
        ipentersave = ip_manuall 
    elif ipenter.get() == "":
        ipenter.delete(0, tk.END)
        ipentersave = ""
    else:
        ipenter.delete(0, tk.END)
        ipenter.insert(0, ipentersave)
    
    try:
        if ipentersave == ip_address:
            lblshowip.config(text= ip_address, fg = col6)
        else:
            lblshowip.config(text= ip_address, fg = col7)
    except:
        pass

def choose_ip(event = None):
    try:
        ipenter
    except:
        return
    
    global ip_address
    global ipentersave

    if comboboxip.current() == (len(ipl)-1):  
        ip_manuall = re.search(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', ipenter.get())    #checks for correct IP format
        if ip_manuall:
            ip_manuall = ip_manuall.group(0)
            ip_address = ip_manuall 
    else:
        ip_address = ipl[comboboxip.current()]

    try:
        if ipentersave == ip_address:
            lblshowip.config(text= ip_address, fg = col6)
        else:
            lblshowip.config(text= ip_address, fg = col7)
    except:
        pass

    router_mode_check()

def choose_sound_mode(event = None):
    global sound_mode
    sound_mode = comboboxsound.current()
    router_mode_check()

def choose_threshold1(event = None):
    global first_threshold
    global second_threshold

    if first_t.get().isdigit() == True:
        if int(first_t.get()) > 9999:
            first_threshold = int(9999)
            first_t.delete(0, tk.END)
            first_t.insert(0, first_threshold)
        else: 
            first_threshold = int(first_t.get())
            first_t.delete(0, tk.END)
            first_t.insert(0, first_threshold)
    else:
        first_threshold = int(0)
        first_t.delete(0, tk.END)
        first_t.insert(0, first_threshold)
    
    try:
        lblshowt1.config(text= first_threshold)
    except:
        pass

    choose_threshold2()

def choose_threshold2(event = None):
    global first_threshold
    global second_threshold
    
    if second_t.get().isdigit() == True:
        if int(second_t.get()) > 9999:
            second_threshold = int(9999)
            second_t.delete(0, tk.END)
            second_t.insert(0, second_threshold)
        elif first_threshold == 0 or int(second_t.get()) <= first_threshold:
            second_threshold = 0
            second_t.delete(0, tk.END)
            second_t.insert(0, second_threshold)
        else:
            second_threshold = int(second_t.get())
            second_t.delete(0, tk.END)
            second_t.insert(0, second_threshold)
    else:
        second_threshold = int(0)
        second_t.delete(0, tk.END)
        second_t.insert(0, second_threshold)
    
    try:
        lblshowt2.config(text= second_threshold)
    except:
        pass

def choose_time_mode(event = None):
    global time_mode
    time_mode = int(ts.get())

def choose_warning_mode(event = None):
    global warning_mode
    warning_mode = hs.get()
    router_mode_check()

def choose_router_mode(event = None):
    global router_mode
    router_mode = rs.get()

def router_mode_check():
    global warning_mode
    global sound_mode
    try:
        if ip_address == "192.168.1.1":
            rs.set(1)
        if warning_mode == 0 and sound_mode == 0:
            rs.set(0)
        choose_router_mode()
    except Exception as error:
        #print(error)
        pass
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def clearterminal():
    textbox.config(state= "normal")
    textbox.delete(1.0, tk.END)
    textbox.config(state= "disabled")

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
        startbutton.config(image= startpic)
    elif start_indicator ==0:
        startbutton.config(image= stoppic)
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

font1_1 = ("Cascadia Code", 9)
font1_2 = ("Cascadia Code", 10)
font1_3 = ("Cascadia Code", 12)
font2   = ("Consolas", 12)

style= ttk.Style()
style.theme_use("clam")

style.configure("TCombobox")
style.map("TCombobox",
    arrowcolor=[("readonly", col3)],
    arrowsize= [("readonly", 15)],
    background= [("readonly", col4)],
    bordercolor= [("readonly", col3)],
    darkcolor= [("readonly", col3)],
    lightcolor=[("readonly", col3)],
    foreground= [("readonly", col2)],
    fieldbackground= [("readonly", col3)],
    padding=[("readonly", 2)],
    selectbackground=[("readonly", col3)],
    selectforeground=[("readonly", col2)])

style.configure("sound.TCombobox")
style.map("sound.TCombobox",
    arrowcolor=[("readonly", col3)],
    arrowsize= [("readonly", 15)],
    background= [("readonly", col4)],
    bordercolor= [("readonly", col3)],
    darkcolor= [("readonly", col3)],
    lightcolor=[("readonly", col3)],
    foreground= [("readonly", col6)],
    fieldbackground= [("readonly", col3)],
    padding=[("readonly", 2)],
    selectbackground=[("readonly", col3)],
    selectforeground=[("readonly", col6)])

style.configure("TScrollbar")
style.map("TScrollbar",
    arrowcolor=[("!disabled", col3), ('pressed', col3), ('active', col3), ("disabled", col3)],
    arrowsize=[("!disabled", 17), ('pressed', 17), ('active', 17), ("disabled", 17)],
    background=[("!disabled", col4), ('pressed', col4), ('active', col4), ("disabled", col4)],
    bordercolor=[("!disabled", col3), ('pressed', col3), ('active', col3), ("disabled", col3)],
    darkcolor=[("!disabled", col3), ('pressed', col3), ('active', col3), ("disabled", col3)],
    lightcolor=[("!disabled", col3), ('pressed', col3), ('active', col3), ("disabled", col3)],
    foreground=[("!disabled", col3), ('pressed', col3), ('active', col3), ("disabled", col3)],
    gripcount=[("!disabled", 0), ('pressed', 0), ('active', 0), ("disabled", 0)],
    troughcolor=[("!disabled", col3), ('pressed', col3), ('active', col3), ("disabled", col3)])

#-------------------------------------------------------------------------------------------------------------------------------------------------------
frame1_r0t2_c0  = tk.Frame(window, width= 35, height= 300, background= col5)
frame1_r0t2_c0.grid(row = 0, column = 0, padx= pad1, pady= pad1, rowspan= 4, sticky= "nsew")

frame2_r0_c1t2  = tk.Frame(window, width= 200, height= 35, background= col5)
frame2_r0_c1t2.grid(row = 0, column = 1, padx= pad1, pady= pad1, columnspan= 2, sticky= "nsew")

frame3_r1_c1    = tk.Frame(window, width= 200, height= 400, background= col4)
frame3_r1_c1.grid(row = 1, column = 1, padx= pad1, pady= pad1, sticky= "nsew")
frame3_r1_c1.rowconfigure((2,5,8,11,14), weight= 1)

frame4_r1_c2    = tk.Frame(window, width= 200, height= 400, background= col4)
frame4_r1_c2.grid(row = 1, column = 2, padx= pad1, pady= pad1, sticky= "nsew")
frame4_r1_c2.rowconfigure((2,5,8,11,14), weight= 1)

frame5_r2_c1t2  = tk.Frame(window, width= 200, background= col5)
frame5_r2_c1t2.grid(row = 2, column = 1, padx= pad1, pady= pad1, columnspan= 2, sticky= "nsew")

frame6_r3_c1t2  = tk.Frame(window, width= 200, height= 100, background= col5)
frame6_r3_c1t2.grid(row = 3, column = 1, padx= pad1, pady= pad1, columnspan= 2, sticky= "nsew")
frame6_r3_c1t2.columnconfigure((0,1,2), weight=1)
frame6_r3_c1t2.rowconfigure((0,1,2), weight=1)

frame7_r0_c3t5  = tk.Frame(window, width= 300, height= 35, background= col5)
frame7_r0_c3t5.grid(row = 0, column = 3, padx= pad1, pady= pad1, columnspan= 3, sticky= "nsew")

frame8_r2_c3t5  = tk.Frame(window, width= 500, height= 300, background= col3)
frame8_r2_c3t5.grid(row = 1, column = 3, padx= pad2, pady= pad2, columnspan= 3 ,rowspan= 2, sticky= "nsew")
frame8_r2_c3t5.columnconfigure(0, weight=3)
frame8_r2_c3t5.rowconfigure(0, weight= 3)

frame9_r3_c3    = tk.Frame(window, width= 100, height= 100, background= col5)
frame9_r3_c3.grid(row = 3, column = 3, padx= pad1, pady= pad1, sticky= "nsew")
frame9_r3_c3.columnconfigure((0,1,2), weight=1)
frame9_r3_c3.rowconfigure((0,1,2), weight=1)


frame10_r3_c4   = tk.Frame(window, width= 100, height= 100, background= col5)
frame10_r3_c4.grid(row = 3, column = 4, padx= pad1, pady= pad1, sticky= "nsew")
frame10_r3_c4.columnconfigure((0,1,2), weight=1)
frame10_r3_c4.rowconfigure((0,1,2), weight=1)

frame11_r3_c5   = tk.Frame(window, width= 100, height= 100, background= col5)
frame11_r3_c5.grid(row = 3, column = 5, padx= pad1, pady= pad1, sticky= "nsew")
frame11_r3_c5.columnconfigure((0,1,2), weight=1)
frame11_r3_c5.rowconfigure((0,1,2), weight=1)

frame12_r0t2_c6 = tk.Frame(window, width= 35, height= 300, background= col5)
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
lbl1 = tk.Label(frame3_r1_c1, text = "IP addresses:", bg = col4, fg= col1, font = font1_1).grid(row = 0, column = 0, sticky= "w")
lbl2 = tk.Label(frame4_r1_c2, text = "Sound options:", bg = col4, fg= col1, font = font1_1).grid(row = 0, column = 0, sticky= "w")

ipl = ip_addresses
comboboxip= ttk.Combobox(frame3_r1_c1, value = ipl, width= 15, state= "readonly", cursor="hand2", font= font1_2)
comboboxip.current(0)
comboboxip.bind("<<ComboboxSelected>>", choose_ip)
choose_ip()
comboboxip.grid(row=1, column=0, padx = 3, pady = 3, sticky= "w")

sdl = ["Silent","Normal","Loud"]
comboboxsound= ttk.Combobox(frame4_r1_c2, value = sdl, width= 6, state= "readonly", cursor="hand2", font= font1_2, style= "sound.TCombobox")
comboboxsound.current(1)
comboboxsound.bind("<<ComboboxSelected>>", choose_sound_mode)
choose_sound_mode()
comboboxsound.grid(row=1, column=0, padx = 3, pady = 3, sticky= "w")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace1 = tk.Label(frame3_r1_c1, bg = col4).grid(row = 2, column = 0)
lblspace1 = tk.Label(frame4_r1_c2, bg = col4).grid(row = 2, column = 0)

lbl3 = tk.Label(frame3_r1_c1, text = "Custom IP address:", bg = col4, fg= col1, font = font1_1).grid(row = 3, column = 0, sticky= "w")
lbl4 = tk.Label(frame4_r1_c2, bg = col4).grid(row = 3, column = 0, sticky= "w")

ipenter = tk.Entry(frame3_r1_c1, bg= col3, fg= col2, relief= "flat", width=15, font = font1_2)
ipenter.grid(row=4, column=0, padx = 3, pady = 3, sticky= "nsw")
ipenter.bind("<Return>", custom_ip_check)

ipenterfake = tk.Entry(frame4_r1_c2, width= 5, bg = col10, font = font1_2)
ipenterfake.grid(row=4, column=0, padx = 3, pady = 3, sticky= "nsw")

lblshowip = tk.Label(frame4_r1_c2, bg= col4, fg= col6, width= 15, anchor="w", font = font1_2, text= "192.168.1.1")
lblshowip.grid(row = 4, column = 0, sticky= "w")
choose_ip()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace1 = tk.Label(frame3_r1_c1, bg= col4).grid(row = 5, column = 0)
lblspace1 = tk.Label(frame4_r1_c2, bg= col4).grid(row = 5, column = 0)

lbl5 = tk.Label(frame3_r1_c1, text = "First threshold:", bg= col4, fg= col1, font = font1_1).grid(row = 6, column = 0, sticky= "w")
lbl6 = tk.Label(frame4_r1_c2, text = "Second threshold:", bg= col4, fg= col1, font = font1_1).grid(row = 6, column = 0, sticky= "w")

first_t = tk.Entry(frame3_r1_c1, bg= col3, fg= col2, relief= "flat", width= 5, font = font1_2)
first_t.grid(row=7, column=0, padx = 3, pady = 3, sticky= "nsw")
first_t.bind("<Return>", choose_threshold1)

second_t = tk.Entry(frame4_r1_c2, bg= col3, fg= col2, relief= "flat", width= 5, font = font1_2)
second_t.grid(row=7, column=0, padx = 3, pady = 3, sticky= "nsw")
second_t.bind("<Return>", choose_threshold1)

lblshowt1 = tk.Label(frame3_r1_c1 ,height= 1 , bg= col4, fg= col6, width= 10, anchor="w", font = font1_2, text= "100")
lblshowt1.grid(row = 7, column = 0, sticky= "e")

lblshowt2 = tk.Label(frame4_r1_c2 ,height= 1 , bg= col4, fg= col6, width= 7, anchor="w", font = font1_2, text= "300")
lblshowt2.grid(row = 7, column = 0, sticky= "e")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace1 = tk.Label(frame3_r1_c1, bg= col4).grid(row = 8, column = 0)
lblspace1 = tk.Label(frame4_r1_c2, bg= col4).grid(row = 8, column = 0)

lbl7 = tk.Label(frame3_r1_c1, text = "Time:", bg= col4, fg= col1, font = font1_1).grid(row = 9, column = 0, sticky= "w")
lbl8 = tk.Label(frame4_r1_c2, bg= col4).grid(row = 9, column = 0, sticky= "w")

ts =  tk.IntVar()
ts.set(1)
rdb1 = tk.Radiobutton(frame3_r1_c1, command =choose_time_mode, text = "Enable", variable = ts, value = 1, bg= col4, fg= col6, activebackground= col4, activeforeground= col7, selectcolor= col4, font = font1_1, cursor="hand2")
rdb1.grid(row = 10, column = 0, padx = 3, pady = 3, sticky= "w")
rdb2 = tk.Radiobutton(frame4_r1_c2, command =choose_time_mode, text = "Disable", variable = ts, value = 0, bg= col4, fg= col6, activebackground= col4, activeforeground= col7, selectcolor= col4, font = font1_1, cursor="hand2")
rdb2.grid(row = 10, column = 0, padx = 3, pady = 3, sticky= "w")
choose_time_mode()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace1 = tk.Label(frame3_r1_c1, bg= col4).grid(row = 11, column = 0)
lblspace1 = tk.Label(frame4_r1_c2, bg= col4).grid(row = 11, column = 0)

lbl9 = tk.Label(frame3_r1_c1, text = "Warning highlight:", bg= col4, fg= col1, font = font1_1).grid(row = 12, column = 0, sticky= "w")
lbl10 = tk.Label(frame4_r1_c2, bg= col4).grid(row = 12, column = 0, sticky= "w")

hs =  tk.IntVar()
hs.set(1)
rdb1 = tk.Radiobutton(frame3_r1_c1, command =choose_warning_mode, text = "Enable", variable = hs, value = 1, bg= col4, fg= col6, activebackground= col4, activeforeground= col7, selectcolor= col4, font = font1_1, cursor="hand2")
rdb1.grid(row = 13, column = 0, padx = 3, pady = 3, sticky= "w")
rdb2 = tk.Radiobutton(frame4_r1_c2, command =choose_warning_mode, text = "Disable", variable = hs, value = 0, bg= col4, fg= col6, activebackground= col4, activeforeground= col7, selectcolor= col4, font = font1_1, cursor="hand2")
rdb2.grid(row = 13, column = 0, padx = 3, pady = 3, sticky= "w")
choose_warning_mode()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
lblspace1 = tk.Label(frame3_r1_c1, bg= col4).grid(row = 14, column = 0)
lblspace1 = tk.Label(frame4_r1_c2, bg= col4).grid(row = 14, column = 0)

lbl11 = tk.Label(frame3_r1_c1, text = "Router check:", bg= col4, fg= col1, font = font1_1).grid(row = 15, column = 0, sticky= "w")
lbl12 = tk.Label(frame4_r1_c2, bg= col4).grid(row = 15, column = 0, sticky= "w")

rs =  tk.IntVar()
rs.set(0)
rdb1 = tk.Radiobutton(frame3_r1_c1, command =choose_router_mode, text = "Enable", variable = rs, value = 1, bg= col4, fg= col6, activebackground= col4, activeforeground= col7, selectcolor= col4, font = font1_1, cursor="hand2")
rdb1.grid(row = 16, column = 0, padx = 3, pady = 3, sticky= "w")
rdb2 = tk.Radiobutton(frame4_r1_c2, command =choose_router_mode, text = "Disable", variable = rs, value = 0, bg= col4, fg= col6, activebackground= col4, activeforeground= col7, selectcolor= col4, font = font1_1, cursor="hand2")
rdb2.grid(row = 16, column = 0, padx = 3, pady = 3, sticky= "w")
choose_router_mode()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
vscroll=ttk.Scrollbar(frame8_r2_c3t5, orient="vertical", cursor="hand2")
vscroll.grid(row = 0, column = 1, sticky = "ns")

textbox = tk.Text(frame8_r2_c3t5, bg= col3, fg= col2, relief= "flat", font = font2, padx= 5, pady= 5, yscrollcommand=vscroll.set, state="disabled")
vscroll.config(command=textbox.yview)
textbox.grid(row=0, column=0, sticky = "nswe")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
logolblpic = tk.PhotoImage(file = os.path.join(base_dir, "Assets", "pingmonitor.png"))
logolbl = tk.Label(frame6_r3_c1t2, bg = col5, relief = "flat", padx = 10, pady = 1, image = logolblpic)
logolbl.grid(row= 1, column= 1, sticky="nsw")

clearbutton = tk.Button(frame9_r3_c3, command= clearterminal, text= "Clear text box ()", bg= col6, fg= col3, activebackground= col7, activeforeground= col3, relief= "flat", font = font1_3, cursor="hand2")
clearbutton.grid(row= 1, column= 1)

startpic = tk.PhotoImage(file = os.path.join(base_dir, "Assets", "start.png"))
stoppic  = tk.PhotoImage(file = os.path.join(base_dir, "Assets", "stop.png"))
startbutton = tk.Button(frame10_r3_c4, command = startstop, bg= col8, activebackground= col9, relief= "flat", cursor="hand2", image= startpic)
startbutton.grid(row= 1, column= 1)

Yfixbutton = tk.Button(frame11_r3_c5, command = scrollfix, text= "Scroll fix ()", bg= col6, fg= col3, activebackground= col7, activeforeground= col3, relief= "flat", font = font1_3, cursor="hand2")
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
ip_address = None
first_threshold = 0 
#first_t.insert(0, first_threshold)
lblshowt1.config(text= first_threshold)
second_threshold = 0 
#second_t.insert(0, second_threshold)
lblshowt2.config(text= second_threshold)
sound_mode
time_mode
warning_mode
router_mode
router_mode_check()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
start_indicator = 0
scrollpo = 1
close = 0

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