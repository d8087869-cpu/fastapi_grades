import json


def load_grades():
    with open("grades.json") as file:
        return json.load(file)


def save_grades(students):
    with open("grades.json", "w") as file:
        json.dump(students, file)