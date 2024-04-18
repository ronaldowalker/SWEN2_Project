from App.models import JobRecommendation
from App.database import db
from flask_mailman import EmailMultiAlternatives
from .student import (get_student_by_UniId, get_student_by_id,
                      get_full_name_by_student_id)


def create_job_recommendation(studentID, staffID, approved, status,
                              currentYearOfStudy, details, company, position,
                              companyEmail):

  student = get_student_by_id(studentID)
  newRec = JobRecommendation(currentYearOfStudy, details, student, staffID,
                             approved, status, company, position,
                             companyEmail)
  db.session.add(newRec)

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[job_recommendation.create_job_recommendation] Error occurred while creating new recommnedation: ",
        str(e))
    db.session.rollback()
    return False


def get_job_recommendations_student(createdByStudentID):
  recs = JobRecommendation.query.filter_by(
      createdByStudentID=createdByStudentID).all()
  if recs:
    return recs
  else:
    return []


def get_job_recommendation(id):
  recs = JobRecommendation.query.filter_by(ID=id).first()
  if recs:
    return recs
  else:
    return []


def get_job_recommendations_staff(taggedStaffID):
  recs = JobRecommendation.query.filter_by(taggedStaffID=taggedStaffID,
                                           approved=False).all()
  if recs:
    return recs
  else:
    return []


def approve_job_recommendation(ID):
  rec = JobRecommendation.query.filter_by(ID=ID).first()
  if rec:
    if rec.approved is True:
      print(
          "[job_recommendation.approve_job_recommendation] Error occured while updating reccomendation: job_recommendation is already approved. "
      )
      return False
    else:
      rec.approved = True
      try:
        db.session.commit()
        return True
      except Exception as e:
        print(
            "[job_recommendation.approve_job_recommendation] Error occurred while updating recommnedation: ",
            str(e))
        db.session.rollback()
        return False
  else:
    print(
        "[job_recommendation.approve_job_recommendation] Error occurred while finding recommnedation: job_recommendation not found"
    )
    return False
