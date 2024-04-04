from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import (create_user, create_student, create_staff,
                             create_admin)
from flask_login import login_required, login_user, current_user, logout_user

index_views = Blueprint('index_views',
                        __name__,
                        template_folder='../templates')


@index_views.route('/', methods=['GET'])
def index_page():
  return render_template('login.html')


@index_views.route('/admin', methods=['GET'])
@login_required
def admin_page():
  return render_template('index.html')


@index_views.route('/init', methods=['GET'])
def init():
  db.drop_all()
  db.create_all()
  # create_user('bob', 'bobpass')
  create_student(username="billy",
                 firstname="",
                 lastname="",
                 email="billy@example.com",
                 password="billypass",
                 faculty="",
                 admittedTerm="",
                 UniId='billy@example.com',
                 degree="",
                 gpa="")
  #Creating staff
  create_staff(username="staff",
               firstname="",
               lastname="",
               email="",
               password="staffpass",
               faculty="")
  print('database intialized')

  create_admin(username="admin",
               firstname="Sanjeev",
               lastname="Praboo",
               email="andy@example.com",
               password="password",
               faculty="FST")

  return jsonify(message='db initialized!')


@index_views.route('/health', methods=['GET'])
def health_check():
  return jsonify({'status': 'healthy'})


@index_views.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory('/workspaces/Info3604_Project/images', filename)
