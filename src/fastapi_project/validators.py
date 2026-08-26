from fastapi import HTTPException
from fastapi_project.storage import load_grades


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



def validate_update(student):
    if "grade" in student:
        validate_grade(student)

    if "name" in student:
        validate_name(student)