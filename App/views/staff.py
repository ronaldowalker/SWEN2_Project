from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime

from App.models import Student, Staff, User
from App.controllers import (
    jwt_authenticate,  get_student_by_id, get_staff_by_id,
    get_staff_by_id, create_review, get_karma,
    analyze_sentiment, calculate_ranks, update_total_points,
    calculate_academic_points, calculate_accomplishment_points,
    calculate_review_points)

staff_views = Blueprint('staff_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''

@staff_views.route('/StaffHome', methods=['GET'])
def get_StaffHome_page():

  staff_id = current_user.get_id()
  staff=get_staff_by_id(staff_id)

  return render_template('Staff-Home.html')

@staff_views.route('/staffhome', methods=['GET'])
def get_staffHome_page():

  staff_id = current_user.get_id()

  return render_template('Staff-Home.html')


@staff_views.route('/incidentReport', methods=['GET'])
def staff_ir_page():
  return render_template('IncidentReport.html')


@staff_views.route('/get_student_name', methods=['POST'])
def get_student_name():
  student_id = request.json['studentID']

  student = get_student_by_id(student_id)

  return jsonify({'studentName': student.fullname})


@staff_views.route('/studentSearch', methods=['GET'])
def student_search_page():
  return render_template('StudentSearch.html')


@staff_views.route('/reviewSearch', methods=['GET'])
def review_search_page():
  return render_template('ReviewSearch.html')


@staff_views.route('/mainReviewPage', methods=['GET'])
def mainReviewPage():
  return render_template('CreateReview.html')
  
@staff_views.route('/createReview', methods=['POST'])
def createReview():
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)

  data = request.form
  studentID = data['studentID']
  studentName = data['name']
  points = int(data['points'])
  print("Start points:", points)
  num = data['num']
  personalReview = data['manual-review']
  details = data['selected-details']
  firstname, lastname = studentName.split(' ')
  student = get_student_by_id(studentID)

  if personalReview:
    details += f"{num}. {personalReview}"
    nltk_points = analyze_sentiment(personalReview)
    rounded_nltk_points = round(float(nltk_points))
    points += int(rounded_nltk_points)
    print("Final points:", points)

  if points > 0:
    positive = True
  else:
    positive = False

  if student:
    review = create_review(staff, student, positive, points, details)
    message = f"You have created a review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)
  else:
    message = f"Error creating review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/searchStudent', methods=['GET'])
@login_required
def studentSearch():

  name = request.args.get('name')
  studentID = request.args.get('studentID')
  faculty = request.args.get('faculty')
  degree = request.args.get('degree')

  query = Student.query

  if name:
    # Check if the name contains both a first name and a last name
    name_parts = name.split()
    if len(name_parts) > 1:
      # If it contains both first name and last name, filter by full name
      query = query.filter_by(fullname=name)
    else:
      # If it contains only one name, filter by either first name or last name
      query = query.filter(
          or_(Student.firstname.ilike(f'%{name}%'),
              Student.lastname.ilike(f'%{name}%')))

  if studentID:
    query = query.filter_by(UniId=studentID)

  if faculty:
    query = query.filter_by(faculty=faculty)

  if degree:
    query = query.filter_by(degree=degree)

  students = query.all()

  if students:
    return render_template('ssresult.html', students=students)
  else:
    message = "No students found"
    return render_template('StudentSearch.html', message=message)


@staff_views.route('/allAchievementApproval', methods=['GET'])
@login_required
def allAchievementApproval():

  staff_id = current_user.get_id()
  return render_template('ProposedAchievements.html')



@staff_views.route('/view-all-student-reviews/<string:uniID>', methods=['GET'])
@login_required
def view_all_student_reviews(uniID):

  student = get_student_by_id(uniID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentReviews.html', student=student,user=user)


@staff_views.route('/view-all-student-incidents/<string:uniID>',
                   methods=['GET'])
@login_required
def view_all_student_incidents(uniID):

  student = get_student_by_id(uniID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentIncidents.html', student=student,user=user)


@staff_views.route('/view-all-student-achievements/<string:uniID>',
                   methods=['GET'])
@login_required
def view_all_student_achievements(uniID):
  student = Student.query.filter_by(UniId=uniID).first()
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentAchivements.html', student=student,user=user)


@staff_views.route('/getStudentProfile/<string:uniID>', methods=['GET'])
@login_required
def getStudentProfile(uniID):
  student = Student.query.filter_by(UniId=uniID).first()

  if student is None:
    student = Student.query.filter_by(ID=uniID).first()

  user = User.query.filter_by(ID=student.ID).first()
  karma = get_karma(student.ID)

  if karma:

    calculate_academic_points(student.ID)
    calculate_accomplishment_points(student.ID)
    calculate_review_points(student.ID)
    #Points: academic (0.4),accomplishment (0,3 shared)
    #missing points: incident , reivew
    #calculate the accomplishment - incident for 0.3 shared
    #assign review based on 1 time reivew max 5pts for 0.3
    update_total_points(karma.karmaID)
    #updaing ranks
    calculate_ranks()


  return render_template('Student-Profile-forStaff.html',
                         student=student,
                         user=user,
                         karma=karma)

@staff_views.route('/view-all-badges-staff/<string:studentID>', methods=['GET'])
@login_required
def view_all_badges(studentID):
  student = get_student_by_id(studentID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllBadges.html',student=student,user=user)