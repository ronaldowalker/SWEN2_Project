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

def create_karma(student):
    newKarma = Karma(student, student.ID, points=0.0, rank=-99)
    db.session.add(newKarma)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[karma.create_karma] Error occurred while creating new karma: ", str(e))
        return False

def calculate_karma(student):
    karma = get_total_points(student.ID)
    return karma

def update_karma(student):
    karmaScore = Karma.query.filter_by(studentID=student.ID).first()
    if karmaScore:
        karmaScore.points = calculate_karma(student)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[karma.update_karma] Error occurred while updating karma:", str(e))
            db.session.rollback()
            return False
    else:
        print("Karma score not found for student:", student.ID)
        return False

