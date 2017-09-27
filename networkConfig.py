# Just like instructions on an exam, READ THE COMMENTS
# before attempting to understand the code.
# This is a simple gui which saves network information in a json file
# whose name is provided as a command-line argument. This is probably not
# the most efficient or intelligent solution, but it seems to work. Note that
# this is written in python 3. Don't forget about the sister file,
# VerifyStrings.

from tkinter import *
import VerifyStrings #string checking
import sys
import json
from pprint import pprint
import os.path
import os
import math

#simply converts a dot-decimal netmask value into a digit value
def convertToNum(netmask):
    if netmask.isdigit():
        return netmask
    else:
        acceptable_values = [0, 128, 192, 224, 240, 248, 252, 254, 255]
        count = 0

        for substr in netmask.split('.'):
            for val in acceptable_values:
                if int(substr) != val:
                    count = count + 1
                else:
                    break

        return count


class NetworkGui:
    def __init__(self, master, isRead, data):
        #This needs to be first because
        self.save = Button(master, text='Save', command=self.write_to_file)
        self.save.grid(row=6, column=1, pady=4)
        # These variables are used for trace(), which essentially tracks
        # their changes in real-time (like being entered into a text field)
        self.ipVar = StringVar()
        self.ipVar.trace('w', self.tracer)

        self.netVar = StringVar()
        self.netVar.trace('w', self.tracer)

        self.routeVar = StringVar()
        self.routeVar.trace('w', self.tracer)

        self.dnsVar = StringVar()
        self.dnsVar.trace('w', self.tracer)

        self.ntpVar = StringVar()
        self.ntpVar.trace('w', self.tracer)

   #-----------------------------------------------------------------------#

        # This section is just for creating the labels and entry fields
        # and setting their positions in the master frame.

        self.master=master


        self.ipAddress = Entry(master, textvariable=self.ipVar)
        self.netmask = Entry(master, textvariable=self.netVar)
        self.route = Entry(master, textvariable=self.routeVar)
        self.dns = Entry(master, textvariable=self.dnsVar)
        self.ntp = Entry(master, textvariable=self.ntpVar)

        self.ipLabel = Label(master, text='IP Address')
        self.netmaskLabel = Label(master, text='Netmask')
        self.routeLabel = Label(master, text='Route IP')
        self.dnsLabel = Label(master, text='DNS Servers IP')
        self.ntpLabel = Label(master, text='NTP Servers IP')

        self.ipLabel.grid(row=0, column=1)
        self.netmaskLabel.grid(row=1, column=1)
        self.routeLabel.grid(row=3, column=1)
        self.dnsLabel.grid(row=4, column=1)
        self.ntpLabel.grid(row=5, column=1)



        self.ipAddress.grid(row=0, column=2)
        self.netmask.grid(row=1, column=2)
        self.route.grid(row=3, column=2)
        self.dns.grid(row=4, column=2)
        self.ntp.grid(row=5, column=2)

        # Initially, the entry fields are greyed out.
        if not isRead or (isRead and os.stat(sys.argv[1]).st_size == 0):
            self.ipAddress.config(state='disabled')
            self.netmask.config(state='disabled')
            self.route.config(state='disabled')
            self.dns.config(state='disabled')
            self.ntp.config(state='disabled')

        # These variables are traced, so anytime there is a change
        # the tracer function is called
        self.ipStatus = StringVar()
        self.ipStatus.trace('w', self.tracer)
        self.dnsStatus = StringVar()
        self.dnsStatus.trace('w', self.tracer)

        self.ntpStatus = StringVar()
        self.ntpStatus.trace('w', self.tracer)

        self.routerStatus = StringVar()
        self.routerStatus.trace('w', self.tracer)

        # For the check button
        self.var1 = IntVar()

        #These are the check buttons, pretty self-explanatory. Checked is for
        # DHCP on, unchecked is for static. DHCP is enabled by default.
        self.c1 = Checkbutton(master, text='DHCP Enabled', state = 'normal',
        	    command=lambda ent1 = self.ipAddress, ent2 = self.netmask,
                var = self.var1: self.ipConfig(ent1, ent2, var), variable=self.ipStatus,
        	    onvalue='DHCP', offvalue='Static')
        self.c1.grid(row=0, column=0)

        self.c2 = Checkbutton(master, text='DHCP Enabled', state = 'normal',
                command=lambda ent = self.route, var = self.var1: self.routerConfig(ent, var),
                variable=self.routerStatus, onvalue='DHCP', offvalue='Static')
        self.c2.grid(row=3, column=0)

        self.c3 = Checkbutton(master, text = 'DHCP Enabled', state = 'normal', command=lambda
                ent4 = self.dns, var = self.var1: self.dnsConfig( ent4, var),
                variable=self.dnsStatus, onvalue='DHCP',
                offvalue='Static')
        self.c3.grid(row = 4, column=0)

        self.c4 = Checkbutton(master, text = 'DHCP Enabled', state = 'normal', command=lambda ent5 = self.ntp,
                var = self.var1: self.ntpConfig(ent5, var),
                variable=self.ntpStatus, onvalue='DHCP',
                offvalue='Static')
        self.c4.grid(row = 5, column = 0)

        if not isRead or (isRead and os.stat(sys.argv[1]).st_size == 0):
            self.c1.select()
            self.c2.select()
            self.c3.select()
            self.c4.select()


        #The buttons, also self-explanatory.
        self.cancel = Button(master, text='Cancel', command=self.quit)
        self.cancel.grid(row=6, column=0, pady=4)



   #-----------------------------------------------------------------------#

    # This is the tracer function. It executes something every time there is
    # an action on the check button as well as an entry field. Its purpose is
    # to disable the save button unless all the input is valid.

    def tracer(self, var1, var2, var3): #needs four arguments

        if(self.ipStatus.get() == 'DHCP' and
            self.dnsStatus.get() == 'DHCP' and
            self.ntpStatus.get() == 'DHCP' and
            self.routerStatus.get() == 'DHCP'):
                self.save.config(state='normal')
                return

        if self.ipStatus.get() != 'DHCP':
            if not (VerifyStrings.singleStringCheck(self.ipAddress.get())   \
                and VerifyStrings.netMaskCheck(self.netmask.get())):
                    self.save.config(state='disabled')
                    return

        if self.dnsStatus.get() != 'DHCP':
            if not VerifyStrings.multipleStringCheck(self.dns.get()):
                self.save.config(state='disabled')
                return

        if self.ntpStatus.get() != 'DHCP':
            if not VerifyStrings.multipleStringCheck(self.ntp.get()):
                self.save.config(state='disabled')
                return

        if self.routerStatus.get() != 'DHCP':
            if not VerifyStrings.singleStringCheck(self.route.get()):
                self.save.config(state='disabled')
                return

        self.save.config(state='normal')


    # When the user has entered everything and the input is valid.
    def write_to_file(self):
        if self.routerStatus.get() == 'DHCP':
            inputFile.write('{\"defaultRoute\": \"dhcp\",')
        else:
            inputFile.write('{\"defaultRoute\": \"%s\",' % self.route.get())
        if self.ipStatus.get() == 'DHCP':
            inputFile.write('\"ipAddress\": \"dhcp\",  \"netmask\": \"dhcp\",')
        else:
            inputFile.write('\"ipAddress\": \"%s\", \"netmask\": \"%s\",' % (self.ipAddress.get(), convertToNum(self.netmask.get())))
        if self.dnsStatus.get() == 'DHCP':
            inputFile.write('\"dnsServers\": \"dhcp\",')
        else:
            inputFile.write('\"dnsServers\": \"%s\",' % self.dns.get())
        if self.ntpStatus.get() == 'DHCP':
            inputFile.write('\"ntpServers\": \"dhcp\"}\n')
        else:
            inputFile.write('\"ntpServers\": \"%s\"}\n' % self.ntp.get())
        inputFile.close()
        self.master.quit()

    # These xConfig functions enable or disable the entry fields depending on
    # whether or not DHCP is enabled for that particular field.

    def ipConfig(self, entry1, entry2, var):
        if self.ipStatus.get() == 'DHCP':
            entry1.configure(state = 'disabled')
            entry2.configure(state = 'disabled')

        else:
            entry1.configure(state = 'normal')
            entry2.configure(state = 'normal')



    def dnsConfig(self, entry4, var):
        if self.dnsStatus.get() == 'DHCP':
            entry4.configure(state = 'disabled')
        else:
            entry4.configure(state = 'normal')

    def ntpConfig(self, entry5, var):
        if self.ntpStatus.get() == 'DHCP':
            entry5.configure(state = 'disabled')
        else:
            entry5.configure(state = 'normal')

    def routerConfig(self, entry, var):
        if self.routerStatus.get() == 'DHCP':
            entry.configure(state='disabled')
        else:
            entry.configure(state = 'normal')
    #For cancel - restores previous file's values
    def quit(self):
        json.dump(data, inputFile)
        inputFile.close()
        self.master.quit()
 #-------------------------------------------------------------#

