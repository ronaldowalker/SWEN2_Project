from App.models import SchoolRecommendation
from App.database import db
from .student import (get_student_by_UniId, get_student_by_id,
                      get_full_name_by_student_id)


def create_school_recommendation(studentID, staffID, approved, status,currentYearOfStudy,details,school, program, schoolEmail):

  student = get_student_by_id(studentID)
  newRec = SchoolRecommendation(currentYearOfStudy,details,student, staffID, approved, status,school, program, schoolEmail)
  db.session.add(newRec)

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[school_recommendation.create_school_recommendation] Error occurred while creating new recommnedation: ",
        str(e))
    db.session.rollback()
    return False


def get_school_recommendations_student(createdByStudentID):
  recs = SchoolRecommendation.query.filter_by(
      createdByStudentID=createdByStudentID).all()
  if recs:
    return recs
  else:
    return []


def get_school_recommendation(id):
  recs = SchoolRecommendation.query.filter_by(ID=id).first()
  if recs:
    return recs
  else:
    return []


def get_school_recommendations_staff(taggedStaffID):
  recs = SchoolRecommendation.query.filter_by(taggedStaffID=taggedStaffID,
                                        approved=False).all()
  if recs:
    return recs
  else:
    return []


def approve_school_recommendation(ID):
  rec = SchoolRecommendation.query.filter_by(ID=ID).first()
  if rec:
    if rec.approved is True:
      print(
          "[school_recommendation.approve_school_recommendation] Error occured while updating reccomendation: school_recommendation is already approved. "
      )
      return False
    else:
      rec.approved = True
      try:
        db.session.commit()
        return True
      except Exception as e:
        print(
            "[school_recommendation.approve_school_recommendation] Error occurred while updating recommnedation: ",
            str(e))
        db.session.rollback()
        return False
  else:
    print(
        "[school_recommendation.approve_school_recommendation] Error occurred while finding recommnedation: school_recommendation not found"
    )
    return False
