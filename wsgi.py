import click, pytest, sys
import nltk
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.models import Student, Karma
from App.controllers import (
    create_student, create_staff, get_all_users_json,get_staff_by_staffID, get_staff_by_name, get_staff_by_username, 
    get_all_users, get_student_by_id, setup_nltk, get_full_name_by_student_id, 
    analyze_sentiment, create_review, get_staff_by_id, create_karma, get_karma, get_student_by_studentID)

from App.controllers.student import *
from App.controllers.staff import *
from App.controllers.review import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

#All the CLI command groups

staff_cli = AppGroup('staff', help = 'Staff object commands')
student_cli = AppGroup('student', help = 'Student object commands')
review_cli = AppGroup('review', help = 'Review object commands')

app.cli.add_command(staff_cli)
app.cli.add_command(student_cli)
app.cli.add_command(review_cli)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()

  print("Database initialized")


# Staff realted CLI commands   

@staff_cli.command("create", help = "Creates a staff")
@click.argument("staffid", default=12345)
@click.argument("username", default="RenWalker")
@click.argument("firstname", default="ren")
@click.argument("lastname", default="walker")
@click.argument("email", default="ren.walker@my.uwi.edu")
@click.argument("password", default="renpass")
def create_staff_command(staffid, username,firstname, lastname, email, password):
  create_staff(staffid, username,firstname, lastname, email, password)
  print(f'{username} created!')


@staff_cli.command("get_by_staffID", help = "retrieves a staff by staffID")
@click.argument("staffid", default=12345)
def get_staff_by_staffID_command(staffid):
  staff = get_staff_by_staffID(staffid)
  print(staff)


@staff_cli.command("get_by_name", help = "retrieves a staff by name")
@click.argument("firstname", default="ren")
@click.argument("lastname", default="walker")
def get_staff_by_name_command(firstname, lastname):
  staff = get_staff_by_name(firstname, lastname)
  print(staff)


@staff_cli.command("get_by_username", help = "retrieves a staff by username")
@click.argument("username", default="RenWalker")
def get_staff_by_username_command(username):
  staff = get_staff_by_username(username)
  print(staff)


@staff_cli.command("get_by_ID", help = "retrieves a staff by ID")
@click.argument("id", default=1)
def get_staff_by_id_command(id):
  staff = get_staff_by_id(id)
  print(staff)


# Student realted CLI commands      

@student_cli.command("create", help = "Creates a student")
@click.argument("studentid", default=816036000)
@click.argument("firstname", default="sly")
@click.argument("lastname", default="cooper")
@click.argument("karma", default=0)
def create_student_command(studentid, firstname, lastname, karma):
  create_student(studentid, firstname, lastname, karma)
  print(f'{firstname} {lastname} created!')
  print(f"Looking for student with ID: {studentid}")



@student_cli.command("get_by_studentID", help = "retrieves a student by studentID")
@click.argument("studentid", default=816036000)
def get_student_by_studnetID_command(studentid):
  student = get_student_by_studentID(studentid)
  print(student)


@student_cli.command("get_by_ID", help = "retrieves a student by ID")
@click.argument("id", default=1)
def get_student_by_id_command(id):
  student = get_student_by_id(id)
  print(student)


@student_cli.command("get_by_name", help = "retrieves a student by name")
@click.argument("firstname", default="sly")
@click.argument("lastname", default="cooper")
def get_student_by_name_command(firstname, lastname):
  student = get_student_by_name(firstname, lastname)
  print(student)


@student_cli.command("get_name_by_ID", help = "retrieves a student's name by ID")
@click.argument("id", default=1)
def get_full_name_by_student_id_command(id):
  student = get_full_name_by_student_id(id)
  print(student)


@student_cli.command("view_history", help = "views a student's karma history")
@click.argument("studentid", default=816036000)
def view_student_karma_history_command(studentid):
  history = view_student_karma_history(studentid)
  print(history)
  


# Review realted CLI commands           

@review_cli.command("create", help = "Creates a review")
@click.argument("staffid", default=12345)
@click.argument("studentid", default=816036000)
@click.argument("ispositive", default=True)
@click.argument("details", default="Well behaved student")
def create_review_command(staffid, studentid, ispositive, details):
  create_review(staffid, studentid, ispositive, details)
  print("review created\n")




# This command creates and initializes the database
# @app.cli.command("init", help="Creates and initializes the database")
# def initialize():
#   db.drop_all()
#   db.create_all()

