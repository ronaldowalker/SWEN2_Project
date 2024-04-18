from App.models import Badges, IncidentReport, Accomplishment, Recommendation, Review, Transcript
from App.controllers.student import get_student_by_id, get_student_by_UniId
from App.controllers.transcript import get_total_As, get_total_Fs
from App.controllers.accomplishment import get_verified_accomplishments_count
from App.database import db


def create_badge(student, name, details, imageLink, studentSeen):

  badge = Badges(student, name, details, imageLink, studentSeen)
  db.session.add(badge)

  try:
    db.session.commit()
    return True
  except Exception as e:
    print("[badge] Error occurred while creating new badge: ", str(e))
    db.session.rollback()
    return False


def sortBadges(student):

  totalAsBadge(student)
  noIncidentsBadge(student)
  threePlusAchi(student)
  verifRecc(student)
  neverFail(student)
  checkGPA(student)
  checkReviews(student)


def checkReviews(student):

  gpa = student.gpa

  reviews = Review.query.filter_by(studentID=student.ID).all()

  for review in reviews:
    if 10 <= review.points <= 15:
      name = "Review Rockstar"
      studentID = student.ID
      details = "Awarded to students who receive positive reviews resulting in between 10 and 15 points. This badge celebrates their ability to positively impact their peers and contribute to a supportive academic environment."

      badge1 = Badges.query.filter_by(name=name, studentID=studentID).first()

      if badge1:
        return "Already assigned"
      else:
        new_badge = Badges(
            student=student,
            name=name,
            details=details,
            imageLink=
            "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/10-15%20points.png?raw=true",
            studentSeen=False)
        db.session.add(new_badge)
        db.session.commit()
        return "Badge assigned"

    if 15 < review.points <= 20:
      name = "Feedback Phenom"
      studentID = student.ID
      details = "Awarded to students who receive positive reviews resulting in between 15 and 20 points. This badge recognizes their outstanding contributions and dedication to excellence in their academic endeavors."

      badge2 = Badges.query.filter_by(name=name, studentID=studentID).first()

      if badge2:
        return "Already assigned"
      else:
        new_badge = Badges(
            student=student,
            name=name,
            details=details,
            imageLink=
            "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/16-20%20points.png?raw=true",
            studentSeen=False)
        db.session.add(new_badge)
        db.session.commit()
        return "Badge assigned"

    if review.points > 20:
      name = "Review Royalty"
      studentID = student.ID
      details = "Awarded to students who receive positive reviews resulting in more than 20 points. This badge signifies their exemplary leadership, dedication, and positive influence within the academic community."

      badge3 = Badges.query.filter_by(name=name, studentID=studentID).first()

      if badge3:
        return "Already assigned"
      else:
        new_badge = Badges(
            student=student,
            name=name,
            details=details,
            imageLink=
            "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/20+%20points.png?raw=true",
            studentSeen=False)
        db.session.add(new_badge)
        db.session.commit()
        return "Badge assigned"

  return "Not fitting criteria"


def checkGPA(student):

  if student.gpa:
    gpa = float(student.gpa)

    if gpa:
      if 3.0 <= gpa <= 3.3:
        name = "GPA Guru"
        studentID = student.ID
        details = "Awarded to students who maintain a GPA between 3.0 and 3.3. This badge recognizes their consistent academic performance and dedication to their studies."

        badge1 = Badges.query.filter_by(name=name, studentID=studentID).first()

        if badge1:
          return "Already assigned"
        else:
          new_badge = Badges(
              student=student,
              name=name,
              details=details,
              imageLink=
              "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/3.0-3.3.png?raw=true",
              studentSeen=False)
          db.session.add(new_badge)
          db.session.commit()
          return "Badge assigned"

      if 3.3 < gpa <= 3.6:
        name = "Scholar Star"
        studentID = student.ID
        details = "Awarded to students who achieve a GPA between 3.3 and 3.6. This badge celebrates their exceptional academic performance and commitment to excellence."

        badge2 = Badges.query.filter_by(name=name, studentID=studentID).first()

        if badge2:
          return "Already assigned"
        else:
          new_badge = Badges(
              student=student,
              name=name,
              details=details,
              imageLink=
              "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/3.3-3.6.png?raw=true",
              studentSeen=False)
          db.session.add(new_badge)
          db.session.commit()
          return "Badge assigned"

      if 3.6 < gpa <= 4.0:
        name = "Academic Ace"
        studentID = student.ID
        details = "Awarded to students who maintain a GPA of 3.6- 4.0. This badge honors their outstanding academic achievements and exemplary dedication to their studies."

        badge3 = Badges.query.filter_by(name=name, studentID=studentID).first()

        if badge3:
          return "Already assigned"
        else:
          new_badge = Badges(
              student=student,
              name=name,
              details=details,
              imageLink=
              "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/3.6-4.0.png?raw=true",
              studentSeen=False)
          db.session.add(new_badge)
          db.session.commit()
          return "Badge assigned"

      if gpa > 4.0:
        name = "Cloud 4.3"
        studentID = student.ID
        details = "Awarded to students who achieve a GPA between 4.0 and 4.3. This prestigious badge celebrates their exceptional academic prowess, demonstrating mastery across all subjects and dedication to academic excellence. These students are true Grade Geniuses, setting a high standard for academic achievement and inspiring their peers to strive for excellence."

        badge4 = Badges.query.filter_by(name=name, studentID=studentID).first()

        if badge4:
          return "Already assigned"
        else:
          new_badge = Badges(
              student=student,
              name=name,
              details=details,
              imageLink=
              "https://github.com/RichardR963/Info3604_Project/blob/main/images/fixes/4.0-4.3.png?raw=true",
              studentSeen=False)
          db.session.add(new_badge)
          db.session.commit()
          return "Badge assigned"

  return "Not fitting criteria"


