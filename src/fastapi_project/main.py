from fastapi import FastAPI, HTTPException
from fastapi_project.storage import load_grades, save_grades
from fastapi_project.validators import *

app = FastAPI()

### students graeds project : 

def find_student_by_id(students, student_id):
    for student in students:
        if student["student_id"] == student_id:
            return student

    return None



### GET all students
@app.get("/students")
def get_students():
    return load_grades()


### GET
@app.get("/students/{student_id}")
def get_student(student_id: int):
    students = load_grades()
    student = find_student_by_id(students, student_id)

    if student:
        return student

    raise HTTPException(
        status_code=404,
        detail="student not found")


### POST
@app.post("/students")
def add_student(student: dict):
    validate_student_id(student)
    validate_name(student)
    validate_grade(student)

    students = load_grades()

    students.append(student)

    save_grades(students)

    return student         

### PUT
@app.put("/students/{student_id}")
def update_student_grade(student_id: int, student: dict):
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


### DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = load_grades()
    student = find_student_by_id(students, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="student not found")

    students.remove(student)
    save_grades(students)

    return student