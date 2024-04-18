from flask import Blueprint, jsonify, request, render_template
from werkzeug.utils import secure_filename
from App.controllers.csv import populate_db_from_csv
from App.controllers.staffcsv import populate_staff_from_csv
import os

csv_views = Blueprint('csv_views', __name__, template_folder='../templates')

UPLOAD_FOLDER = 'App/Csv'
ALLOWED_EXTENSIONS = {'csv'}

@csv_views.route('/getLanding', methods=['GET'])
def getLanding():
  message = request.args.get('message', '')

  return render_template('adminLanding.html', message=message)

@csv_views.route('/upload_csv2', methods=['POST'])
def upload_csv2():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'})

  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'})

  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)
    try:
      populate_staff_from_csv(file_path)
      return jsonify({'message': 'CSV file uploaded successfully'})
    except Exception as e:
      return jsonify({'error': str(e)})
  else:
    return jsonify({'error': 'Invalid file format'})


@csv_views.route('/upload_csv', methods=['POST'])
def upload_csv():
  if 'file' not in request.files:
    return jsonify({'error': 'No file part'})

  file = request.files['file']
  if file.filename == '':
    return jsonify({'error': 'No selected file'})

  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file.save(file_path)
    try:
      populate_db_from_csv(file_path)
      return jsonify({'message': 'CSV file uploaded successfully'})
    except Exception as e:
      return jsonify({'error': str(e)})
  else:
    return jsonify({'error': 'Invalid file format'})


def allowed_file(filename):
  return '.' in filename and filename.rsplit(
      '.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
  app.run(debug=True)
