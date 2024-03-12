from App.models import Grades
from App.database import db

def create_grade(studentID ,course, grade):
    newGrade = Grades(studentID ,course, grade)

    db.session.add(newGrade)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[grades.create_grades] Error occurred while creating new grade: ", str(e))
        db.session.rollback()
        return False
    
def delete_grade(id):
    grade = Grades.query.filter_by(ID=id).first()

    if grade:
        db.session.delete(grade)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[grades.delete_grade] Error occurred while deleting grade: ", str(e))
            db.session.rollback()
            return False
    
    else:
        print("[grades.delete_grade] Error occurred while finding grade: ", str(e))
        return False

def get_grade(id):
    grade = Grades.query.filter_by(ID=id).first()
    if grade:
        return grade
    else:
        return None