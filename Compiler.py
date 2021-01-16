import shutil
import PyInstaller.__main__
import os
import inquirer
import inquirer.themes
import termcolor
from datetime import datetime

AppDataPath = os.path.join(os.getenv('APPDATA'), "KL Corporation", "Mastermind Compiler")
BuildsPath = os.path.join(AppDataPath, "Builds")
os.makedirs(BuildsPath, exist_ok=True)
WorkPath = os.path.join(AppDataPath, "cache", "work")
CachePath = os.path.join(AppDataPath, "cache")
if os.path.isdir(CachePath): shutil.rmtree(CachePath)

parentDir = os.path.dirname(os.path.abspath(__file__))

BuildPath = os.path.join(BuildsPath, "build_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
fileName = "Mastermind.py"
iconName = "default_logo.ico"
    
PyInstaller.__main__.run([
    "--noconfirm",
    "--distpath",
    BuildPath,
    "--workpath",
    WorkPath,
    "--specpath",
    CachePath,
    "--windowed",
    "--icon",
    f"{parentDir}/{iconName}",
    f"{parentDir}/{fileName}"
])

print(termcolor.colored(f"Built Mastermind at " + os.path.join(BuildPath, os.path.splitext(fileName)[0], os.path.splitext(fileName)[0] + ".exe"), "green"))

if os.path.isdir(os.path.join(AppDataPath, "cache")): shutil.rmtree(os.path.join(AppDataPath, "cache"))