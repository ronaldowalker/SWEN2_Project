from App.models import Student
from App.database import db
from App.karmaManager import KarmaManager  # Import KarmaManager

karma_manager = KarmaManager()  # Instantiate the KarmaManager

def create_student(studentID, firstname, lastname, karma):
    newStudent = Student(studentID, firstname, lastname, karma)
    db.session.add(newStudent)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[student.create_student] Error occurred while creating new student:", str(e))
        db.session.rollback()
        return False


def get_student_by_id(id):
    student = Student.query.get(id)
    if student:
        return student
    else:
        return None

def get_student_by_studnetid(id):
    student = Student.query.filter_by(studentID = id)
    if student:
        return student
    else:
        return None


def get_student_by_name(firstname, lastname):
    students = Student.query.filter_by(firstname=firstname, lastname=lastname).all()
    if students:
        return students
    else:
        return []


def get_full_name_by_student_id(id):
    student = Student.query.filter_by(ID=id).first()
    if student:
        full_name = f"{student.firstname} {student.lastname}"
        return full_name
    else:
        return None


# Returning all information about students
def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []

    students_json = []
    for student in students:
        student_data = {
            'id': student.ID,
            'studentID': student.studentID,
            'username': student.username,
            'firstname': student.firstname,
            'lastname': student.lastname,
            'karma': student.karma,
        }
        students_json.append(student_data)

    return students_json


def update_student_karma(student_id, is_positive):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"

    # Use KarmaManager to update karma
    if is_positive:
        result = karma_manager.increase_karma(student, 1)
    else:
        result = karma_manager.decrease_karma(student, 1)

    db.session.commit()  # Persist changes
    return result


def undo_last_karma_change(student_id):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"

    result = karma_manager.undo_last_action(student)
    db.session.commit()  # Persist changes
    return result


def view_student_karma_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"

    return karma_manager.view_history(student)
