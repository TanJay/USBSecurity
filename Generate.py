import win32api
import win32file
import time
import sys
import os
import os.path
from win32com.shell import shell, shellcon
import win32com.client
#variables
file1 = "Authenticated_USB.txt"
file2 = "System_USB.txt"
present_usb = []
usb_system = []
found_usb = []
print("Welcome to Secure USB Wizard \n")
def checkfiles(file):
    exist = os.path.isfile(file)
    return exist

def detect():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    global found_usb
    for a in drives:
        v = (a)
        d = win32file.GetDriveType(v)
        if d == 2:
            found_usb.append("We Found " + str(v) + " as USB")
    if len(found_usb) > 0:
        found = 1
        return found
    else:
        found = 0
        return found

def devInfo():
    wmi = win32com.client.GetObject("winmgmts:")
    usb_listed = []
    for usb in wmi.InstancesOf("Win32_USBHub"):
        usb_listed.append(usb.DeviceID)
    return usb_listed



val = checkfiles(file1)
val1 = checkfiles(file2)
if val and val1:
    print("Previous Files Found")
    num = raw_input("Press Y to Delete Previous and Continue and N to Exit")
    if num.lower() == "y":
        print("Deleting and Starting Process")
        os.remove(file1)
        os.remove(file2)
    elif num.lower() == "n":
        print("Exiting")
        sys.exit(0)
elif val:
    os.remove(file1)
elif val1:
    os.remove(file2)




found = detect()
while found == 1:
    for a in found_usb: print(a)
    print("\nPlease Remove USB Devices \n")
    raw_input("Please Press Enter When Your Done Removing")
    found_usb = []
    found = detect()
print("No USB Found")
print("Scanning the USB Interfaces")
time.sleep(10)
usb_system = devInfo()
for a in usb_system: print( a + " have been authenticated as System \n")
raw_input("Please Press Enter After Plugging in USB you want to authenticate")
now_usb = detect()
while now_usb == 0:
    print("Please Enter a USB")
    raw_input("Please Press Enter When Insert Your USB")
    now_usb = detect()

print("\n Please Wait a moment")
present_usb = devInfo()
myusb = list(set(present_usb) - set(usb_system))
print(myusb)
raw_input("Please Press Enter to Continue")
fo = open(file2, "wb")
for a in usb_system:
    fo.write(a + "\n")
print(fo.name + " is Generated")
fo.close()
bo = open(file1 , "wb")
for b in myusb:
    bo.write(b + "\n")
print(bo.name + " is Genarated")
bo.close()
print("Generating Completed\nPlease edit the file Sec.py for email Notifications")