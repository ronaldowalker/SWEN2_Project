from App.models import Student, Post
from App.database import db 
from .staff import(
    get_staff_by_username
)
from .post import (
    create_post
)

def create_student(username, firstname, lastname, email, password, faculty, admittedTerm, yearofStudy, degree):
    newStudent = Student(username, firstname, lastname, email, password, faculty, admittedTerm, yearofStudy, degree)
    db.session.add(student)
    try:
        db.session.commit()
        return True
        # return newStudent
    except Exception as e:
        print("[student.create_student] Error occurred while creating new student: ", str(e))
        db.session.rollback()
        return False
    

def get_student_by_id(id):
    student = Student.query.filter_by(ID=id).first()
    if student:
        return student
    else:
        return None

def get_student_by_username(username):
    student = Student.query.filter_by(username=username).first()
    if student:
        return student
    else:
        return None

def get_students_by_faculty(faculty):
    students = Student.query.filter_by(faculty=faculty).all()
    if students:
        return students
    else:
        return []

def get_students_by_degree(degree):
    students = Student.query.filter_by(degree=degree).all()
    if students:
        return students
    else:
        return []

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json


def student_create_post(studentUsername, teacherUsername, details):
    if create_post(studentUsername, teacherUsername, verified=False, details):
        return True
    else:
        print("[student.student_create_post] Error occurred while creating new post: create_post returned False")
        return False

def update_admittedTerm(studentID, newAdmittedTerm):
    student = get_student_by_id(studentID)
    if student:
        student.admittedTerm = newAdmittedTerm
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[student.update_admittedTerm] Error occurred while updating student admittedTerm:", str(e))
            db.session.rollback()
            return False
    else:
        print("[student.update_admittedTerm] Error occurred while updating student admittedTerm: Student "+studentID+" not found")
        return False

def update_yearofStudy(studentID, newYearofStudy):
    student = get_student_by_id(studentID)
    if student:
        student.yearofStudy = newYearofStudy
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[student.update_yearofStudy] Error occurred while updating student yearofStudy:", str(e))
            db.session.rollback()
            return False
    else:
        print("[student.update_yearofStudy] Error occurred while updating student yearofStudy: Student "+studentID+" not found")
        return False

def update_degree(studentID, newDegree):
    student = get_student_by_id(studentID)
    if student:
        student.degree = newDegree
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[student.update_degree] Error occurred while updating student degree:", str(e))
            db.session.rollback()
            return False
    else:
        print("[student.update_degree] Error occurred while updating student degree: Student "+studentID+" not found")
        return False