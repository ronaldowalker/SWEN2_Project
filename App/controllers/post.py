from App.models import Post
from App.database import db 
from .staff import (
    get_staff_by_username
)
from .student import (
    get_student_by_username
)

def create_post(studentUsername, staffUsername, verified, details):
    student = get_student_by_username(studentUsername)
    staff = get_staff_by_username(staff)
    if student is None:
        print("[post.create_post] Error occurred while creating new post: No student found.")
        return False
    if staff is None:
        print("[post.create_post] Error occurred while creating new post: No staff found.")
        return False

    newPost = Post(student.ID, staff.ID, verified, details)
    db.session.add(newPost)

    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[post.create_post] Error occurred while creating new post: ", str(e))
        db.session.rollback()
        return False

def delete_post(postID):
    post = Post.query.filter_by(ID=postID).first()
    if post:
        db.session.delete(post)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[post.delete_post] Error occurred while deleting post: ", str(e))
            db.session.rollback()
            return False
    else:
        print("[post.delete_post] Error occurred while deleting post: Post not found.")
        return False

def get_posts_by_studentID(studentID):
    posts = Post.query.filter_by(createdByStudentID=studentID).all()
    if posts:
        return posts
    else:
        return []

        
