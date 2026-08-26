import questionary
import requests


BASE_URL = "http://127.0.0.1:8000"


def show_all_students():
    response = requests.get(f"{BASE_URL}/students")

    print(response.json())


def find_student():
    try:
        student_id = int(input("Enter student ID: "))
        response = requests.get(f"{BASE_URL}/students/{student_id}")
    except ValueError:
        print("status: 400")
        print("Invalid input")
        return

    print("Status:", response.status_code)
    print("Response:", response.json())

def add_student():
    try:
        student_id = int(input("Enter student ID: "))
        name = input("Enter student name: ")
        grade = int(input("Enter student grade: "))
    except ValueError:
        print("status: 404")
        print("Inavlid input!!!")
        return
    student = {
        "student_id": student_id,
        "name": name,
        "grade": grade}

    response = requests.post(
        f"{BASE_URL}/students",
        json=student)

    print("Status:", response.status_code)
    print("Response:", response.json())


def update_student_grade():
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("status: 404")
        print("Invalid error")
        return
    
    student = {}

    update_grade = questionary.confirm(
        "Do you want to update the grade?").ask()

    if update_grade:
        try:
            grade = int(input("Enter new grade: "))
            student["grade"] = grade
        except ValueError:
            print("Status: 400")
            print("Invalid input!!!")
            return


    change_name = questionary.confirm(
        "Do you want change the name?").ask()

    if change_name:
        student["name"] = input("Enter new name: ")

    response = requests.put(
        f"{BASE_URL}/students/{student_id}",
        json=student)

    print("Status:", response.status_code)
    print("Response:", response.json())


def delete_student():
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("status: 400")
        print("Invalid input!!!")
        return

    response = requests.delete(f"{BASE_URL}/students/{student_id}")

    print("Status", response.status_code)
    print("Response",response.json())


def main():
    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Show all students",
                "Find a student",
                "Add a student",
                "Update student grade/name",
                "Delete a student",
                "Exit"]).ask()

        if choice == "Show all students":
            show_all_students()

        elif choice == "Find a student":
            find_student()

        elif choice == "Add a student":
            add_student()

        elif choice == "Update student grade/name":
            update_student_grade()

        elif choice == "Delete a student":
            delete_student()

        elif choice == "Exit":
            break
        
if __name__ == "__main__":
    main()