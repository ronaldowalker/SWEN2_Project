from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user

from App.models import Student, Staff, User, IncidentReport
from App.controllers import (
    jwt_authenticate, login, create_incident_report, get_student_by_UniId,
    get_accomplishment, get_student_by_id, get_recommendations_staff,
    get_recommendation, get_student_by_name, get_students_by_faculty,
    get_staff_by_id, get_requested_accomplishments,
    get_student_ids_by_tagged_staff_id, get_students_by_ids, get_transcript,
    get_total_As, get_student_for_ir, create_review, get_karma)

staff_views = Blueprint('staff_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''


@staff_views.route('/staffhome', methods=['GET'])
def get_staffHome_page():
  return render_template('Staff-Home.html')


@staff_views.route('/incidentReport', methods=['GET'])
def staff_ir_page():
  return render_template('IncidentReport.html')


@staff_views.route('/studentSearch', methods=['GET'])
def student_search_page():
  return render_template('StudentSearch.html')


@staff_views.route('/reviewSearch', methods=['GET'])
def review_search_page():
  return render_template('ReviewSearch.html')


@staff_views.route('/mainReviewPage', methods=['GET'])
def mainReviewPage():
  return render_template('P-N-Review.html')


@staff_views.route('/positiveReviewPage', methods=['GET'])
def positiveReviewPage():
  return render_template('preview.html')


@staff_views.route('/negativeReviewPage', methods=['GET'])
def negativeReviewPage():
  return render_template('nreview.html')


@staff_views.route('/createPositiveReview', methods=['POST'])
def createPositiveReview():
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)

  data = request.form
  studentID = data['studentID']
  studentName = data['name']
  points = data['points']
  details = data['details']
  firstname, lastname = studentName.split(' ')
  student = get_student_by_UniId(studentID)

  if student:
    review = create_review(staff, student, True, points, details)
    message = f"You have created a positive review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)
  else:
    message = f"{studentName} not found"
    return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/createNegativeReview', methods=['POST'])
def createNegativeReview():
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)

  data = request.form
  studentID = data['studentID']
  studentName = data['name']
  points = data['points']
  details = data['details']
  firstname, lastname = studentName.split(' ')
  student = get_student_by_UniId(studentID)

  if student:
    review = create_review(staff, student, False, points, details)
    message = f"You have created a negative review on Student: {studentName}"
    return render_template('Stafflandingpage.html', message=message)
  else:
    return "Student not found", 404


@staff_views.route('/newIncidentReport', methods=['POST'])
@login_required
def newIncidentReport():
  data = request.form
  staff_id = current_user.get_id()

  student_id = data['studentID']
  student_name = data['name']
  firstname, lastname = student_name.split(' ')
  student = get_student_for_ir(firstname, lastname, student_id)

  topic = data['topic']
  details = data['details']
  points = data['points-dropdown']

  incidentReport = create_incident_report(student_id, staff_id, details, topic,
                                          points)
  message = f"You have created an incident report on the student {student_name} with a topic of {topic} !"

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
    firstname, lastname = name.split(' ')
    # Filtering by firstname and lastname if they are provided
    query = query.filter_by(firstname=firstname, lastname=lastname)

  if studentID:
    student = get_student_by_id(studentID)
    if student:
      # Render student profile immediately
      return jsonify(student.serialize())
    else:
      return "Student not found", 404

  if faculty:
    query = query.filter_by(faculty=faculty)

  if degree:
    query = query.filter_by(degree=degree)

  students = query.all()

  if students:
    return render_template('ssresult.html', students=students)
  else:
    return "No matching records", 404


# @staff_views.route('/review_search/<string:reviewID>', methods=['GET'])
# @login_required
# def reviewSearch(reviewID):

#     if not isinstance(current_user, Staff):
#         return "Unauthorized", 401

