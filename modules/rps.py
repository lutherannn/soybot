import random


def rps(userChoice):
    choices = ["Rock", "Paper", "Scissors"]
    validChoice = False
    userWin = False
    cpuWin = False
    tie = False
    userChoice = userChoice.title()
    if userChoice not in choices:
        return "You did not enter a correct choice."
    else:
        validChoice = True
    if validChoice:
        cpuChoice = random.choice(choices)
        if userChoice == choices[0] and cpuChoice == choices[2]:
            userWin = True
        if userChoice == choices[1] and cpuChoice == choices[0]:
            userWin = True
        if userChoice == choices[2] and cpuChoice == choices[1]:
            userWin = True
        if cpuChoice == choices[0] and userChoice == choices[2]:
            cpuWin = True
        if cpuChoice == choices[1] and userChoice == choices[0]:
            cpuWin = True
        if cpuChoice == choices[2] and userChoice == choices[1]:
            cpuWin = True
        if userChoice == cpuChoice:
            tie = True

        if cpuWin and not tie:
            return f"I chose {cpuChoice}, I win!"
        if userWin and not tie:
            return f"I chose {cpuChoice}, you win, incel."
        if tie:
            return f"We both chose {cpuChoice}, we tied."
