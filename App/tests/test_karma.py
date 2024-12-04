import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Karma
from App.controllers import (
    to_json
)

'''
   Unit Tests
'''
class KarmaUnitTests(unittest.TestCase):

    def test_new_karma(self):
        assert create_student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0) == True
        student = get_student_by_studnetID(816036000)
        history = Karma(studentID = student.ID, action = "increase", amount = 1, previous_karma = 0, updated_karma = 1)
        assert history is not None
        

    def test_karma_to_json(self):
        assert create_student(studentID=816036000, firstname = "sly", lastname="cooper", karma=0) == True
        student = get_student_by_studnetID(816036000)
        history = Karma(studentID = student.ID, action = "increase", amount = 1, previous_karma = 0, updated_karma = 1)
        history_json = history.to_json()
        self.assertDictEqual(history_json,{
            "id": 1,
            "student_id": f"{student.ID}",
            "action": "increase", 
            "amount": "1", 
            "previous_karma": "0",
            "updated_karma": "1",
            "timestamp": -f"{history.timestamp}",
        })

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

class KarmaIntegrationTests(unittest.TestCase):
