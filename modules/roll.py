import random


def roll():
    nums = ""
    for _ in range(10):
        nums += str(random.randrange(0, 9))
    return nums
