from App.models import Review
from App.database import db


def create_review(staff, student, isPositive, points, details):
  newReview = Review(staff=staff,
                     student=student,
                     isPositive=isPositive,
                     points=points,
                     details=details,
                     studentSeen=False)
  db.session.add(newReview)
  try:
    db.session.commit()
    return True
  except Exception as e:
    print("[review.create_review] Error occurred while creating new review: ",
          str(e))
    db.session.rollback()
    return False


def delete_review(reviewID):
  review = Review.query.filter_by(ID=reviewID).first()
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


def calculate_points_upvote(review):
  review.points *= 1.1  # multiplier can be changed accordingly

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[review.calculate_points_upvote] Error occurred while updating review points:",
        str(e))
    db.session.rollback()
    return False


def calculate_points_downvote(review):
  review.points *= 0.9

  try:
    db.session.commit()
    return True
  except Exception as e:
    print(
        "[review.calculate_points_downvote] Error occurred while updating review points:",
        str(e))
    db.session.rollback()
    return False


# def get_total_review_points(studentID):
#   reviews = Review.query.filter_by(studentID=studentID).all()
#   if reviews:
#     sum = 0
#     for review in reviews:
#       sum += review.points
#     return sum
#   return 0
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
  review = Review.query.filter_by(ID=id).first()
  if review:
    return review
  else:
    return None
