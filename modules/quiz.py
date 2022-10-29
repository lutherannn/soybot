import random


def quiz():
    with open("questions.txt") as f:
        qa = []
        lines = f.readlines()
        question = random.choice(lines)
        if "country" in question:
            answer = lines[lines.index(question) + 1].replace("city ", "")
            question = question.replace("country ", "")
            qa.append(f"What is the capital of: {question}")
            qa.append(f"Answer: {answer}")
        if "city" in question:
            answer = lines[lines.index(question) - 1].replace("country ", "")
            question = question.replace("city ", "")
            qa.append(f"Which country/state has the capital city of: {question}")
            qa.append(f"Answer: {answer}")
    f.close()
    return qa
