import os
import random


def wheel():
    try:
        with open("names.txt", "r") as f:
            lines = f.readlines()
            f.close()
            return f"The wheel has chosen {random.choice(lines)}"
    except:
        print("File not found")
