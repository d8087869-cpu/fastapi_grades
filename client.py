import questionary
import requests


BASE_URL = "http://127.0.0.1:8000"


def show_all_students():
    response = requests.get(f"{BASE_URL}/students")

    print(response.json())


def find_student():
    student_id = int(input("Enter student ID: "))
    response = requests.get(f"{BASE_URL}/students/{student_id}")

    print("Status:", response.status_code)
    print("Response:", response.json())

def add_student():
    student_id = int(input("Enter student ID: "))
    name = input("Enter student name: ")
    grade = int(input("Enter student grade: "))

    student = {
        "student_id": student_id,
        "name": name,
        "grade": grade
    }

    response = requests.post(
        f"{BASE_URL}/students",
        json=student
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

def main():
    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Show all students",
                "Find a student",
                "Add a student",
                "Update student grade",
                "Delete a student",
                "Exit"
            ]
        ).ask()

        if choice == "Show all students":
            show_all_students()

        elif choice == "Find a student":
            find_student()

        elif choice == "Add a student":
            add_student()

        elif choice == "Exit":
            break
        
if __name__ == "__main__":
    main()