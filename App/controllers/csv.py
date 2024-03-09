
import csv
from App.models import *
from App.database import db

def populate_db_from_csv(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            student = Student(
                studentID=row['studentID'],
                firstname=row['firstname'],
                lastname=row['lastname']
            )
            # Check if student already exists
            existing_student = Student.query.filter_by(studentID=row['studentID']).first()
            if existing_student is None:
                db.session.add(student)
        db.session.commit()
