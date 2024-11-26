from App.models import Review, Staff, Student, IncreaseKarmaCommand, DecreaseKarmaCommand
from App.database import db


def create_review(staffID, studentID, isPositive, details):

  staff = Staff.query.get(staffID)
  student = Student.query.get(studentID)

  if not staff:
      return f"No staff found with ID {staff}"
  if not student:
      return f"No student found with ID {student}"

  newReview = Review(staff=staff,
                     student=student,
                     isPositive=isPositive,
                     details=details)
  db.session.add(newReview)
  try:
    db.session.commit()

    if isPositive:
        command = IncreaseKarmaCommand(student, 1)
    else:
        command = DecreaseKarmaCommand(student, 1)
    
    result = student.karma_history.execute_command(command)
    db.session.commit()

    print(f"Karma Update: {result}")
    return True
  except Exception as e:
    print("[review.create_review] Error occurred while creating new review or updating karma: ",
          str(e))
    db.session.rollback()
    return False


def delete_review(reviewID):
  review = Review.query.get(reviewID)
  if review:
    db.session.delete(review)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print("[review.delete_review] Error occurred while deleting review: ",
            str(e))
      db.session.rollback()
      return False
  else:
    return False

def get_total_review_points(studentID):
  reviews = Review.query.filter_by(studentID=studentID).all()
  if reviews:
      total_points = 0
      review_count = 0
      for review in reviews:
          
          capped_points = max(min(review.points, 30), -30)
          total_points += capped_points / 30
          if capped_points <= 30 or capped_points >= -30:  # Only count reviews after applying the threshold
              #print(" review.points:", review.points)
              review_count += 1
      if review_count == 0:  # Avoid division by zero
          return 0
      #print("Total Points:", total_points)
      #print("Review Count:", review_count)

      return round(100 * total_points / review_count, 2) # multiplying by 100 to normalize to 100 points
  return 0

def get_review(id):
  review = Review.query.get(id)
  if review:
    return review
  else:
    return None
  
