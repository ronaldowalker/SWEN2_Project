import csv
from App.models import *
from App.controllers.student import create_student
from App.controllers.user import create_user
from App.database import db

def populate_db_from_csv(csv_file_path):
    try:
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                firstname = row.get('First name')
                lastname = row.get('Last name')
                username = f"{firstname}.{lastname}" if firstname and lastname else ""
                UniId = row.get('ID number')
                email = row.get('Email address')

                if None in [firstname, lastname, username, UniId, email]:
                    print("Some values in the row are None.")
                    continue

                new_user = create_student(
                    username=username,
                    UniId=UniId,
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    password="",  # No password provided from CSV
                    faculty="",
                    admittedTerm="",
                    degree="",
                    gpa="",
                )

                if new_user:
                    print(f"User created: {firstname} {lastname}")
                else:
                    print(f"Failed to create user: {firstname} {lastname}")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {str(e)}")


