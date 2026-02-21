import os
import pyautogui as gui
from dotenv import load_dotenv
load_dotenv("Bot.env")
Myself = int(os.getenv("ID"))

def Check(SendingID):
    if SendingID == Myself:
        return True
    else:
        return False

def ShutdownPc():
    os.system("shutdown /s /f /t 0")

def LockPc():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def TakeScreenshot():
    path = "Screen.png"
    gui.screenshot(path)
    return path

def LaunchApp():
    
    return

def LaunchSite():
    
    return