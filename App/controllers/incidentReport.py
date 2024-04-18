from App.models import IncidentReport
from App.database import db

from .student import (get_student_by_username, get_student_by_UniId)
from .staff import (get_staff_by_username, get_staff_by_id)


def create_incident_report(studentid, staffid, report, topic, points):
  student = get_student_by_UniId(studentid)
  staff = get_staff_by_id(staffid)
  if student is None:
    print(
        "[incidentReport.create_incident_report] Error occurred while creating new incident report: No student found."
    )
    return False
  if staff is None:
    print(
        "[incidentReport.create_incident_report] Error occurred while creating new incident report: No staff found."
    )
    return False

  newIncidentReport = IncidentReport(student.ID,
                                     staff.ID,
                                     topic,
                                     report,
                                     points,
                                     studentSeen=False)
  db.session.add(newIncidentReport)

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[incidentReport.create_incident_report] Error occurred while creating new incident report: ",
        str(e))
    db.session.rollback()
    return False


def delete_incident_report(reportID):
  report = IncidentReport.query.filter_by(id=reportID).first()
  if report:
    db.session.delete(report)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[incidentReport.delete_incident_report] Error occurred while deleting incident report: ",
          str(e))
      db.session.rollback()
      return False
  else:
    print(
        "[incidentReport.delete_incident_report] Error occurred while deleting incident report: Report not found."
    )
    return False


def get_incident_report(id):
  report = IncidentReport.query.filter_by(id=id).first()
  if report:
    return report
  else:
    return None


def get_total_incident_points(studentID):
  incidents = IncidentReport.query.filter_by(studentID=studentID).all()
  if incidents:
    sum = 0
    for incident in incidents:
      sum += incident.pointsDeducted
    return round (100* min(sum, 40) / 40, 2) #total sum of incidents cannot exceed 40 points
  return 0


def get_incident_reports(staffID):
  reports = IncidentReport.query.filter_by(madeByStaffId=staffID).all()
  if reports:
    return reports
  else:
    return []
