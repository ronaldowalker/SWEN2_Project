from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, get_jwt_identity
from App.database import db
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime

from App.models import Student, Staff, User, Review
from App.controllers import (
    jwt_authenticate,  get_student_by_id, get_staff_by_id,
    get_staff_by_id, create_review, get_karma,
    analyze_sentiment, calculate_ranks, update_total_points,
    calculate_academic_points, calculate_accomplishment_points,
    calculate_review_points,get_student_by_studentID)

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
    
    if student:
        # Concatenate firstName and lastName to form the fullname
        fullname = f"{student.firstName} {student.lastName}"
        return jsonify({'studentName': fullname})
    else:
        return jsonify({'error': 'Student not found'}), 404


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
    # Get staff_id from session
    staff_id = session.get('staff_id')
    if not staff_id:
        return jsonify({"msg": "Staff not logged in"}), 401

    # Get form data
    data = request.form
    studentID = data['studentID']
    studentName = data['name']
    is_positive = data['isPositive'] == 'True'  # This will be 'True' or 'False' as a string
    details = data['details']  # The review entered by the staff member
    
    # Validate student
    firstname, lastname = studentName.split(' ')
    student = get_student_by_studentID(studentID)

    # Determine the points based on positivity
    points = 1 if is_positive else -1

    # If student exists, create review and update karma
    if student:
        review = Review(
            taggedStudentID=studentID,  # Matches the column name in the model
            createdByStaffID=staff_id,  # Matches the column name in the model
            isPositive=is_positive,
            details=details   # Correct variable name
        )
        db.session.add(review)
        db.session.commit()

        # Update student's karma based on review positivity
        student.karma += points if is_positive else -points
        db.session.commit()

        # Success message and redirection
        message = f"You have created a review for Student: {studentName}"
        return render_template('Stafflandingpage.html', message=message)

    else:
        # Handle error if student doesn't exist
        message = f"Error creating review for Student: {studentName}"
        return render_template('Stafflandingpage.html', message=message)



@staff_views.route('/searchStudent', methods=['GET'])
def studentSearch():
    name = request.args.get('name')
    studentID = request.args.get('studentID')

    query = Student.query

    if name:
        # Split the name to check if it's a full name or partial
        name_parts = name.split()
        if len(name_parts) > 1:
            # If there are multiple parts, assume full name
            first_name, last_name = name_parts[0], name_parts[1]
            query = query.filter(
                db.and_(
                    Student.firstName.ilike(f'%{first_name}%'),
                    Student.lastName.ilike(f'%{last_name}%')
                )
            )
        else:
            # If only one part, search in first or last name
            query = query.filter(
                db.or_(
                    Student.firstName.ilike(f'%{name}%'),
                    Student.lastName.ilike(f'%{name}%')
                )
            )

    if studentID:
        query = query.filter_by(studentID=studentID)

    students = query.all()

    if students:
        return render_template('ssresult.html', students=students)
    else:
        message = "No students found"
        return render_template('StudentSearch.html', message=message)



@staff_views.route('/view-all-student-reviews/<string:uniID>', methods=['GET'])
@login_required
def view_all_student_reviews(uniID):

  student = get_student_by_id(uniID)
  user = User.query.filter_by(ID=current_user.ID).first()
  return render_template('AllStudentReviews.html', student=student,user=user)



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
