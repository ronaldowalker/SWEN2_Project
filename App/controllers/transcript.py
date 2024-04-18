from App.models.transcript import Transcript
from App.controllers.student import get_student_by_id, get_student_by_UniId
from App.database import db
import json


def create_transcript(transcript_data):
  try:
    UniId = transcript_data.get('id')
    gpa = transcript_data.get('gpa')
    fullname = transcript_data.get('fullname')
    courses = transcript_data.get('courses', {})
    in_progress_courses = transcript_data.get('inProgressCourses', {})

    #print('Transcript data:', transcript_data)

    # Function to split courses by semester
    def split_courses_by_semester(courses_dict):
      semesters = {}
      current_semester = None
      current_courses = {}
      for key, value in courses_dict.items():
        if 'Semester' in key:  # Assuming semester keys start with 'Semester' for years
          if current_semester:  # If there was a previous semester, store its courses
            semesters[current_semester] = current_courses
          current_semester = key
          current_courses = {}
        else:
          current_courses[key] = value
      if current_semester:  # Store the last semester's courses
        semesters[current_semester] = current_courses
      return semesters

    courses_by_semester = split_courses_by_semester(courses)
    in_progress_courses_by_semester = split_courses_by_semester(
        in_progress_courses)

    # Iterate through completed courses
    for semester, semester_courses in courses_by_semester.items():
      for course, grade in semester_courses.items():
        if grade:  # Check if grade is not empty
          print(
              f"Adding completed course for {semester}: {course} - Grade: {grade}"
          )
          #check if already exists
          transcript = Transcript.query.filter_by(UniId=UniId,
                                                  semester=semester,
                                                  course=course).first()
          if not transcript:
            new_transcript = Transcript(UniId=UniId,
                                        semester=semester,
                                        course=course,
                                        grade=grade,
                                        isInProgress=False)
            db.session.add(new_transcript)
            db.session.commit()  # Commit the changes to the database
          else:
            if grade != transcript.grade:
              transcript.grade = grade #overwriting the grade if null from last semester
              transcript.isInProgress = False #setting it to false as it is completed
              db.session.commit()  # Commit the changes to the database
            print(
                f"Course {course} for {semester} already exists in database! (from controller) "
            )

    # Iterate through in-progress courses
    for semester, in_progress_semester_courses in in_progress_courses_by_semester.items(
    ):
      for in_progress_course in in_progress_semester_courses.keys():
        print(
            f"Adding in-progress course for {semester}: {in_progress_course}")
        #check if already exists
        transcript = Transcript.query.filter_by(
            UniId=UniId, semester=semester, course=in_progress_course).first()
        if not transcript:
          new_transcript = Transcript(UniId=UniId,
                                      semester=semester,
                                      course=in_progress_course,
                                      grade='',
                                      isInProgress=True)
          db.session.add(new_transcript)
        else:
          print(
              f"Course {in_progress_course} for {semester} already exists in database! (from controller)"
          )

    db.session.commit()
    print("Transcript data stored succefully in database! (from controller)")
    return True
  except Exception as e:
    print(
        "[transcript.create_transcript] Error occurred while creating new transcript: ",
        str(e))
    db.session.rollback()
    return False


def calculate_academic_score(studentID):
  # student = get_student_by_UniId(studentID)
  student = get_student_by_id(studentID)

  # UniId = '816033730'
  if student:
    UniId = student.UniId
    total_As = get_total_As(UniId)
    total_courses_attempted = get_total_courses_attempted(UniId)
    total_grades_points= get_total__grade_points(UniId)

    if total_courses_attempted == 0:
      print("Error: No courses attempted for student with ID:", UniId)
      return 0

    aratio = total_As / total_courses_attempted
    gpa = student.gpa
    # print("A ratio:", round(float(aratio), 2), '\nGPA:', gpa)

    # Convert aratio and gpa to float if they are not already numeric
    if not isinstance(aratio, (int, float)):
      aratio = float(aratio)
    if not isinstance(gpa, (int, float)):
      gpa = float(gpa)

    gparatio = gpa / 4.3
    # print("GPA ratio:", round(float(gparatio), 2), '/ 1.0')
    # Calculate academic score
    academic_score = (aratio * 0.15) + (gparatio * 0.85)

    # Round the academic score to 5 decimal place
    academic_score = round(academic_score, 5)
    # print("Academic score total:", academic_score)
    # print("Academic score:", academic_score * 0.4, ' / 0.4 weight')
    return round(100 * academic_score, 2) # multiplying by 100 to normalize to 100 points
  else:
    print("Student not found with ID:")
    # print('Student with UniId:', UniId, 'not found')
    return 0


def get_total_As(UniId):
  transcripts = get_transcript(UniId)
  # get points from grade
  if transcripts:
    get_total_As = 0
    for transcript in transcripts:
      # Extract grade from transcript
      grade = transcript.grade
      # Check if grade starts with 'A'
      if grade and grade.startswith('A'):
        get_total_As += 1
    return get_total_As
  return 0

def get_total_Fs(UniId):
  transcripts = get_transcript(UniId)
  # get points from grade
  if transcripts:
    get_total_Fs = 0
    for transcript in transcripts:
      # Extract grade from transcript
      grade = transcript.grade
      # Check if grade starts with 'F'
      if grade and grade.startswith('F'):
        get_total_Fs += 1
    return get_total_Fs
  return 0


def get_total__grade_points(UniId):
  transcripts = get_transcript(UniId)
  # get points from grade
  if transcripts:
    totalpoints = 0.0
    for transcript in transcripts:
      # Extract grade from transcript
      grade = transcript.grade
      if grade:
        points = getGradePoints(grade)
        totalpoints += points
    return totalpoints
  return 0


def get_total_courses_attempted(UniId):
  transcripts = get_transcript(UniId)
  # get points from grade
  if transcripts:
    total_courses_attempted = 0
    for transcript in transcripts:
      # Extract grade from transcript
      grade = transcript.grade
      # Check if grade starts with 'A'
      if grade != '':
        total_courses_attempted += 1
    return total_courses_attempted
  return 0


#get points from grade
def getGradePoints(grade):
  if grade == "" or grade is None:
    return 0
  if grade == 'A+':
    return 4.3
  if grade == 'A':
    return 4
  if grade == 'A-':
    return 3.7
  if grade == 'B+':
    return 3.3
  if grade == 'B':
    return 3
  if grade == 'B-':
    return 2.7
  if grade == 'C+':
    return 2.3
  if grade == 'C':
    return 2
  
  return 0


def delete_transcript(UniId):
  transcript = Transcript.query.filter_by(UniId=UniId).first()

  if transcript:
    db.session.delete(transcript)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print(
          "[transcript.delete_transcript] Error occurred while deleting transcript: ",
          str(e))
      db.session.rollback()
      return False

  else:
    print(
        "[transcript.delete_transcript] Transcript not found for student with ID: ",
        UniId)
    return False


def get_transcript(UniId):
  transcripts = Transcript.query.filter_by(UniId=UniId).all()
  if transcripts:
    return transcripts
  else:
    return None
