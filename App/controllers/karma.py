from App.models import Karma
from App.database import db 
from .review import (
    get_total_points
)

def get_karma(karmaID):
    karma = Karma.query.filter_by(karmaID=karmaID).first()
    if karma:
        return karma
    else:
        return None

def create_karma(studentID):
    newKarma = Karma(points=0.0, rank=-99, studentID=studentID)
    db.session.add(newKarma)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[karma.create_karma] Error occurred while creating new karma: ", str(e))
        return False

def calculate_karma(studentID):
    karma = get_total_points(studentID)
    return karma

def update_karma(studentID):
    karmaScore = Karma.query.filter_by(studentID=studentID).first()
    if karmaScore:
        karmaScore.points = calculate_karma(studentID)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[karma.update_karma] Error occurred while updating karma:", str(e))
            db.session.rollback()
            return False
    else:
        print("Karma score not found for student:", studentID)
        return False