def neverFail(student):
  name = "Flawless Finisher"
  studentID = student.ID
  details = "Awarded to students who demonstrate consistent academic excellence by never failing a course throughout their academic career. This badge highlights their resilience, determination and commitment to success in their studies."

  existing_badge = Badges.query.filter_by(name=name,
                                          studentID=studentID).first()

  checkStudent = Transcript.query.filter_by(UniId=student.UniId).first()

  if checkStudent:
    count = get_total_Fs(student.UniId)

    if count > 0:

      if existing_badge:
        db.session.delete(existing_badge)
        db.session.commit()

      return "Not fitting criteria"
    else:
      if existing_badge:
        return "Already assigned"
      else:
        new_badge = Badges(
            student=student,
            name=name,
            details=details,
            imageLink=
            "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/never%20failing%20a%20course.png?raw=true",
            studentSeen=False)
        db.session.add(new_badge)
        db.session.commit()
        return "Badge assigned"

  return "Not meeting criteria"


def verifRecc(student):
  name = "Recommendation Royalty"
  studentID = student.ID
  details = "Awarded to students whose recommendations are verified and endorsed by trusted sources within the university community. This badge signifies their outstanding character, reliability and positive impact on others."

  recc = Recommendation.query.filter_by(createdByStudentID=student.UniId,
                                        approved=True).all()

  if recc:
    existing_badge = Badges.query.filter_by(name=name,
                                            studentID=studentID).first()
    if existing_badge:
      return "Badge already exists"
    else:
      new_badge = Badges(
          student=student,
          name=name,
          details=details,
          imageLink=
          "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/verified%20recommendation.png?raw=true",
          studentSeen=False)
      db.session.add(new_badge)
      db.session.commit()
      return "Badge assigned"


def threePlusAchi(student):
  name = "Achievement Ace"
  studentID = student.ID
  details = "Awarded to students who excel in extracurricular activities and accomplishments, earning three or more significant achievements. This badge acknowledges their versatility, leadership and commitment beyond the classroom."

  numAcs = get_verified_accomplishments_count(student.ID)

  if numAcs >= 3:
    existing_badge = Badges.query.filter_by(name=name,
                                            studentID=studentID).first()
    if existing_badge:
      return "Badge already exists"
    else:
      new_badge = Badges(
          student=student,
          name=name,
          details=details,
          imageLink=
          "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/3%20or%20more%20accomplishments.png?raw=true",
          studentSeen=False)
      db.session.add(new_badge)
      db.session.commit()
      return "Badge assigned"


def noIncidentsBadge(student):
  name = "Smooth Sailing"
  studentID = student.ID
  details = "Awarded to students who maintain a commendable record of conduct without any incidents. This badge celebrates their ability to navigate their academic journey smoothly, contributing positively to the university community."

  existing_badge = Badges.query.filter_by(name=name,
                                          studentID=studentID).first()

  incidents = IncidentReport.query.filter_by(studentID=studentID).all()

  if incidents:

    if existing_badge:
      db.session.delete(existing_badge)
      db.session.commit()

    return "Not fitting criteria"
  else:
    if existing_badge:
      return "Already assigned"
    else:
      new_badge = Badges(
          student=student,
          name=name,
          details=details,
          imageLink=
          "https://github.com/RichardR963/Info3604_Project/blob/main/images/badges/no%20incidents.png?raw=true",
          studentSeen=False)
      db.session.add(new_badge)
      db.session.commit()
      return "Badge assigned"


def totalAsBadge(student):

  name = "A's Acquirer"
  studentID = student.ID
  details = "This badge is allocated to students who have acuumulated a certain level of A's in their transcripts"

  numAs = get_total_As(student.UniId)

  if numAs >= 3:
    existing_badge = Badges.query.filter_by(name=name,
                                            studentID=studentID).first()
    if existing_badge:
      return "Badge already exists"
    else:
      new_badge = Badges(
          student=student,
          name=name,
          details=details,
          imageLink=
          "https://github.com/RichardR963/Info3604_Project/blob/main/images/GPA.png?raw=true",
          studentSeen=False)
      db.session.add(new_badge)
      db.session.commit()
      return "Badge assigned"
