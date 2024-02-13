from App.models import recommendation
from App.database import db 

def create_Recommendation(studentID, staffID, approved):
    newRec = Recommendation(studentID, staffID, approved)
    db.session.add(newRec)

    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[recommendation.create_recommendation] Error occurred while creating new recommnedation: ", str(e))
        db.session.rollback()
        return False

def get_recommendations_student(createdByStudentID):
    recs = Recommendation.query.filter_by(createdByStudentID=createdByStudentID).all()
    if recs:
        return recs
    else:
        return []

def get_recommendations_staff(taggedStaffID):
    recs = Recommendation.query.filter_by(taggedStaffID=taggedStaffID).all()
    if recs:
        return recs
    else:
        return []

def approve_recommendation(ID):
    rec = Recommendation.query.filter_by(ID=ID).first()
    if rec:
        if rec.approved is True:
            print("[recommendation.approve_recommendation] Error occured while updating reccomendation: Recommendation is already approved. ")
            return False 
        else:
            rec.approved = True
            try:
                db.session.commit()
                return True
            except Exception as e:
                print("[recommendation.approve_recommendation] Error occurred while updating recommnedation: ", str(e))
                db.session.rollback()
                return False
    else:
        print("[recommendation.approve_recommendation] Error occurred while finding recommnedation: Recommendation not found")
        return False

        