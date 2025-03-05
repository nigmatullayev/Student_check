from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict

app = FastAPI()

students: Dict[int, dict] = {}
tests: Dict[int, dict] = {}
test_results: List[dict] = []


class Student(BaseModel):
    id: int = Field(..., description="Unique identifier for the student")
    name: str = Field(..., min_length=2, max_length=50, description="Student's full name")
    email: str = Field(..., description="Student's email address")


class Test(BaseModel):
    id: int
    name: str
    max_score: int


class TestResult(BaseModel):
    student_id: int
    test_id: int
    score: int


class ResponseMessage(BaseModel):
    message: str


@app.post("/students/", response_model=ResponseMessage)
def create_student(student: Student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    students[student.id] = student.dict()
    return {"message": "Student added successfully"}


@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/students/")
def get_all_students():
    return list(students.values())


@app.post("/tests/", response_model=ResponseMessage)
def create_test(test: Test):
    if test.id in tests:
        raise HTTPException(status_code=400, detail="Test ID already exists")
    tests[test.id] = test.dict()
    return {"message": "Test added successfully"}


@app.get("/tests/{test_id}")
def get_test(test_id: int):
    test = tests.get(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@app.get("/tests/")
def get_all_tests():
    return list(tests.values())


@app.post("/results/", response_model=ResponseMessage)
def submit_test_result(result: TestResult):
    if result.student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if result.test_id not in tests:
        raise HTTPException(status_code=404, detail="Test not found")

    test_results.append(result.dict())
    return {"message": "Test result submitted successfully"}


@app.get("/results/student/{student_id}")
def get_student_results(student_id: int):
    results = [r for r in test_results if r["student_id"] == student_id]
    return results


@app.get("/results/test/{test_id}")
def get_test_results(test_id: int):
    results = [r for r in test_results if r["test_id"] == test_id]
    return results


@app.get("/results/test/{test_id}/average")
def get_average_score(test_id: int):
    scores = [r["score"] for r in test_results if r["test_id"] == test_id]
    if not scores:
        raise HTTPException(status_code=404, detail="No results found for this test")
    return {"average_score": sum(scores) / len(scores)}


@app.get("/results/test/{test_id}/highest")
def get_highest_score(test_id: int):
    scores = [r["score"] for r in test_results if r["test_id"] == test_id]
    if not scores:
        raise HTTPException(status_code=404, detail="No results found for this test")
    return {"highest_score": max(scores)}


@app.delete("/students/{student_id}", response_model=ResponseMessage)
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted successfully"}
