from App.models import User
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

def get_all_users():
    users = User.query.all()
    if users:
        return users
    else:
        return []

def get_all_users_json():
    users = User.query.all()
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
    