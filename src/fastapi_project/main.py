from fastapi import FastAPI, HTTPException
from fastapi_project.storage import load_grades, save_grades
from fastapi_project.validators import *
from fastapi_project.user_storage import *
from fastapi_project.roles import has_permission
from pydantic import BaseModel


app = FastAPI()

class UserRequest(BaseModel):
    username: str
    password: str

### students graeds project : 

def find_student_by_id(students, student_id):
    for student in students:
        if student["student_id"] == student_id:
            return student

    return None



### GET all students
@app.get("/students")
def get_students(user_id: int | None = None, guest:bool=False):
    check_permission(user_id, guest,"GET")
    return load_grades()


### GET
@app.get("/students/{student_id}")
def get_student(student_id: int, user_id: int | None = None, guest: bool=False):

    check_permission(user_id,guest, "GET")

    students = load_grades()
    student = find_student_by_id(students, student_id)

    if student:
        return student

    raise HTTPException(
        status_code=404,
        detail="student not found")


### POST
@app.post("/students")
def add_student(student: dict, user_id: int | None = None, guest: bool = False):
    check_permission(user_id, guest, "POST")

    validate_student_id(student)
    validate_name(student)
    validate_grade(student)

    students = load_grades()

    students.append(student)

    save_grades(students)

    return student         

### PUT
@app.put("/students/{student_id}")
def update_student_grade(student_id: int, student: dict,user_id: int | None = None,guest: bool = False):
    check_permission(user_id, guest, "PUT")

    validate_update(student)

    students = load_grades()
    student_data = find_student_by_id(students, student_id)

    if not student_data:
        raise HTTPException(
            status_code=404,
            detail="Student not found")

    if "grade" in student:
        student_data["grade"] = student["grade"]

    if "name" in student:
        student_data["name"] = student["name"]
            
    save_grades(students)
    return student



@app.post("/login")
def login(user_data: UserRequest):
    users = load_users()

    username = user_data.username
    password = user_data.password

    user = find_user_by_username(users, username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password")

    if user["password"] != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password")

    return {
        "user_id": user["ID"],
        "username": user["username"],
        "Type": user["Type"]}



@app.post("/user/signin")
def signin(user_data: UserRequest):
    users = load_users()

    username = user_data.username
    password = user_data.password

    user = find_user_by_username(users, username)

    if user is not None:
        raise HTTPException(
            status_code=401,
            detail="Username already exists")

    new_id = len(users) +1

    new_user = {
        "ID": new_id,
        "username": username,
        "password": password,
        "Type": "USER"}
    
    save_user(new_user)
    return {
        "user_id": new_user["ID"],
        "username": new_user["username"],
        "Type": new_user["Type"]
    }



### DELETE
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    user_id: int | None = None,
    guest: bool = False
):
    check_permission(user_id, guest, "DELETE")

    students = load_grades()
    student = find_student_by_id(students, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="student not found"
        )

    students.remove(student)
    save_grades(students)

    return student


def check_permission(user_id=None, guest=False, method="GET"):
    if guest:
        if has_permission("GUEST",method):
            return

        raise HTTPException(status_code=403, detail="You do not have permission")

    users = load_users()
    user = find_user_by_id(users, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not has_permission(user["Type"], method):
        raise HTTPException(status_code=403,detail="You do not have permission")


