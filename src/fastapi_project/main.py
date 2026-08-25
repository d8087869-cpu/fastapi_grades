from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

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



### students graeds project : 

def load_grades():
    with open("grades.json") as file:
        return json.load(file)

@app.get("/students")
def get_students():
    return load_grades()


@app.get("/students/{name}")
def get_student(name: str):
    students = load_grades()

    for student in students:
        if student["name"].lower() == name.lower():
            return student

    raise HTTPException(
        status_code=404,
        detail="student not found"
    )