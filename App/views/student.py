from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from .index import index_views
from App.models import Staff, Student, User
from App.controllers import (
    create_user, jwt_authenticate, login, get_transcript, get_student_by_UniId,
    create_recommendation, create_accomplishment, get_all_students_json,
    get_total_As, get_karma, calculate_academic_points,
    calculate_accomplishment_points, get_staff_by_name, calculate_ranks,
    calculate_review_points, create_job_recommendation,
    create_school_recommendation, update_total_points)

student_views = Blueprint('student_views',
                          __name__,
                          template_folder='../templates')
'''
Page/Action Routes
'''


@student_views.route('/Student-Home', methods=['GET'])
@login_required
def home_page():
  login_required(home_page)
  return render_template('Student-Home.html')


@student_views.route('/student_dashboard', methods=['GET'])
@login_required
def student_dashboard_page():
  return render_template('StudentPage.html')


@student_views.route('/student-page', methods=['GET'])
@login_required
def student_page():
  #getting student info from controller
  #using flasklogin to get the current user
  student = Student.query.filter_by(ID=current_user.ID).first()
  user = User.query.filter_by(ID=current_user.ID).first()
  karma = get_karma(student.ID)
  if karma:

    calculate_academic_points(student.ID)
    calculate_accomplishment_points(student.ID)
    calculate_review_points(student.ID)
    print("review points:" + str(karma.reviewsPoints))
    #Points: academic (0.4),accomplishment (0,3 shared)
    #missing points: incident , reivew
    #calculate the accomplishment - incident for 0.3 shared
    #assign review based on 1 time reivew max 5pts for 0.3
    update_total_points(karma.karmaID)
    print('total karma points', karma.points)
    #updaing ranks
    calculate_ranks()
    print(karma.to_json())
  #studentjson = student.to_json(karma)
  #print(studentjson)

  transcripts = get_transcript(current_user.UniId)
  numAs = get_total_As(current_user.UniId)
  if student:
    print("Student found - from view")
    # print(student)
    # print(student.get_json())
    return render_template('StudentPage.html',
                           student=student,
                           user=user,
                           transcripts=transcripts,
                           numAs=numAs,
                           karma=karma)
  else:
    return render_template('Student-Home.html')


@student_views.route('/upload-transcript', methods=['GET'])
@login_required
def student_profile():
  return render_template('uploadtranscript.html')


@student_views.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory('/workspaces/Info3604_Project/images', filename)


#route for request recommendation
@student_views.route('/request-recommendation-form', methods=['GET'])
@login_required
def recommendation():
  return render_template('request recommendation.html')


#route for viewing reviews
@student_views.route('/view-reviews', methods=['GET'])
@login_required
def view_reviews():
  return render_template('Student-Home.html')


#route for viewing achievements
@student_views.route('/view-achievements', methods=['GET'])
@login_required
def view_achievements():
  return render_template('view-achievements.html')


#route for viewing Incidents
@student_views.route('/view-incidents', methods=['GET'])
@login_required
def view_incidents():
  return render_template('View-incidents.html')


@student_views.route('/propose-achievement', methods=['GET'])
@login_required
def propose_achievement():
  return render_template('StudentProposeAchievement.html')


@student_views.route('/request-recommendation', methods=['POST'])
@login_required
def request_recommendation():
  # Extract data from the request
  student_id = current_user.get_id()
  teacherName = request.form.get('teacherName')
  firstname, lastname = teacherName.split(' ')
  staff = get_staff_by_name(firstname, lastname)
  cyos = request.form.get('cyos')
  approved = False

  recommendation_type = request.form.get('recommendationType')

  if recommendation_type == 'Job':
    company_name = request.form.get('companyName')
    position = request.form.get('position')
    company_email = request.form.get('companyEmail')
    details = request.form.get('jobdetails')
    status = "Job"
    # Handle job recommendation
    newrec = create_job_recommendation(student_id, staff.ID, approved, status,
                                       cyos, details, company_name, position,
                                       company_email)
    message = f"You have submitted a recommendation request to {teacherName}!!"

    return render_template('landingpage.html', message=message)
  elif recommendation_type == 'School':
    school_name = request.form.get('schoolName')
    program = request.form.get('program')
    school_email = request.form.get('schoolEmail')
    details = request.form.get('schooldetails')
    status = "School"
    # Handle job recommendation
    newrec = create_school_recommendation(student_id, staff.ID, approved,
                                          status, cyos, details, school_name,
                                          program, school_email)
    message = f"You have submitted a recommendation request to {teacherName} {details}!!"

    return render_template('landingpage.html', message=message)


