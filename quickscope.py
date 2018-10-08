import tkinter as tk
from tkinter import Frame, Label, ttk
from os import popen

def chCpu():

    command = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
    cpuUsage = str(round(float(popen(command).read()), 3))

    tempInfo = str(open('/sys/class/thermal/thermal_zone0/temp').readlines())

    usgCpu.configure(text='Total usage:\n' + cpuUsage[:-1]+'%')
    tempCpu .configure(text='Temperature:\n' + tempInfo[2:4]+'.'+tempInfo[5]+'ºC')

    root.after(1000, chCpu)

def chHDD(event):

    part = lstBx.get()
    command = 'df ' + part
    hddUsagelist = list(popen(command).readlines())
    hddUsage = hddUsagelist[1].split()
    hddTotal = float(hddUsage[1])
    hddUsed = float(hddUsage[2])
    hddLeft = float(hddUsage[3])

    ttlHdd.configure(text='Total space:\n' + str(round(hddTotal / 1000000, 3)) + ' GB')

    usdHdd.configure(text='Used space:\n' + str(round(hddUsed / 1000000, 3)) + ' GB')

    leftHdd.configure(text='Left space:\n' + str(round(hddLeft / 1000000, 3)) + ' GB')




def chRam():

    meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in open('/proc/meminfo').readlines())

    mem_tt_kib = meminfo['MemTotal']
    mem_tt_gib= str(round(mem_tt_kib/1048576, 3))

    mem_ac_kib = meminfo['Active']
    mem_ac_gib= str(round(mem_ac_kib/1048576, 3))

    mem_av_kib = meminfo['MemAvailable']
    mem_av_gib= str(round(mem_av_kib/1048576, 3))

    TtRam.configure(text='Total RAM:\n'+mem_tt_gib+' GB')
    AcRam.configure(text='Active RAM:\n'+mem_ac_gib+' GB')
    AvRam.configure(text='Available RAM:\n'+mem_av_gib+' GB')

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

#-----------#


frmCpu = Frame(frmContainer, height=250, width=200, background='#505050', highlightbackground='#404040', highlightthickness=1)
frmCpu.pack_propagate(False)
frmCpu.grid(column=0, row=0)

titleCpu = Label(frmCpu, font=("Arial bold", 18), text='CPU', background='#505050', foreground='white')
titleCpu.pack(side='top', pady=(20, 30))

usgCpu = Label(frmCpu, text='', foreground='white', background='#505050')
usgCpu.pack()

tempCpu = Label(frmCpu, text='', foreground='white', background='#505050')
tempCpu.pack()

#-----------#


frmHDD = Frame(frmContainer, height=250, width=200, background='#505050', highlightbackground='#404040', highlightthickness=1)
frmHDD.pack_propagate(False)
frmHDD.grid(column=1, row=0)

titleHDD = Label(frmHDD, font=("Arial bold", 18), text='Disk', background='#505050', foreground='white')
titleHDD.pack(side='top', pady=(20, 5))

partition = Label(frmHDD, text='Section:', background='#505050', foreground='white')
partition.pack(pady=(0, 5))

hddParts = list(popen('df').readlines())
hddPartsLen = len(hddParts)

partitionlist = []

for x in range(1, hddPartsLen):
    hddPartition = hddParts[x].split()
    if hddPartition[0] != 'tmpfs' and hddPartition[0] != 'udev' :
        partitionlist.append(hddPartition[0])

lstBx = ttk.Combobox(frmHDD, width=15)
lstBx['values'] = partitionlist
lstBx.set(partitionlist[0])
lstBx.pack(pady=(0, 20))

lstBx.bind("<<ComboboxSelected>>", chHDD)

part = lstBx.get()
command = 'df ' + part
hddUsagelist = list(popen(command).readlines())
hddUsage = hddUsagelist[1].split()
hddTotal = round(float(hddUsage[1]) / 1000000, 3)
hddUsed = round(float(hddUsage[2]) / 1000000, 3)
hddLeft = round(float(hddUsage[3])/ 1000000, 3)

ttlHdd = Label(frmHDD, text='Total space:\n' + str(hddTotal) + ' GB', foreground='white', background='#505050')
ttlHdd.pack(pady=(0, 10))

usdHdd = Label(frmHDD, text='Used space:\n' + str(hddUsed) + ' GB', foreground='white', background='#505050')
usdHdd.pack(pady=(0, 10))

leftHdd = Label(frmHDD, text='Left space:\n' + str(hddLeft) + ' GB', foreground='white', background='#505050')
leftHdd.pack()

#-----------#

frmRam = Frame(frmContainer, height=250, width=200, background='#505050', highlightbackground='#404040', highlightthickness=1)
frmRam.pack_propagate(False)
frmRam.grid(column=2, row=0)

titleRam = Label(frmRam, font=("Arial bold", 18), text='RAM', background='#505050', foreground='white')
titleRam.pack(side='top', pady=(20, 30))

TtRam = Label(frmRam, text='', foreground='white', background='#505050')
TtRam.pack(pady=(0,3))

AcRam = Label(frmRam, text='', foreground='white', background='#505050')
AcRam.pack(pady=(0,3))

AvRam = Label(frmRam, text='', foreground='white', background='#505050')
AvRam.pack(pady=(0,3))

#----------#

chCpu()
chRam()

root.mainloop()
