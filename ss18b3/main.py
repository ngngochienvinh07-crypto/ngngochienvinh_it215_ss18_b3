from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from schema import EnrollmentCreate, EnrollmentResponse
from service import create_enrollment, get_student_courses
import model
app = FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {"message": "Course Enrollment API"}


@app.post(
    "/enrollments",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_student(
    data: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    return create_enrollment(data, db)


@app.get("/students/{student_id}/courses")
def student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):
    return get_student_courses(student_id, db)