root = Tk()
data = None
inputFile = None

isRead = os.path.isfile(sys.argv[1])

#reads from file if it exists, and sets the values in the GUI
if isRead and os.stat(sys.argv[1]).st_size != 0:
    inputFile = open(sys.argv[1])
    data = json.load(inputFile)

    gui = NetworkGui(root, isRead, data)
    if data['ipAddress'] == 'dhcp':
        gui.c1.select()
        gui.ipAddress.configure(state='disabled')
        gui.netmask.configure(state='disabled')
    else:
        gui.c1.deselect()
        gui.ipAddress.insert(0, data['ipAddress'])
        gui.netmask.insert(0, data['netmask'])
    if data['defaultRoute'] == 'dhcp':
        gui.c2.select()
        gui.route.configure(state='disabled')
    else:
        gui.c2.deselect()
        gui.route.insert(0, data['defaultRoute'])
    if data['dnsServers'] == 'dhcp':
        gui.c3.select()
        gui.dns.configure(state='disabled')
    else:
        gui.c3.deselect()
        gui.dns.insert(0, data['dnsServers'])

    if data['ntpServers'] == 'dhcp':
        gui.c4.select()
        gui.ntp.configure(state='disabled')
    else:
        gui.c4.deselect()
        gui.ntp.insert(0, data['ntpServers'])

else:
    gui = NetworkGui(root, isRead, data)
inputFile = open(sys.argv[1], "w")

root.mainloop()
