from App.models import IncidentReport
from App.database import db 

from .student import(
    get_student_by_username
)
from .staff import(
    get_staff_by_username
)

def create_incident_report(studentUsername, staffUsername, report, points):
    student = get_student_by_username(studentUsername)
    staff = get_staff_by_username(taggedStaffUsername)
    if student is None:
        print("[incidentReport.create_incident_report] Error occurred while creating new incident report: No student found.")
        return False
    if staff is None:
        print("[incidentReport.create_incident_report] Error occurred while creating new incident report: No staff found.")
        return False

    newIncidentReport = IncidentReport(student.ID, staff.ID, report, points)
    db.session.add(newIncidentReport)

    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[incidentReport.create_incident_report] Error occurred while creating new incident report: ", str(e))
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
            print("[incidentReport.delete_incident_report] Error occurred while deleting incident report: ", str(e))
            db.session.rollback()
            return False
    else:
        print("[incidentReport.delete_incident_report] Error occurred while deleting incident report: Report not found.")
        return False