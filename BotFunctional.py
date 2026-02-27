import os
import pyautogui as gui
import webbrowser
from pathlib import Path
from dotenv import load_dotenv
path = Path(__file__).resolve().parent
load_dotenv(dotenv_path=path/"Bot.env")
Myself = int(os.getenv("ID"))

def Check(SendingID):
    if Myself == SendingID:
        return True
    else:
        return False

def ShutdownPc():
    os.system("shutdown /s /f /t 0")

def LockPc():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def TakeScreenshot():
    photo = "Screen.png"
    gui.screenshot(path/photo)
    return photo

def LaunchSite():

    return