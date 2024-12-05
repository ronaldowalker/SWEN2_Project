import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Review
from App.controllers import get_student_by_studentID
from App.controllers import (
    create_student,
    create_staff,
    create_review,
    get_student_by_studentID,
    get_staff_by_staffID,

    delete_review,
    get_review,
)
'''
   Unit Tests
'''
class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        assert create_staff(staffID=12345,username="RenWalker",firstname="ren", lastname="walker", email="ren@example.com", password="renpass") == True
        assert create_student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0) == True
        student = get_student_by_studnetID(816036000)
        staff = get_staff_by_staffID(12345)
        review = Review(staff.staffID, student.studentID, True, "Good Student")
        assert review is not None

    def test_review_to_json(self):
        assert create_staff(staffID=12345,username="RenWalker",firstname="ren", lastname="walker", email="ren@example.com", password="renpass") == True
        assert create_student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0) == True
        student = get_student_by_studnetID(816036000)
        staff = get_staff_by_staffID(12345)
        review = Review(staff.staffID, student.studentID, True, "Good Student")
        review_json = review.to_json()
        self.assertDictEqual(review_json, {"reviewID": "1",
                                            "reviewer": "ren walker",
                                            "studentID": "816036000",
                                            "studentName": "sly cooper",
                                            "created": f"{review.dateCreated}",
                                            "isPositive": "True",
                                            "reviews": "Good Student"})

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class ReviewIntegrationTests(unittest.TestCase):

    def test_create_review(self):
        assert create_staff(staffID=12345,username="RenWalker",firstname="ren", lastname="walker", email="ren@example.com", password="renpass") == True
        assert create_student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0) == True
        student = get_student_by_studnetID(816036000)
        staff = get_staff_by_staffID(12345)
        assert create_review(staffID = staff.staffID, studentID=student.studentID, isPositive=True, details="Good Student") == True
        review = get_review(1)

    # def test_get_review(self):
    #     self.test_create_review()
    #     review = get_review(1)
    #     print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
    #     assert review is not None

    # def test_delete_review(self):
    #     self.test_create_review()
    #     review = get_review(2)
    #     assert delete_review(review.ID) == True
