import secrets
import string
import csv
from App.models import *
from App.controllers.student import create_student
from App.controllers.user import create_user
from App.database import db


def generate_random_password(length=12):
  alphabet = string.ascii_letters + string.digits + string.punctuation
  return ''.join(secrets.choice(alphabet) for _ in range(length))


def populate_db_from_csv(csv_file_path):
  try:
    with open(csv_file_path, newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        # Generate a default username if it's missing

        username = f"{row.get('First name')}.{row.get('Last name')}"
        UniId = row.get('ID number')
        # Generate a random password
        password = generate_random_password()

        # Create a user using the parameters from the CSV
        new_user = create_student(
            username=username,
            UniId=UniId,
            firstname=row.get('First name'),
            lastname=row.get('Last name'),
            email=row.get('Email address'),
            password=password,
            faculty="",
            admittedTerm="",
            degree="",
            gpa="",
        )

        # Check if the user was successfully created
        if new_user:
          print(f"User created: {row['First name']} {row['Last name']}")
        else:
          print(f"Failed to create user: {row['First name']} {row['Last name']}")
  except Exception as e:
    print(f"An error occurred while processing the CSV file: {str(e)}")
