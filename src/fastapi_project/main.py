from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

### students graeds project : 

def load_grades():  
    with open("grades.json") as file:
        return json.load(file)

@app.get("/students")
def get_students():
    return load_grades()

### GET
@app.get("/students/{student_id}")
def get_student(student_id: int):
    students = load_grades()

    for student in students:
        if student["student_id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="student not found")


def validate_student_id(student):
    if "student_id" not in student:
        raise HTTPException(
            status_code=400,
            detail="student_id is must")

    if type(student["student_id"]) is not int:
        raise HTTPException(
            status_code=400,
            detail="student_id must be an int")

    if student["student_id"] <= 0:
        raise HTTPException(
            status_code=400,
            detail="student_id must be positive")

    students = load_grades()

    for existing_student in students:
        if existing_student["student_id"] == student["student_id"]:
            raise HTTPException(
                status_code=400,
                detail="student_id already exists")

def validate_name(student):
    if not (
        "name" in student
        and type(student["name"]) is str
        and student["name"] != ""):
        raise HTTPException(
            status_code=400,
            detail="Invalid input, please check your input")

def validate_grade(student):
    if not (
        "grade" in student
        and type(student["grade"]) is int
        and 0 <= student["grade"] <= 100):
        raise HTTPException(
            status_code=400,
            detail="Invalid input, please check your input")
        
### POST
@app.post("/students")
def add_student(student: dict):
    validate_student_id(student)
    validate_name(student)
    validate_grade(student)

    students = load_grades()

    students.append(student)

    with open("grades.json", "w") as file:
        json.dump(students, file)

    return student         

### PUT
@app.put("/students/{student_id}")
def update_student_grade(student_id: int, student: dict):
    validate_grade(student)
    students = load_grades()
    found = False

    for student_data in students:
        if student_data["student_id"] == student_id:

            if "grade" in student:
                validate_grade(student)
                student_data["grade"] = student["grade"]

            if "name" in student:
                validate_name(student)
                student_data["name"] = student["name"]
            
            found = True

            
    if not found:
        raise HTTPException(
            status_code=404,
            detail="Student not found")


    with open("grades.json", "w") as file:
        json.dump(students, file)

    return student

### DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = load_grades()

    for student in students:
        if student["student_id"] == student_id:
            students.remove(student)

            with open("grades.json", "w") as file:
                json.dump(students, file)

            return student
    raise HTTPException(
        status_code=404,

        detail="student not found"
    )