from App.database import db
from App.models import Review, Staff, Student

def create_review(staffID, studentID, isPositive, details): 
    staff = Staff.query.filter_by(staffID=staffID).first()
    student = Student.query.filter_by(studentID=studentID).first()

    if not staff:
        print(f"No staff found with ID {staffID}")
        return f"No staff found with ID {staffID}"
    
    if not student:
        print(f"No student found with ID {studentID}")
        return f"No student found with ID {studentID}"

    newReview = Review(
        StaffID=staff.ID,
        StudentID=student.ID,
        isPositive=isPositive,
        details=details
    )
    
    db.session.add(newReview)
    
    try:
        db.session.commit() 

       
        karma_change = 1 if isPositive else -1
        if isPositive:
            result = student.increase_karma(karma_change)  
        else:
            result = student.decrease_karma(karma_change)  
        
        db.session.commit()  # Commit the karma change

        print(f"\nKarma Update: {result}")
        return True
    
    except Exception as e:
        print(f"[review.create_review] Error occurred while creating new review or updating karma: {str(e)}")
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
          if capped_points <= 30 or capped_points >= -30:  
              review_count += 1
      if review_count == 0:  
          return 0

      return round(100 * total_points / review_count, 2) # multiplying by 100 to normalize to 100 points
  return 0

def get_review(id):
  review = Review.query.get(id)
  if review:
    return review
  else:
    return None
  
