from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from model import Student, Course, Enrollment
from schema import EnrollmentCreate


def create_enrollment(data: EnrollmentCreate, db: Session):
    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is inactive"
        )
    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    if course.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is closed"
        )
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == data.student_id,
        Enrollment.course_id == data.course_id
    ).first()
    if enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already enrolled"
        )
    total = db.query(func.count(Enrollment.id)).filter(
        Enrollment.course_id == data.course_id
    ).scalar()

    if total >= course.max_students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is full"
        )
    new_enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


def get_student_courses(student_id: int, db: Session):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()

    courses = []

    for enrollment in enrollments:
        course = db.query(Course).filter(
            Course.id == enrollment.course_id
        ).first()

        if course:
            courses.append({
                "id": course.id,
                "name": course.name
            })

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": courses
    }