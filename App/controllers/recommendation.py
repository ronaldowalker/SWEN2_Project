from App.models import Recommendation
from App.database import db
from .student import (get_student_by_UniId, get_student_by_id,
                      get_full_name_by_student_id)


def create_recommendation(studentID, staffID, approved, status,
                          currentYearOfStudy, details):

  student = get_student_by_id(studentID)
  newRec = Recommendation(student,
                          staffID,
                          approved,
                          status,
                          currentYearOfStudy,
                          details,
                          studentSeen=False)
  db.session.add(newRec)

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[recommendation.create_recommendation] Error occurred while creating new recommnedation: ",
        str(e))
    db.session.rollback()
    return False


def get_recommendations_student(createdByStudentID):
  recs = Recommendation.query.filter_by(
      createdByStudentID=createdByStudentID).all()
  if recs:
    return recs
  else:
    return []


def get_recommendation(id):
  recs = Recommendation.query.filter_by(ID=id).first()
  if recs:
    return recs
  else:
    return []


def get_recommendations_staff(taggedStaffID):
  recs = Recommendation.query.filter_by(taggedStaffID=taggedStaffID,
                                        approved=False).all()
  if recs:
    return recs
  else:
    return []


def get_recommendations_student_count(createdByStudentID):
  count = Recommendation.query.filter_by(createdByStudentID=createdByStudentID,
                                         approved=True,
                                         studentSeen=False).count()

  return count


def get_recommendations_staff_count(taggedStaffID):
  count = Recommendation.query.filter_by(taggedStaffID=taggedStaffID,
                                         approved=False).count()

  return count


def approve_recommendation(ID):
  rec = Recommendation.query.filter_by(ID=ID).first()
  if rec:
    if rec.approved is True:
      print(
          "[recommendation.approve_recommendation] Error occured while updating reccomendation: Recommendation is already approved. "
      )
      return False
    else:
      rec.approved = True
      try:
        db.session.commit()
        return True
      except Exception as e:
        print(
            "[recommendation.approve_recommendation] Error occurred while updating recommnedation: ",
            str(e))
        db.session.rollback()
        return False
  else:
    print(
        "[recommendation.approve_recommendation] Error occurred while finding recommnedation: Recommendation not found"
    )
    return False
