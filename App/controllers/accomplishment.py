from App.models import Accomplishment
from App.database import db
from .staff import (get_staff_by_name, get_staff_by_id)
from .student import (get_student_by_UniId, get_student_by_id,
                      get_full_name_by_student_id)


def create_accomplishment(studentID, verified, taggedStaffName, topic, details,
                          points, status):

  student = get_student_by_id(studentID)
  firstname, lastname = taggedStaffName.split(' ')
  staff = get_staff_by_name(firstname, lastname)
  if student is None:
    print(
        "[accomplishment.create_accomplishment] Error occurred while creating new accomplishment: No student found."
    )
    return False
  if staff is None:
    print(
        "[accomplishment.create_accomplishment] Error occurred while creating new accomplishment: No staff found."
    )
    return False

  newAccomplishment = Accomplishment(student=student,
                                     verified=False,
                                     taggedStaffId=staff.ID,
                                     topic=topic,
                                     details=details,
                                     points=points,
                                     status=status,
                                     studentSeen=False)

  db.session.add(newAccomplishment)

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[accomplishment.create_accomplishment] Error occurred while creating new accomplishment: ",
        str(e))
    db.session.rollback()
    return False


def delete_accomplishment(accomplishmentID):
  accomplishment = Accomplishment.query.filter_by(id=accomplishmentID).first()
  if accomplishment:
    db.session.delete(accomplishment)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[accomplishment.delete_accomplishment] Error occurred while deleting accomplishment: ",
          str(e))
      db.session.rollback()
      return False
  else:
    print(
        "[accomplishment.delete_accomplishment] Error occurred while deleting accomplishment: Accomplishment not found."
    )
    return False


def get_accomplishment(id):
  accomplishment = Accomplishment.query.filter_by(id=id).first()
  if accomplishment:
    return accomplishment
  else:
    return None


def get_total_accomplishment_points(studentID):
  accomplishments = get_accomplishments_by_studentID(studentID)
  if accomplishments:
    sum = 0
    for accomplishment in accomplishments:
      sum += accomplishment.points
    return round (100* min(sum, 75) / 75, 2) #total sum of accomplishments cannot exceed 75 points
  return 0


def get_accomplishments_by_studentID(studentID):
  accomplishments = Accomplishment.query.filter_by(
      createdByStudentID=studentID).all()
  if accomplishments:
    return accomplishments
  else:
    return []


def get_all_verified(studentID):
  accomplishments = Accomplishment.query.filter(
      (Accomplishment.createdByStudentID == studentID)
      & (Accomplishment.verified == True)).all()
  if accomplishments:
    return accomplishments
  else:
    return []


def get_requested_accomplishments(teacherID):
  accomplishments = Accomplishment.query.filter(
      (Accomplishment.taggedStaffId == teacherID)
      & (Accomplishment.verified == False)).all()
  if accomplishments:
    return accomplishments
  else:
    return []


def get_verified_accomplishments_count(studentID):

  count = Accomplishment.query.filter(
      (Accomplishment.createdByStudentID == studentID)
      & (Accomplishment.verified == True)).count()

  return count


def get_requested_accomplishments_count(teacherID):

  count = Accomplishment.query.filter(
      (Accomplishment.taggedStaffId == teacherID)
      & (Accomplishment.verified == False)).count()

  return count


def get_student_ids_by_tagged_staff_id(tagged_staff_id):
  accomplishments = Accomplishment.query.filter_by(
      taggedStaffId=tagged_staff_id).all()
  if accomplishments:
    student_ids = [
        accomplishment.createdByStudentID for accomplishment in accomplishments
    ]
    return student_ids
  else:
    return []
