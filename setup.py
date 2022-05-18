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
