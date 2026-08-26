from fastapi import FastAPI, HTTPException
import json

app = FastAPI()
"""
@app.get("/")
def home():
    return{"message": "Hello world"}


@app.get("/hello")
def hello():
    return {"message": "Hi FastAPI"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello {name}"}


@app.post("/hello")
def create_hello():
    return {"message": "Hello was created:)"}


@app.delete("/hello")
def delete_hello():
    return {"message": "Hello was deleted"}



# curl localhost:"8000/hello?name=bob"
# --> bob
@app.get("/hello")
def get_name(name):
    return name
"""


### students graeds project : 

def load_grades():  
    with open("grades.json") as file:
        return json.load(file)

@app.get("/students")
def get_students():
    return load_grades()


@app.get("/students/{student_id}")
def get_student(student_id: int):
    students = load_grades()

    for student in students:
        if student["student_id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="student not found"
    )


def validate_student_id(student):
    if "student_id" not in student:
        raise HTTPException(
            status_code=400,
            detail="student_id is must"
        )

    if type(student["student_id"]) is not int:
        raise HTTPException(
            status_code=400,
            detail="student_id must be an int"
        )

    if student["student_id"] <= 0:
        raise HTTPException(
            status_code=400,
            detail="student_id must be positive"
        )

    students = load_grades()

    for existing_student in students:
        if existing_student["student_id"] == student["student_id"]:
            raise HTTPException(
                status_code=400,
                detail="student_id already exists"
            )

def validate_name(student):
    if not (
        "name" in student
        and type(student["name"]) is str
        and student["name"] != ""
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid input, please check your input"
        )

def validate_grade(student):
    if not (
        "grade" in student
        and type(student["grade"]) is int
        and 0 <= student["grade"] <= 100
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid input, please check your input"
        )

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