@student_views.route('/api/propose-achievement', methods=['POST'])
@login_required
def propose_achievement_post():
  if request.method == 'POST':
    # Extract data from the request
    topic = request.form.get('topic')
    taggedStaffName = request.form.get(
        'taggedStaffName'
    )  #todo get id from name  displayed in list in front end
    details = request.form.get('details')
    student_id = current_user.ID
    print(student_id)
    print(topic)
    print(taggedStaffName)
    status = "None yet"

    # Check if any required field is missing
    if not all([student_id, taggedStaffName, details]):
      return jsonify({'message': 'All fields are required.'}), 400

    # Call the controller function
    try:
      response = create_accomplishment(student_id, False, taggedStaffName,
                                       topic, details, 0, status)
      message = f"You have submitted an achievement to be verified by {taggedStaffName} !!"

      return render_template('landingpage.html', message=message)
    except Exception as e:
      return jsonify({'message': str(e)}), 500
  else:
    return jsonify({'message': 'Method not allowed'}), 405


# #leaderboard route
# @student_views.route('/leaderboard', methods=['GET'])
# @login_required
# def leaderboard_api():
#   # Getting students' details from controller
#   students = get_all_students_json()
#   students = Student.query.all()
#   # Return the students' details in JSON format
#   calculate_ranks()
#   for stu in students:
#     print('tttt')
#     students_json = stu.to_json(get_karma(stu.ID))
#     print(students_json)


#   # Traverse students, invoke calculate ranking for all
#   # Order object based on ranking
#   return render_template(
#       'Leaderboard.html',
#       students_json=students_json,
#   )
#   #return jsonify({'students': students_data}), 200
#leaderboard route
@student_views.route('/leaderboard', methods=['GET'])
@login_required
def leaderboard_api():
  # Getting students' details from controller
  students = get_all_students_json()
  students = Student.query.all()





  #Recalculating points for each student and ranks
  for student in students:
    karma = get_karma(student.ID)
    if karma:
  
      calculate_academic_points(student.ID)
      calculate_accomplishment_points(student.ID)
      calculate_review_points(student.ID)
      print("review points:" + str(karma.reviewsPoints))
      #Points: academic (0.4),accomplishment (0,3 shared)
      #missing points: incident , reivew
      #calculate the accomplishment - incident for 0.3 shared
      #assign review based on 1 time reivew max 5pts for 0.3
      update_total_points(karma.karmaID)
      print('total karma points', karma.points)
      print(karma.to_json())







  

  
  students_json = []  # Initialize students_json list

  # Return the students' details in JSON format
  calculate_ranks()
  for stu in students:
    print('gathering students and their karma info using student json')
    student_info = stu.to_json(get_karma(stu.ID))
    students_json.append(
        student_info)  # Append each student's info to the students_json list
    print(students_json)

  # Traverse students, invoke calculate ranking for all
  # Order object based on ranking
  return render_template(
      'Leaderboard.html',
      students_json=students_json,
  )
  #return jsonify({'students': students_data}), 200


@student_views.route('/view-all-reviews', methods=['GET'])
@login_required
def view_all_reviews():
  student = get_student_by_UniId(current_user.UniId)
  # Return the students' details in JSON format
  return render_template('AllStudentReviews.html', student=student)
  #return jsonify({'students': students_data}), 200


@student_views.route('/view-all-incidents', methods=['GET'])
@login_required
def view_all_incidents():
  # Return the students' details in JSON format
  student = get_student_by_UniId(current_user.UniId)
  return render_template('AllStudentIncidents.html', student=student)
  #return jsonify({'students': students_data}), 200


@student_views.route('/view-all-achievements', methods=['GET'])
@login_required
def view_all_achievements():
  student = Student.query.filter_by(ID=current_user.ID).first()
  # Return the students' details in JSON format

  return render_template('AllStudentAchivements.html', student=student)
  #return jsonify({'students': students_data}), 200
