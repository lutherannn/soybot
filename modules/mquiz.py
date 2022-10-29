import random


def mquiz():
    qa = []
    ops = ["+", "-", "*"]
    num1, num2 = random.randrange(1, 100), random.randrange(1, 100)
    operator = random.choice(ops)
    qa.append(f"What is: {num1} {operator} {num2}")
    if operator == "+":
        answer = num1 + num2
    if operator == "-":
        answer = num1 - num2
    if operator == "*":
        answer = num1 * num2
    sleep(5)
    qa.append(f"Solution: {answer}")
    return qa
