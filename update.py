import os
import requests
print("Ensure soybot is not running before running the updater...")
print("Press any key to continue...")
os.system("pause" if os.name == "nt" else "read")

print("Downloading soybot")
soyUrl = "https://raw.githubusercontent.com/lutherannn/soybot/main/soybot.py"
r = requests.get(soyUrl)

open("soybot.tmp", "x").write(r.text)
os.remove("soybot.py")

if not os.path.exists("soybot.py"):
    os.rename("soybot.tmp", "soybot.py")
else:
    print("Update failed, to manually update, run git pull from root directory. Or download zip file from github.")

print("Downloading installer")
insUrl = "https://raw.githubusercontent.com/lutherannn/soybot/main/setup.py"
r = requests.get(insUrl)

open("setup.tmp", "x").write(r.text)
os.remove("setup.py")

if not os.path.exists("setup.py"):
    os.rename("setup.tmp", "setup.py")

lchoice = input("Done. Relaunch soybot? y/n: ")
if lchoice == "y" or lchoice == "yes":
    os.system("python soybot.py")
os.system("exit")