#   create_student(studentID = "816036438",
#                  firstname="Billy",
#                  lastname="John",
#                  karma=0)

#   create_student(studentID = "81603938",
#                 firstname="Shivum",
#                 lastname="Praboocharan",
#                 karma=0)

#   create_student(studentID = "816039358",
#                 firstname="Jovani",
#                 lastname="Highley",
#                 karma=0)

#   create_student(studentID = "816035718",
#                 firstname="Kasim",
#                 lastname="Taylor",
#                 karma=0)

#   create_student(studentID = "81607491",
#                 firstname="Brian",
#                 lastname="Cheruiyot",
#                 karma=0)

#     #Creating staff
#   create_staff(staffID = 123,
#               username="tim",
#               firstname="Tim",
#               lastname="Long",
#               email="",
#               password="timpass")

#   create_staff(staffID = 4321,
#               username="vijay",
#               firstname="Vijayanandh",
#               lastname="Rajamanickam",
#               email="Vijayanandh.Rajamanickam@sta.uwi.edu",
#               password="vijaypass")

#   create_staff(staffID = 1987,
#               username="permanand",
#               firstname="Permanand",
#               lastname="Mohan",
#               email="Permanand.Mohan@sta.uwi.edu",
#               password="password")

#   staff = get_staff_by_id(1)
#   student1 = get_student_by_studnetid(816036438)
#   create_review(1, 1, True, "Behaves very well in class!")

#   student2 = get_student_by_studnetid(81603938)
#   create_review(1, 2, True, "Behaves very well in class!")
#   student3 = get_student_by_studnetid(816039358)
#   create_review(1, 3, True, "Behaves very well in class!")
#   student4 = get_student_by_studnetid(816035718)
#   create_review(1, 4, True, "Behaves very well in class!")
 

#   students = Student.query.all()

#   for student in students:
    
#     if student:
#       print(student.ID)
#       print(student.studentID)
#       print(student.firstName)
#       print(student.lastName)
#       print(student.karma)
#       print("\n")
#       db.session.commit()


@app.cli.command("nltk_test", help="Tests nltk")
@click.argument("sentence", default="all")
def analyze(sentence):
  analyze_sentiment(sentence)
  return


# '''
# User Commands
# '''

# # Commands can be organized using groups

# # create a group, it would be the first argument of the comand
# # eg : flask user <command>
# # user_cli = AppGroup('user', help='User object commands')

# # # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(id, username, firstname,lastname , password, email, faculty):
#     create_user(id, username, firstname,lastname , password, email, faculty)
#     print(f'{username} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')

@test.command("final", help="Runs ALL tests")
@click.argument("type", default="all")
def final_tests_command(type):
  if type == "all":
    sys.exit(pytest.main(["App/tests"]))

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "UserUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StudentUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StaffUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def review_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("recommendation", help="Run Recommendation tests")
@click.argument("type", default="all")
def recommendation_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "RecommendationUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "RecommendationIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("karma", help="Run Karma tests")
@click.argument("type", default="all")
def karma_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "KarmaUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "KarmaIntegrationTests"]))
  # else:
  #   sys.exit(pytest.main(["-k", "App"]))


@test.command("incidentreport", help="Run Incident Report tests")
@click.argument("type", default="all")
def incident_reports_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "IncidentReportUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "IncidentReportIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("accomplishment", help="Run Accomplishment tests")
@click.argument("type", default="all")
def accomplishment_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AccomplishmentUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AccomplishmentIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("grades", help="Run Grades tests")
@click.argument("type", default="all")
def grades_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "GradesUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "GradesIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("admin", help="Run Admin tests")
@click.argument("type", default="all")
def admin_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AdminUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
  # else:
  #     sys.exit(pytest.main(["-k", "App"]))


@test.command("nltk", help="Run NLTK tests")
@click.argument("type", default="all")
def nltk_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "NLTKUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "NLTKIntegrationTests"]))


@test.command("printstu", help="print get_student")
@click.argument("type", default="all")
def print_student(type):
  UniId = input("Enter student ID: ")
  student = get_student_by_id(UniId)
  if student:
    if type == "all":
      print(student.to_json(0))
    # elif type == "id":
    #     print(student.UniId)
    # elif type == "gpa":
    #     print(student.gpa)
    # elif type == "fullname":
    #     print(student.fullname)
    else:
      print(
          "Invalid type. Please choose 'all', 'id', 'gpa', 'fullname', or add more options."
      )
  else:
    print("Student not found with ID:", UniId)



app.cli.add_command(test)
