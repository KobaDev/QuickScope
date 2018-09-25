import tkinter as tk
from tkinter import Frame, Label
from os import popen

def chCpu():
    for widget in frmCpu.winfo_children():
        widget.destroy()

    titleCpu = Label(frmCpu, font=("Arial bold", 18), text='CPU', background='#505050', foreground='white')
    titleCpu.pack(side='top', pady=(20, 30))

    command = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
    cpuUsage = str(popen(command).read())

    tempInfo = str(open('/sys/class/thermal/thermal_zone0/temp').readlines())

    usgCpu = Label(frmCpu, text=cpuUsage[:-1]+'%', foreground='white', background='#505050')
    usgCpu.pack()

    tempCpu = Label(frmCpu, text=tempInfo[2:4]+'.'+tempInfo[5]+'ºC', foreground='white', background='#505050')
    tempCpu.pack()

    root.after(1000, chCpu)

def chHDD():
    for widget in frmHDD.winfo_children():
        widget.destroy()

    titleHDD = Label(frmHDD, font=("Arial bold", 18), text='Disk', background='#505050', foreground='white')
    titleHDD.pack(side='top', pady=(20, 30))

    command = 'df /dev/sda6'
    hddUsagelist = list(popen(command).readlines())
    hddUsage = hddUsagelist[1].split()
    hddTotal = float(hddUsage[1])
    hddUsed = float(hddUsage[2])
    hddLeft = float(hddUsage[3])

    ttlHdd = Label(frmHDD, text='Total space:\n'+str(round(hddTotal/1000000, 3))+' GB', foreground='white', background='#505050')
    ttlHdd.pack(pady=(0,10))

    usdHdd = Label(frmHDD, text='Used space:\n'+str(round(hddUsed/1000000, 3))+' GB', foreground='white', background='#505050')
    usdHdd.pack(pady=(0,10))

    leftHdd = Label(frmHDD, text='Left space:\n'+str(round(hddLeft/1000000, 3))+' GB', foreground='white', background='#505050')
    leftHdd.pack()

    root.after(1000, chHDD)

def chRam():
    for widget in frmRam.winfo_children():
        widget.destroy()

    titleRam = Label(frmRam, font=("Arial bold", 18), text='RAM', background='#505050', foreground='white')
    titleRam.pack(side='top', pady=(20, 30))

    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())

    mem_tt_kib = meminfo['MemTotal']
    mem_tt_gib= mem_tt_kib/1048576

    mem_ac_kib = meminfo['Active']
    mem_ac_gib= mem_ac_kib/1048576

    mem_av_kib = meminfo['MemAvailable']
    mem_av_gib= mem_av_kib/1048576

    TtRam = Label(frmRam, text='Total: '+str(round(mem_tt_gib, 2))+' GB', foreground='white', background='#505050')
    TtRam.pack(pady=(0,3))

    AcRam = Label(frmRam, text='Active: '+str(round(mem_ac_gib, 2))+' GB', foreground='white', background='#505050')
    AcRam.pack(pady=(0,3))

    AvRam = Label(frmRam, text='Available: '+str(round(mem_av_gib, 2))+' GB', foreground='white', background='#505050')
    AvRam.pack(pady=(0,3))

    root.after(1000, chRam)


root = tk.Tk()
h, w = 600, 350
root.geometry(str(h)+'x'+str(w))
root.title('QuickScope Hardware Monitor')
root.resizable(False, False)

frmTop = Frame(root, height=100, width=600, background='#505050')
frmTop.pack_propagate(False)
frmTop.pack()

title = Label(frmTop, font=("Arial bold", 31), text='QuickScope', foreground='white', background='#505050')
title.pack(pady=(10,0))
subtitle = Label(frmTop,  font=("Arial bold", 11), text='Just a quick hardware monitor.', foreground='white', background='#505050')
subtitle.pack()

frmContainer = Frame(root, height=700, width=600)
frmContainer.pack()

frmCpu = Frame(frmContainer, height=250, width=200, background='#505050', highlightbackground='#404040', highlightthickness=1)
frmCpu.pack_propagate(False)
frmCpu.grid(column=0, row=0)

frmHDD = Frame(frmContainer, height=250, width=200, background='#505050', highlightbackground='#404040', highlightthickness=1)
frmHDD.pack_propagate(False)
frmHDD.grid(column=1, row=0)

frmRam = Frame(frmContainer, height=250, width=200, background='#505050', highlightbackground='#404040', highlightthickness=1)
frmRam.pack_propagate(False)
frmRam.grid(column=2, row=0)

chCpu()
chHDD()
chRam()

root.mainloop()
