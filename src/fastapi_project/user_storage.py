import csv


def load_users():
    with open("src/fastapi_project/users.csv") as file:
        reader = csv.DictReader(file)
        return list(reader)


def find_user_by_id(users,user_id):
    for user in users:
        if user["ID"] == str(user_id):
            return user
    return None


def find_user_by_username(users, username):
    for user in users:
        if user["username"] == username:
            return user

    return None



def save_user(user):
    with open("src/fastapi_project/users.csv", "a", newline="") as file:
        fieldnames = ["ID", "username", "password", "Type"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writerow(user)