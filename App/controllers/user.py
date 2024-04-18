from App.models import User, Student
from App.database import db

def create_user(username, firstname, lastname, password, email, faculty):
    newuser = User(username=username, firstname=firstname ,lastname=lastname, password=password, email=email, faculty=faculty)
    db.session.add(newuser)
    try:
        db.session.commit()
        return newuser
    except Exception as e:
        print("[user.create_user] Error occurred while creating new user: ", str(e))
        db.session.rollback()
        return None
    

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    else:
        return None

def get_user(id):
    user = User.query.get(id)
    if user:
        return user
    else:
        return None

def get_user_student(student):
  user = User.query.get(student.ID)
  if user:
      return user
  else:
      return None

def get_all_users():
    users = User.query.all()
    if users:
        return users
    else:
        return []

def get_all_users_json():
    users = User.query.all()
    # users = Student.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user_username(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_user_username] Error occurred while creating new user: ", str(e))
            db.session.rollback()
            return False
    return False

def update_username(userID, newUsername):
    user = get_user(userID)
    if user:
        user.username = newUsername
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_username] Error occurred while updating user username:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_username] Error occurred while updating user username: User "+userID+" not found")
        return False

def update_name(userID, newFirstname, newLastName):
    user = get_user(userID)
    if user:
        user.firstname = newFirstname
        user.lastname = newLastName
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_name] Error occurred while updating user name:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_name] Error occurred while updating user name: User "+userID+" not found")
        return False

def update_email(userID, newEmail):
    user = get_user(userID)
    if user:
        user.email = newEmail
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_email] Error occurred while updating user email:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_email] Error occurred while updating user email: User "+userID+" not found")
        return False

def update_password(userID, newPassword):
    user = get_user(userID)
    if user:
        user.set_password(newPassword)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_password] Error occurred while updating user password:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_password] Error occurred while updating user password: User "+userID+" not found")
        return False

def update_faculty(userID, newFaculty):
    user = get_user(userID)
    if user:
        user.faculty = newFaculty
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[user.update_faculty] Error occurred while updating user faculty:", str(e))
            db.session.rollback()
            return False
    else:
        print("[user.update_faculty] Error occurred while updating student faculty: User "+userID+" not found")
        return False