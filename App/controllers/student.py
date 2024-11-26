from App.models import Student, IncreaseKarmaCommand, DecreaseKarmaCommand
from App.database import db


def create_student(firstname, lastname, karma):
  newStudent = Student(firstname, lastname, karma)
  db.session.add(newStudent)
  try:
    db.session.commit()
    return True
    # return newStudent
  except Exception as e:
    print(
        "[student.create_student] Error occurred while creating new student: ",
        str(e))
    db.session.rollback()
    return False


def get_student_by_id(id):
  student = Student.query.get(id)
  if student:
    return student
  else:
    return None


def get_student_by_name(firstname, lastname):
  students = Student.query.filter_by(firstname=firstname,
                                     lastname=lastname).all()
  if students:
    return students
  else:
    return []


def get_full_name_by_student_id(id):
  student = Student.query.filter_by(ID=id)
  if student:
    full_name = f"{student.firstname} {student.lastname}"
    return full_name
  else:
    return None


#returning all information about students
def get_all_students_json():
  students = Student.query.all()
  if not students:
    return []

  students_json = []
  for student in students:
    student_data = {
        'id': student.ID,
        'username': student.username,
        'firstname': student.firstname,
        'lastname': student.lastname,
        'karma': student.karma,
        # Include other details as needed
    }
    students_json.append(student_data)

  return students_json


def update_student_karma(student_id, is_positive):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"

    if is_positive:
        command = IncreaseKarmaCommand(student, 1)
    else:
        command = DecreaseKarmaCommand(student, 1)

    result = student.karma_history.execute_command(command)
    db.session.commit()  # Persist changes
    return result

def undo_last_karma_change(student_id):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"

    result = student.karma_history.undo_last_command()
    db.session.commit()  # Persist changes
    return result

def view_student_karma_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        return "Student not found"

    return student.karma_history.view_history()