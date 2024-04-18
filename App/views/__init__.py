# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .csv import csv_views
from .student import student_views
from .staff import staff_views
from .transcript import transcript_views


views = [user_views, index_views, auth_views, csv_views, student_views, transcript_views,staff_views]

# blueprints must be added to this list
