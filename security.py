import win32api
import win32file
import time
import sys
import os.path
from win32com.shell import shell, shellcon
import win32com.client
from sec import send_email

print("Welcome to Tan USB Security System")
know_usb = []
Tan_usb = []
file1 = "Authenticated_USB.txt"
file2 = "System_USB.txt"

def checkfiles(file):
    exist = os.path.isfile(file)
    return exist

if not checkfiles(file1) and checkfiles(file2):
    raw_input("Please Run Generate.py First")
    sys.exit()


know_usb = [line.rstrip('\n') for line in open(file2)]
Tan_usb = [line.rstrip('\n') for line in open(file1)]

Tan_Found = 0

while 1:
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for a in drives:
        v = (a)
        d = win32file.GetDriveType(v)
        if d == 2:
            wmi = win32com.client.GetObject("winmgmts:")
            usb_found = []
            for usb in wmi.InstancesOf("Win32_USBHub"):
                usb_found.append(usb.DeviceID)
            #Windows USB
            diff_usb = list(set(usb_found) - set(know_usb))
            #My Tan USB
            without_tan_usb = []
            if len(diff_usb) > 0:
                nem = set(diff_usb) & set(Tan_usb)
                if len(nem) > 0:
                    if Tan_Found == 0:
                        print("Tan USB Found")
                    without_tan_usb = list(set(diff_usb) - set(Tan_usb))
                    Tan_Found = 1
                else:
                    Tan_Found = 0
                if len(nem) == 0 and len(without_tan_usb) > 0:
                    print("Not Authenticated With TanUSB " + "Removing the Drive " + str(v).replace("\\", "").replace(":", ""))
                    send_email(str("Not Authenticated With TanUSB " + "Removing the Drive " + str(v).replace("\\", "").replace(":", "")))
                    shell.SHChangeNotify(shellcon.SHCNE_DRIVEREMOVED, shellcon.SHCNF_PATH, str(v))
                elif len(nem) > 0 and len(without_tan_usb) > 0:
                    print("Different Drivers Found with Tan Authentication")

            # print(str(v).replace("\\", "").replace(":", "")+ " is a Removable Drive has connected to the PC and  have notified that")
            #send_email(str(v).replace("\\", "").replace(":", "")+ " is a Removable Drive")
            #
            time.sleep(2)