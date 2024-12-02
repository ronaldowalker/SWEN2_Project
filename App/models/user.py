from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Specify the table name explicitly
    ID = db.Column(db.Integer, primary_key=True)  # Primary Key
    userID = db.Column(db.Integer, nullable=True, unique=True)  
    username = db.Column(db.String(120), nullable=False, unique=True)  # Unique username
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)  # Unique email
    type = db.Column(db.String(50))  # For polymorphism

    # Polymorphism settings
    __mapper_args__ = {
        "polymorphic_identity": "user",  # Default type for User
        "polymorphic_on": type           # Use the 'type' column to differentiate subclasses
    }

    def __init__(self, userID, username, firstname, lastname, email, password):
        self.userID = userID
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)

    def get_json(self):
        """Returns a JSON representation of the User object."""
        return {
            'id': self.ID,
            'userID': self.userID,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
        }

    def get_id(self):
        """Returns the unique ID of the User."""
        return self.ID

    def get_userid(self):
        """Returns the external userID."""
        return self.userID

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Checks a given password against the stored hash."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.ID}: {self.username}>'
