import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Student
from App.controllers import (
    create_student,
    get_student_by_id,
    get_student_by_studentID,
    get_student_by_name,
    get_full_name_by_student_id,
    get_all_students_json,
    update_student_karma,
    undo_last_karma_change,
    view_student_karma_history
)

'''
   Unit Tests
'''
class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0)
        assert student.firstname == "sly"

    def test_full_name(self):
        student = Student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0)
        assert student.full_name == f"{firstName} {lastName}"

    def test_student_to_json(self):
        student = Student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0)
        student_json = student.to_json()
        print(student_json)
        self.assertDictEqual(student_json, {"studentID": "816036000",
                                            "firstname": "sly",
                                            "lastname": "cooper",
                                            "karma": "0",
                                            "reviews": []})


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

class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        assert create_student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0) == True
        
    def test_get_student_by_id(self):
        student = get_student_by_id(1)
        assert student is not None
    
    def test_get_student_by_name(self):
        student = get_student_by_name(firstname="sly", lastname="cooper")
        assert student is not None

    def test_get_student_by_studnetID(self):
        student = get_student_by_studentID(studentID=816036000)
        assert student is not None

    def test_get_full_name_by_student_id(self):
        student = get_full_name_by_student_id(ID=1)
        assert student is not None

    
    def test_get_all_students_json(self):
        students = get_all_students_json()
        assert students != []

    def test_update_student_karma(self):
        student = update_student_karma(studentID=816036000, is_positive=True)
        assert student is not None

    def test_undo_last_karma_change(self):
        student = undo_last_karma_change(studentID=816036000)
        assert student is not None

    def test_view_student_karma_history(self):
        students = view_student_karma_history(studentID=816036000)
        assert students != []