import questionary
import requests


BASE_URL = "http://127.0.0.1:8000"


def print_response(response):
    print("Status:", response.status_code)
    print("Response:", response.json())

def login():
    while True:
        choice = questionary.select(
            "How do you want to continue?",
            choices=[
                "Continue as Guest",
                "Login",
                "Sign in"
            ]
        ).ask()

        if choice == "Continue as Guest":
            return {
                "guest": True,
                "user_id": None
            }

        username = input("Enter username: ")
        password = input("Enter password: ")

        user_data = {
            "username": username,
            "password": password
        }

        if choice == "Login":
            response = requests.post(
                f"{BASE_URL}/login",
                json=user_data
            )

        elif choice == "Sign in":
            response = requests.post(
                f"{BASE_URL}/user/signin",
                json=user_data
            )

        print_response(response)

        if response.status_code == 200:
            response_data = response.json()

            return {
                "guest": False,
                "user_id": response_data["user_id"]
            }


def show_all_students(current_user):
    response = requests.get(f"{BASE_URL}/students",params=current_user)


    print_response(response)


def find_student(current_user):
    try:
        student_id = int(input("Enter student ID: "))
        response = requests.get(f"{BASE_URL}/students/{student_id}",params=current_user)
    except ValueError:
        print("status: 400")
        print("Invalid input")
        return

    print_response(response)

def add_student(current_user):
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
        json=student,params=current_user)

    print_response(response)


def update_student_grade(current_user):
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
        json=student,params=current_user)

    print_response(response)

def delete_student(current_user):
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("status: 400")
        print("Invalid input!!!")
        return

    response = requests.delete(
        f"{BASE_URL}/students/{student_id}",
        params=current_user
    )

    print_response(response)


def main():
    current_user = login()
    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Show all students",
                "Find a student",
                "Add a student",
                "Update student grade/name",
                "Delete a student",
                "Change User",
                "Exit"]).ask()

        if choice == "Show all students":
            show_all_students(current_user)

        elif choice == "Find a student":
            find_student(current_user)

        elif choice == "Add a student":
            add_student(current_user)

        elif choice == "Update student grade/name":
            update_student_grade(current_user)

        elif choice == "Delete a student":
            delete_student(current_user)

        elif choice == "Change User":
            current_user = login()

        elif choice == "Exit":
            break
        
if __name__ == "__main__":
    main()