#     studentName = request.form.get('student_name')
#     #TOPICS
#     leadership = request.form.get('leadership')
#     respect = request.form.get('respect')
#     punctuality = request.form.get('punctuality')
#     participation = request.form.get('participation')
#     teamwork = request.form.get('teamwork')
#     interpersonal = request.form.get('interpersonal')
#     respect_authority = request.form.get('respect_authority')
#     attendance = request.form.get('attendance')
#     disruption = request.form.get('disruption')

#     # Initialize query with Review model
#     query = Review.query

#     if studentName:
#         query = query.filter_by(studentName=studentName)

#     # Retrieve matching reviews
#     reviews = query.all()

#     if reviews:
#         # Serialize reviews and return as JSON response
#         serialized_reviews = [review.to_json() for review in reviews]
#         return jsonify(serialized_reviews)
#     else:
#         return "No matching records", 404


@staff_views.route('/allAchievementApproval', methods=['GET'])
@login_required
def allAchievementApproval():

  staff_id = current_user.get_id()
  accomplishments = get_requested_accomplishments(staff_id)
  return render_template('ProposedAchivements.html',
                         accomplishments=accomplishments)


@staff_views.route('/approveAchievement/<int:accomplishmentID>',
                   methods=['GET'])
@login_required
def approveAchievement(accomplishmentID):
  accomplishment = get_accomplishment(accomplishmentID)
  student = get_student_by_id(accomplishment.createdByStudentID)

  return render_template('FullReview.html',
                         accomplishment=accomplishment,
                         student=student)


@staff_views.route('/acceptAccomplishment/<int:accomplishmentID>',
                   methods=['POST'])
@login_required
def acceptAccomplishment(accomplishmentID):
  selected_points = int(request.form.get('points'))

  accomplishment = get_accomplishment(accomplishmentID)

  accomplishment.points = selected_points
  accomplishment.verified = True
  accomplishment.status = "Achievement Verified"
  db.session.add(accomplishment)
  db.session.commit()

  message = "You have verified this accomplishment !!"

  return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/declineAccomplishment/<int:accomplishmentID>',
                   methods=['POST'])
@login_required
def declineAccomplishment(accomplishmentID):

  accomplishment = get_accomplishment(accomplishmentID)

  accomplishment.verified = True
  accomplishment.status = "Achievement Declined"
  db.session.add(accomplishment)
  db.session.commit()

  message = "You have declined this accomplishment !!"

  return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/getStudentProfile/<string:uniID>', methods=['GET'])
@login_required
def getStudentProfile(uniID):
  student = get_student_by_UniId(uniID)
  user = User.query.filter_by(ID=student.ID).first()
  karma = get_karma(student.ID)
  transcripts = get_transcript(uniID)
  numAs = get_total_As(uniID)

  return render_template('Student-Profile-forStaff.html',
                         student=student,
                         user=user,
                         transcripts=transcripts,
                         numAs=numAs,
                         karma=karma)


@staff_views.route('/allRecommendationRequests', methods=['GET'])
@login_required
def allRecommendationRequests():
  staffID = current_user.get_id()
  print(staffID)
  recommendations = get_recommendations_staff(staffID)

  return render_template('RecommendationRequests.html',
                         recommendations=recommendations)


@staff_views.route('/declineRR/<int:rrID>', methods=['POST'])
@login_required
def declineRR(rrID):

  recommendation = get_recommendation(rrID)

  recommendation.approved = True
  recommendation.status = "Recommendation Declined"
  db.session.add(recommendation)
  db.session.commit()

  message = "You have declined this recommendation !!"

  return render_template('Stafflandingpage.html', message=message)


@staff_views.route('/acceptRR/<int:rrID>', methods=['POST'])
@login_required
def acceptRR(rrID):
  recommendation = get_recommendation(rrID)

  recommendation.approved = True
  recommendation.status = "Recommendation Accepted"
  db.session.add(recommendation)
  db.session.commit()

  message = "You have accepted this recommendation !!"
  return render_template('RecommendationLetter.html')
