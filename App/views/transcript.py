from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
#from App.controllers.transcript import *
import os
from flask_login import login_required, login_user, current_user, logout_user
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
import requests

from App.controllers.transcript import create_transcript
from App.controllers.student import *

transcript_views = Blueprint('transcript_views', __name__)


@transcript_views.route('/upload_transcript', methods=['POST'])
def upload_transcript():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'})

  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'})

  if file and file.filename.endswith('.pdf'):

    filename = secure_filename(file.filename)
    file_path = os.path.join(
        'App', 'Transcript', filename
    )  # Assuming 'App/Transcript' is the path to save transcript files
    file.save(file_path)
    #print("saved transcript file!")

    # Call transcript parser service
    try:
      print('trying_to_parse_transcript')
      transcript_data = parse_transcript(
          file_path)  # Function to parse transcript using external service
      if transcript_data:
        # Assuming transcript_data is a dictionary containing parsed transcript data
        # Call controller function to create transcript
        #print("transcript data before attempting to use controller: ")
        #print(transcript_data)

        # Pass transcript_data dictionary as a single argument to create_transcript function
        success = (create_transcript(transcript_data))
        if success:
          print("transcript data stored in database from view!")
          successStudent = create_student_from_transcript(
              transcript_data, current_user)
          if successStudent:
            print("Student data stored in database!")
            return jsonify(
                {'message': 'Student data stored in database from view'})

          message = f"Transcript {filename} uploaded successfully!!"

          return render_template('landingpage.html', message=message)
        else:
          print("failed to store transcript data in database from view!")
          return jsonify({
              'error':
              'Failed to store transcript data in database from view'
          })
      else:
        print("transcript parsing failed from view!")
        return jsonify({'error': 'Transcript parsing failed from view'})
    except Exception as e:
      print("failed to create transcript from view")
      print(str(e))
      return jsonify({'error': 'Failed to parse transcript from view'})
  print("invalid file format!")
  return jsonify({'error': 'Invalid file format'})


# Function to parse transcript using external service
def parse_transcript(file_path):
  # API endpoint for transcript parser service
  parser_url = 'https://parser-service.onrender.com/parse'

  # Prepare file for uploading
  files = {'file': open(file_path, 'rb')}

  # Make POST request to transcript parser service
  response = requests.post(parser_url, files=files)

  # Check if request was successful and return parsed data
  if response.status_code == 200:
    parsed_data = response.json(
    )  # Assuming response contains parsed transcript data
    #print("parsed transcript data from API: ")
    #print(parsed_data)
    return parsed_data
  else:
    return None
