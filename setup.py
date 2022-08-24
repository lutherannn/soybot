import os

if os.path.isfile("requirements.txt"):
    os.system("pip install -r requirements.txt")
else:
    print("requirements.txt is missing, skipping")

if not os.path.isfile(".env"):
    try:
        with open(".env", "w") as f:
            discordKey = input("Discord API Key: ")
            f.write(f"DISCORD_TOKEN={discordKey}")
            f.write("\n")
            chanID = input("Main channel ID: ")
            f.write(f"QUOTE_CHAN={chanID}")
            f.close()
    except FileNotFoundError:
        print("File not Found\n")
else:
    print("\n.env file already exists, skipping creating .env")
    print(
        "Either edit the .env file on your own, or delete it and run the setup again to automatically add it\n"
    )

if not os.path.isfile("reponses.txt"):
    try:
        with open("responses.txt", "w") as f:
            f.write("Response One\nResponse Two\nEtc")
            f.close()
    except FileNotFoundError:
        print("File not Found\n")
else:
    print("responses.txt file already exists, skipping creating reponses.txt\n")
    print(
        "Either edit the requirements.txt file on your own, or delete it and run the setup again to automatically add it\n"
    )

if not os.path.isfile("names.txt"):
    try:
        with open("names.txt", "w") as f:
            f.write("Name1\nName2\nEtc")
            f.close()
    except FileNotFoundError:
        print("File not Found")
else:
    print("names.txt file already exists, skipping creating names.txt\n")
    print(
        "Either edit the names.txt file on your own, or delete it and run the setup again to automatically add it"
    )

quoteChoice = input(
    "Have a chance of sending an inspirational quote every hour (y/n)? "
)
if quoteChoice == "y" or quoteChoice == "yes":
    open(".quote", "x")
    print(".quote file created, soybot will send quotes")
else:
    print(".quote file not created, soybot will not send quotes")

os.system("pause" if os.name == "nt" else "read")
