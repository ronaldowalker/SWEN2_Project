import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Review
from App.controllers import (
    create_student,
    create_staff,
    get_staff_by_username,
    get_staff_by_id,
    get_student_by_id,
    get_student_by_username,
    create_review,
    delete_review,
    calculate_points_upvote,
    calculate_points_downvote,
    get_total_review_points,
    get_review
)
'''
   Unit Tests
'''
class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031160',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        review = Review(staff, student, True, 3, "Billy is good.", studentSeen=False)
        assert review is not None

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
        assert create_staff(username="joe",firstname="Joe", lastname="Mama", email="joe@example.com", password="joepass", faculty="FST") == True
        assert create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031160',
                 degree="",
                 gpa="") == True
        student = get_student_by_username("billy")
        staff = get_staff_by_username("joe")
        assert create_review(staff=staff, student=student, isPositive=True, points=3, details="Billy is good.") == True
        review = get_review(1)

    def test_get_review(self):
        self.test_create_review()
        review = get_review(1)
        print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
        assert review is not None

    def test_calc_points_upvote(self):
        self.test_create_review()
        review = get_review(1)
        print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
        assert review is not None
        assert calculate_points_upvote(review) == True

    def test_calc_points_downvote(self):
        self.test_create_review()
        review = get_review(1)
        print(review.to_json(student=get_student_by_id(review.studentID), staff=get_staff_by_id(review.createdByStaffID)))
        assert review is not None
        assert calculate_points_downvote(review) == True

    def test_get_total_points(self):
        self.test_create_review()
        review = get_review(1)
        assert get_total_review_points(review.studentID) != 0

    def test_delete_review(self):
        self.test_create_review()
        review = get_review(2)
        assert delete_review(review.ID) == True
