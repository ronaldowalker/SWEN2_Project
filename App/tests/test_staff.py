import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff
from App.controllers import (
    create_staff,
    get_staff_by_id,
    get_staff_by_username,
    get_staff_by_name,
    get_staff_by_staffID,
)
'''
   Unit Tests
'''
class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        newStaff = Staff(staffID=12345,username="RenWalker",firstname="ren", lastname="walker", email="ren@example.com", password="renpass")
        assert newStaff.username == "RenWalker"

    def test_check_password(self):
        newStaff = Staff(staffID=12345,username="RenWalker",firstname="ren", lastname="walker", email="ren@example.com", password="renpass")
        assert newStaff.check_password(newStaff.password)

    def test_generate_password_hash(self):
        newStaff = Staff(staffID=12345,username="RenWalker",firstname="ren", lastname="walker", email="ren@example.com", password="renpass")
        assert newStaff.password != "renpass"

    def test_staff_to_json(self):
        newStaff = Staff(staffID=12345,username="RenWalker",firstname="ren", lastname="walker", email="ren@example.com", password="renpass")
        staff_json = newStaff.to_json()
        print(staff_json)
        self.assertDictEqual(staff_json, {"staffID": "12345",
            "username": "RenWalker",
            "firstname": "ren",
            "lastname": "walker",
            "email": "ren@example.com",
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

class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        assert create_staff(staffID=12345, username="RenWalker", firstname="ren", lastname="walker", email="ren@example.com",password="renpass") == True

    def test_get_staff_by_id(self):
        staff = get_staff_by_id(1)
        assert staff is not None

    def test_get_staff_by_username(self):
        staff = get_staff_by_username("RenWalker")
        assert staff is not None

    def test_get_staff_by_staffID(self):
        staff = get_staff_by_staffID(staffID = 12345)
        assert staff is not None

    def test_get_staff_by_name(self):
        staff = get_staff_by_name(firstname = "ren", lastname = "walker")
        assert staff is not None