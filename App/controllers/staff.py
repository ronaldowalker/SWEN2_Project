from App.models import Staff, Review, Student
from App.database import db 
# add create_review and get_student
from .review import create_review
from .student import(
    get_student_by_id,
    get_student_by_username,
    get_students_by_degree,
    get_students_by_faculty
)

def create_staff(username,firstname, lastname, email, password, faculty):
    newStaff = Staff(username,firstname, lastname, email, password, faculty)
    db.session.add(newStaff)
    
    try:
        db.session.commit()
        return True
        # can return if we need
        # return newStaff
    except Exception as e:
        print("[staff.create_staff] Error occurred while creating new staff: ", str(e))
        db.session.rollback()
        return False
    

def get_staff_by_id(id):
    staff = Staff.query.filter_by(ID=id).first()
    if staff:
        return staff
    else:
        return None

def get_staff_by_username(username):
    staff = Staff.query.filter_by(username=username).first()
    if staff:
        return staff
    else:
        return None

# need clarifcation for this 
# def studentSearch(username, studentID, faculty, degree):

# def reviewSearch():


def staff_create_review(staff, student, isPositive, points, details):
    if create_review(staff, student, isPositive, points,details):
        return True
    else:
        return False



