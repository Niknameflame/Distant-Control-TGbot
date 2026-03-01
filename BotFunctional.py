import os
import pyautogui as gui
import webbrowser
from pathlib import Path
from dotenv import load_dotenv
path = Path(__file__).resolve().parent
load_dotenv(dotenv_path=path/"Bot.env")
Myself = int(os.getenv("ID"))

class FunctionConstructor:
    Ftype: str
    text: str
    special: str | None = None

def Check(SendingID):
    if Myself == SendingID:
        return True
    else:
        return False

def ShutdownPc():
    os.system("shutdown /s /f /t 0")
    return FunctionConstructor(Ftype="command",text="Succefully shutdowned")

def LockPc():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return FunctionConstructor(Ftype="command",text="Succefully locked")

def TakeScreenshot():
    photo = "Screen.png"
    gui.screenshot(path/photo)
    return FunctionConstructor(Ftype="photo",text="Succefully screenshoted",special=photo)

def LaunchSite(url):
    webbrowser.open_new_tab(url)
    return FunctionConstructor(Ftype="command",text="Succefully opened")